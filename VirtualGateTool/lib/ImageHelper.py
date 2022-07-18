import os
import cv2 
import glob
import numpy as np

class ImageHelper():
    
    __DEFAULT_DATASET_PATH = '/nol/iTraffic/Dataset'
    #__DEFAULT_DATASET_PATH = 'D:/_Course/Project/iTraffic/Dataset'
    
    __SAMPLING_STEP = 3
    __MAX_IMAGE_COUNT = 360
    
    def __init__(self, srcpath, dstpath):
        
        self.__srcpath = self.__safeSrcPath(srcpath)
        self.__dstpath = self.__safeDstPath(dstpath)
        
        '''
        print('src1 path: ', srcpath)
        print('dst1 path: ', dstpath)
        print('src2 path: ', self.__srcpath)
        print('dst2 path: ', self.__dstpath)
        '''
        
        self.__toImgs(self.__srcpath, self.__dstpath)
        self.__imgList = self.__loadImgList(self.__dstpath)
            
    def __safeSrcPath(self, dirname):
        if os.path.isfile(dirname):
            dirname = os.path.dirname(dirname)
            
        path = os.path.join(dirname, 'screenshot.mp4')
        path = os.path.join(self.__DEFAULT_DATASET_PATH, path)
        
        if not os.path.exists(path):
            path = os.path.join(dirname, '*.mp4')
            path = os.path.join(self.__DEFAULT_DATASET_PATH, path)
        return path
        
    def __safeDstPath(self, dirname):
        path = os.path.join(self.__DEFAULT_DATASET_PATH, dirname)
        if not os.path.exists(path):
            os.mkdir(path)
        return path
    
    def __getCap(self, srcpath):
        cap = cv2.VideoCapture(srcpath)
        fps = int(round(cap.get(cv2.CAP_PROP_FPS), 0))
        total_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return cap, fps, total_count
    
    def __loadImgList(self, dstpath):
        pattern = os.path.join(dstpath, '*.jpg')
        imgList = glob.glob(pattern)
        return imgList
    
    def __toImgs(self, srcpath, dstpath):

        quality = 50
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        
        srcfiles = glob.glob(srcpath)
        
        print('found source video: ', len(srcfiles))
        
        for srcfile in srcfiles:
            
            #basename = os.path.basename(srcfile).split('.')[0]
            basename = 'screenshot'
            
            #srcpattern = '{0}/{1}_*.jpg'.format(dstpath, basename)
            srcpattern = '{0}/*.jpg'.format(dstpath)
            
            imgList = glob.glob(srcpattern)

            if len(imgList) == 0:
            
                print('converting mp4 to imgs: {0}'.format(srcfile))
                cap, fps, total_count = self.__getCap(srcfile)
                sfps = fps // self.__SAMPLING_STEP
                
                f_counter = -1
                s_counter = 0
                
                while (s_counter < self.__MAX_IMAGE_COUNT):
                    success, frame = cap.read()
                    
                    if success:
                        f_counter += 1
                        
                        if (f_counter % sfps) == 0:
                            
                            s_counter += 1
                            
                            imgfile = '{0}/{1}_{2}.jpg'.format(dstpath, basename, f_counter)
                            cv2.imencode('.jpg', frame, encode_params)[1].tofile(imgfile)
                            
                            '''
                            if not os.path.exists(imgfile):
                                cv2.imencode('.jpg', frame, encode_params)[1].tofile(imgfile)
                            '''
                    else:
                        break
                
                cap.release()
                print('done')
                
                break
            
            else:
                print('CCTV images are in screenshot folder already')
                
    def getImgList(self):
        return self.__imgList


if __name__ == "__main__":
    
    srcpath = 'D:/_Course/Project/iTraffic/Dataset/000北港大橋/IF-065/CCTV_001/CCTV_001.png'
    dstpath = 'D:/_Course/Project/iTraffic/Dataset/000北港大橋/IF-065/CCTV_001/screenshot'
    
    imageHelper = ImageHelper(srcpath, dstpath)
    
    imgList = imageHelper.getImgList()
    print(len(imgList))
    print('done')