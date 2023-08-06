import numpy as np
import matplotlib.pyplot as plt
import os, fnmatch #to look for your image
import pandas as pd
from scipy import ndimage as ndi
import seaborn as sns

from scikit-image import io #to load the imported image as ndarray
from scikit-image import data, color
from scikit-image.util import img_as_ubyte
from scikit-image.filters import try_all_threshold
from scikit-image.filters import threshold_otsu # OMM segmentation
from scikit-image.filters import threshold_triangle, threshold_yen # NUC segmentation
from scikit-image.morphology import remove_small_objects
from scikit-image.segmentation import clear_border
from scikit-image.measure import find_contours


class mito_segmentator():
    
    def __init__(self,
                threshold_mito=threshold_otsu,
                threshold_nuc=threshold_triangle,
                threshold_seg=threshold_otsu ,
                area_min_mito=0, area_min_nuc=0,
                remove_not_overlaped='nuc', clear_borders=True,
                seg_type='fiji'):
        
        self.threshold_mito = threshold_mito
        self.threshold_nuc = threshold_nuc
        self.threshold_seg = threshold_seg
        self.area_min_mito = area_min_mito
        self.area_min_nuc = area_min_nuc
        self.remove_not_overlaped = remove_not_overlaped #'mito', 'nuc', 'both', False
        self.clear_borders = clear_borders
        self.mode = 'batch' #'single'
        self.folders = None
        self.raw_data = None
        self.analyzed_data = None
        self.seg_type = seg_type # 'weka', 'fiji'
        
    def _segmentator(self, path_mito, path_nuc, path_segmito, path_segnuc):
        '''
        Segmentation of mitochondria and nucleoids and obtention of data
        '''
        if path_segmito == False:
            method_mito = f'from image {self.threshold_mito}'
        else:  method_mito = f'from mask {self.threshold_seg}'
        if path_segnuc == False:
            method_nuc = f'from image {self.threshold_nuc}'
        else:  method_nuc = f'from mask {self.threshold_seg}'
        #Get files
        file_omm = os.path.join(path_mito)
        file_nuc = os.path.join(path_nuc)
        if path_segmito:
            file_segmito = os.path.join(path_segmito)
            loaded_mitomask = io.imread(file_segmito)
        if path_segnuc:
            file_segnuc = os.path.join(path_segnuc)
            loaded_nucmask = io.imread(file_segnuc)

        #Read files as images
        imraw_omm = io.imread(file_omm) #original image
        imraw_nuc = io.imread(file_nuc)
        
        #adaptor for 2d images only 1 time
        if imraw_omm.shape ==2:
            imraw_omm = imraw_omm[np.newaxis,...]
            imraw_nuc = imraw_nuc[np.newaxis,...]
        
        #channel selection if needed, modify for new masks
        if path_segmito == True:
            if self.seg_type == 'weka':
                iomm = loaded_mitomask[:,:,:,0] #https://stackoverflow.com/questions/36354639/python-list-slicing-with-string-argument
            if self.seg_type == 'fiji':
                iomm = loaded_mitomask
            iomm = imraw_omm #imraw[:,:,:,channel_omm] #image in the OMM channel
        else: iomm = loaded_mitomask[:,:,:,0] #https://stackoverflow.com/questions/36354639/python-list-slicing-with-string-argument

        #TODO solve for 2 dimensions
                 
                 
        if path_segmito == False:
            iomm = imraw_omm #imraw[:,:,:,channel_omm] #image in the OMM channel
        else: iomm = loaded_mitomask[:,:,:,0] #https://stackoverflow.com/questions/36354639/python-list-slicing-with-string-argument

        if path_segnuc == False:
            inuc = imraw_nuc #imraw[:,:,:,channel_omm] #image in the OMM channel
        else: inuc = loaded_nucmask[:,:,:,0]

        t,x,y = iomm.shape #get image shape

        #Define the data structure
        columns = { 'Frame':[], 'Object':[], 'Method':[],
                   'Num':[], 'Area':[], 'Im':[], 'Mask':[], 'Mask_full':[]}
        mito_df = pd.DataFrame(columns)

        for i in range(t-1):
            imraw_mito_frame = imraw_omm[i,:,:]
            imraw_nuc_frame = imraw_nuc[i,:,:]
            im_omm = iomm[i,:,:] #image at frame i
            im_nuc = inuc[i,:,:]

            #segmentation
            if path_segmito == False:
                binary_omm = im_omm > self.threshold_mito(im_omm)
            else:  binary_omm = im_omm > self.threshold_seg(im_omm)

            if path_segnuc == False:
                binary_nuc = im_nuc > self.threshold_nuc(im_nuc)
            else: binary_nuc = im_nuc > self.threshold_seg(im_nuc)

            #closing if necesary
            #bw = closing(image > thresh, square(3))

            #clear borders
            if self.clear_borders == True:
                cleared_binary_omm = clear_border(binary_omm)
                cleared_binary_nuc = clear_border(binary_nuc)
            else:
                cleared_binary_omm = binary_omm
                cleared_binary_nuc = binary_nuc

            #remove small objects
            binary_rso_omm = remove_small_objects(cleared_binary_omm, min_size=self.area_min_mito)
            binary_rso_nuc = remove_small_objects(cleared_binary_nuc, min_size=self.area_min_nuc)

            #remove nucleoids that are not in a valid mito
            if self.remove_not_overlaped == 'mito':
                binary_rso_omm = binary_rso_nuc*binary_rso_omm
            elif self.remove_not_overlaped == 'nuc':
                binary_rso_nuc = binary_rso_nuc*binary_rso_omm
            elif self.remove_not_overlaped == 'both':
                #TODO review this part
                binary_rso_omm = binary_rso_nuc*binary_rso_omm
                binary_rso_nuc = binary_rso_nuc*binary_rso_omm
            else: pass
            
            #labeling and number
            labeled_omm, num_omm = ndi.label(binary_rso_omm)
            labeled_nuc, num_nuc = ndi.label(binary_rso_nuc)

            #calculations
            area_tomm = np.sum(binary_rso_omm)*0.0018#23.47**2 #this transforms pixels into um #TODO make this an argument
            area_tnuc = np.sum(binary_rso_nuc)*0.0018#23.47**2

            for m in range(1, num_omm):          
                temp_mito_df = { 'Frame':i+1, 'Object': 'Mito_OMM', 'Method': f'{method_mito}',
                                'Num':m, 'Area': np.sum(labeled_omm==m)*0.0018, 
                                'Im': imraw_mito_frame, 'Mask': labeled_omm==m, 'Mask_full':labeled_omm}
                mito_df = mito_df.append(temp_mito_df,ignore_index=True )  
            for n in range(1, num_nuc):
                temp_mito_df = { 'Frame':i+1, 'Object': 'Nuc', 'Method': f'{method_nuc}',
                                'Num':n, 'Area':np.sum(labeled_nuc==n)*0.0018,
                                'Im': imraw_nuc_frame, 'Mask':labeled_nuc==n, 'Mask_full':labeled_nuc}
                mito_df = mito_df.append(temp_mito_df,ignore_index=True )
        return mito_df
        
    def folder_analysis(self, rootdir, folders=[], 
                        pattern_file='*.tif', pattern_mito='mito*', pattern_nuc='nuc*',
                        pattern_segmito='False', pattern_segnuc='False'):  
        self.folders = folders
        if pattern_segmito == 'False':
            method_mito = f'from image {self.threshold_mito}'
        else:  method_mito = f'from mask {self.threshold_seg}'
        if pattern_segnuc == 'False':
            method_nuc = f'from image {self.threshold_nuc}'
        else:  method_nuc = f'from mask {self.threshold_seg}'
        all_data_df = pd.DataFrame()
        #folders = range(1,8) # folders can be called numerically access them easily
        for f in folders: #access to folders
            path_mito = False
            path_nuc = False
            path_segmito = False
            path_segnuc = False
            listOfFiles = os.listdir(rootdir + str(f))
            pattern0 = pattern_file
            pattern1 = pattern_mito # pattern to recognize OMM images
            pattern2 = pattern_nuc # pattern to recognize NUC images
            pattern3 = pattern_segmito
            pattern4 = pattern_segnuc
            for entry in listOfFiles: #reads the files in the folder
                if fnmatch.fnmatch(entry, pattern0):
                    print('going'+ str(f))
                    if fnmatch.fnmatch(entry, pattern1):
                        print('Analysis mito:')
                        path_mito = os.path.join(rootdir + str(f) + '/' + entry)
                        print(entry)
                    elif fnmatch.fnmatch(entry, pattern2):
                        print('Analysis nuc:')
                        path_nuc = os.path.join(rootdir + str(f) + '/' + entry)
                        print(entry)
                    elif fnmatch.fnmatch(entry, pattern3):
                        print('Analysis segmented mito:')
                        path_segmito = os.path.join(rootdir + str(f) + '/' + entry)
                        print(entry)
                    elif fnmatch.fnmatch(entry, pattern4):
                        print('Analysis segmented nuc:')
                        path_segnuc = os.path.join(rootdir + str(f) + '/' + entry)
                        print(entry)
                    else: continue
            print('--------------------')
            mito_df = self._segmentator(path_mito, path_nuc, path_segmito, path_segnuc)
            mito_df['Folder']= f 
            all_data_df = all_data_df.append(mito_df, ignore_index=True)
            self.raw_data = all_data_df
            
            analysis_df = pd.DataFrame()
            frames = [1]
            for folder in folders:
                for frame in frames:
                    nuc_num_pframe = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Nuc']['Num']
                    mito_num_pframe = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Mito_OMM']['Num']
                    mito_area_pframe = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Mito_OMM']['Area']
                    nuc_area_pframe = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Nuc']['Area']
                    
                    
                    temp_mito_df = { 'Folder':folder, 'Frame':frame,  'Method': f'Mito {method_mito}, Nuc {method_nuc}',
                                    'Num Nuc':nuc_num_pframe.max(), 'Num Mito':mito_num_pframe.max(),
                                    'Total area Nuc':nuc_area_pframe.sum(), 'Total area Mito':mito_area_pframe.sum(),
                                    'Mean area Nuc':nuc_area_pframe.sum()/nuc_num_pframe.max() , 'Mean area Mito':mito_area_pframe.sum()/mito_num_pframe.max(),
                                    'Num Nuc/Total area Mito':nuc_num_pframe.max()/mito_area_pframe.sum(), 'Total area Nuc/Total area Mito':nuc_area_pframe.sum()/mito_area_pframe.sum()
                                    }
                    analysis_df = analysis_df.append(temp_mito_df,ignore_index=True )
            self.analyzed_data = analysis_df
    
    def get_raw_data(self, name, save_as='xlsx' ):
        if save_as == 'xlsx':
            self.raw_data.to_excel(f'{name}.xlsx', sheet_name = 'Sheet1')
        elif save_as == 'json':
            self.raw_data.to_json(orient="index")
        else:
            return self.raw_data

    def get_analyzed_data(self, name, save_as='excel' ):
        if save_as == 'xlsx':
            self.analyzed_data.to_excel(f'{name}.xlsx', sheet_name = 'Sheet1')
        elif save_as == 'json':
            pass
        else:
            return self.analyzed_data
        pass
        
    def get_masks(self, num, frame, folders='all'):
        all_data_df = self.raw_data
        if folders == 'all':
            folders = self.folders
        else: folders = folders
        
        for folder in folders:
            im_nuc = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Nuc'][all_data_df['Num']==num]['Im']
            np_nuc = np.array(im_nuc)
            plt.figure(figsize=(12,12), dpi=300)
            plt.imshow(np_nuc[0], cmap='gray')
            plt.savefig(f'object Nuc folder {folder} raw.png', dpi=300)
            
            skimage_nuc_mask = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Nuc'][all_data_df['Num']==num]['Mask_full']
            np_nuc_skimage = np.array(skimage_nuc_mask)
            plt.figure(figsize=(12,12), dpi=300)
            plt.imshow(np_nuc[0], cmap='gray')
            contours1 = find_contours(np_nuc_skimage[0]>0, 0.5)
            for n,contour in enumerate(contours1):
                plt.plot(contour[:,1], contour[:,0], 'g')
            plt.savefig(f'object Nuc folder {folder} method skimage.png', dpi=300)

            im_mito = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Mito_OMM'][all_data_df['Num']==num]['Im']
            np_mito = np.array(im_mito)
            plt.figure(figsize=(12,12), dpi=300)
            plt.imshow(np_mito[0], cmap='gray')
            plt.savefig(f'object Mito_OMM folder {folder} raw.png', dpi=300)

            skimage_mito_mask = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Mito_OMM'][all_data_df['Num']==num]['Mask_full']
            np_mito_skimage = np.array(skimage_mito_mask)
            plt.figure(figsize=(12,12), dpi=300)
            plt.imshow(np_mito[0], cmap='gray')
            contours1 = find_contours(np_mito_skimage[0]>0, 0.5)
            for n,contour in enumerate(contours1):
                plt.plot(contour[:,1], contour[:,0], 'r')
            plt.savefig(f'object Mito_OMM folder {folder} method Skimage.png', dpi=300)
            
    def explore_single_object(self, object_, folder, frame, num):
        skimage_mito_mask = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Mito_OMM'][all_data_df['Method']==method][all_data_df['Num']==num]['Mask']
        image = all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']=='Mito_OMM'][all_data_df['Method']==method][all_data_df['Num']==num]['Im']
        np_mito_skimage = np.array(skimage_mito_mask)
        np_image = np.array(image)

        plt.figure(figsize=(12,12), dpi=300)
        plt.imshow(np_image[0], cmap='gray')
        contours1 = find_contours(np_mito_skimage[0]>0, 0.5)
        for n,contour in enumerate(contours1):
            plt.plot(contour[:,1], contour[:,0], 'r')
        plt.savefig(f'object {object_} folder {folder} num {num} method {method}.png', dpi=300)

        all_data_df[all_data_df['Folder']==folder][all_data_df['Frame']==frame][all_data_df['Object']==object_][all_data_df['Method']==method][all_data_df['Num']==num]['Area']
            
    def check_shape(self, path):
        ''' :path: str
        '''
        path_to_check = os.path.join(path)
        file = io.imread(path_to_check)
        return file.shape

        