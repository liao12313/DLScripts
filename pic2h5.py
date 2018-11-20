# -*- coding: utf-8 -*-
import h5py
import os
import glob
from shutil import copyfile, rmtree
import cv2

class H5Converter(object):
    """
    Convert all image files in the directory to .h5 extension
    """
    def __init__(self, dataset_name='X', scaled_width=960, scaled_height=625):
        self.dataset_name = dataset_name
        self.pic_scaled_width = scaled_width
        self.pic_scaled_height = scaled_height

    def _images_to_h5(self, images, h5_name):
        """
        convert all images to h5

        input: 
            images: list of all image path
            h5_name: A string end with .h5
        return:
            nothing    
        """
        if len(images) == 0:
            print('empty pic file')
            return

        h5f = h5py.File(h5_name, 'w')
        shape = (len(images), self.pic_scaled_width, self.pic_scaled_height, 3)
        maxshape=(None, self.pic_scaled_width, self.pic_scaled_height, 3)
        h5f.create_dataset(self.dataset_name, shape, maxshape=maxshape)
        for i, pic in enumerate(images):
            img = cv2.imread(pic)
            img = cv2.resize(img,
                             (self.pic_scaled_height, self.pic_scaled_width),
                             interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h5f[self.dataset_name][i] = img
        h5f.close()

    def run(self, dir_name, h5_name):
        if not os.path.isdir(dir_name):
            print('{} is not a valid dir'.format(dir_name))
            return
        images = glob.glob(dir_name+'/*.jpg', recursive=True)
        self._images_to_h5(images, h5_name)
        print('Convert Success')

if __name__ == '__main__':
    h5conerter = H5Converter()
    h5conerter.run('dir_name', 'test.h5')

