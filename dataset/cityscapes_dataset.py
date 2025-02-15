import os
import os.path as osp
import numpy as np
import random
import matplotlib.pyplot as plt
import collections
import torch
import torchvision
from torch.utils import data
from PIL import Image

class cityscapesDataSet(data.Dataset):
    def __init__(self, root, list_path, max_iters=None, crop_size=(321, 321), mean=(128, 128, 128), scale=True, mirror=True, ignore_label=255, set='val'):
        self.root = root
        self.list_path = list_path
        self.crop_size = crop_size
        self.scale = scale
        self.ignore_label = ignore_label
        self.mean = mean
        self.is_mirror = mirror
        # self.mean_bgr = np.array([104.00698793, 116.66876762, 122.67891434])
        self.img_ids = [i_id.strip() for i_id in open(list_path)]


        if not max_iters==None:
            self.img_ids = self.img_ids * int(np.ceil(float(max_iters) / len(self.img_ids)))
        self.files = []
        self.set = set
        
        
        
        # Read image paths from the list
        self.img_ids = [i_id.strip() for i_id in open(list_path)]
        
        # Debugging: Print the image paths being read
        print(f"Reading image paths from {list_path}:")
        for img_id in self.img_ids:
            print(f"Image path: {osp.join(self.root, '%s/%s/%s' % (self.set, 'img', img_id))}")
        
        # ends here
        # for split in ["train", "trainval", "val"]:
        for name in self.img_ids:
            img_file = osp.join(self.root, "%s/%s/%s" % (self.set,"img", name))
            self.files.append({
                "img": img_file,
                "name": name
            })

        print(f"Dataset initialized with {len(self.files)} files.")


    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        datafiles = self.files[index]
        #debugging lines
        file_path = self.files[index]
        print(f"Loading file: {file_path}")
        ######
        image = Image.open(datafiles["img"]).convert('RGB')
        name = datafiles["name"]

        # resize
        image = image.resize(self.crop_size, Image.BICUBIC)

        image = np.asarray(image, np.float32)

        size = image.shape
        image = image[:, :, ::-1]  # change to BGR
        image -= self.mean
        image = image.transpose((2, 0, 1))

        return image.copy(), np.array(size), name


if __name__ == '__main__':
    dst = GTA5DataSet("./", is_transform=True)
    trainloader = data.DataLoader(dst, batch_size=4)
    for i, data in enumerate(trainloader):
        imgs, labels = data
        if i == 0:
            img = torchvision.utils.make_grid(imgs).numpy()
            img = np.transpose(img, (1, 2, 0))
            img = img[:, :, ::-1]
            plt.imshow(img)
            plt.show()
