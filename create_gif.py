import cv2
import numpy as np
from PIL import Image

size     = 200
frame    = 50
duration = 70
save_name = './test.gif'
image_paths_init  = ['./image/pxr1.png', './image/glomerulus1.png', './image/fundus1.png', './image/fish1.png']
image_paths_after = ['./image/pxr2.png', './image/glomerulus2.png', './image/fundus2.png', './image/fish2.png']



def get_percent_image(img1, img2, percent=0.5):
    """percent range from 0 to 1"""
    img1 = img1.copy()
    img2 = img2.copy()
    img  = np.zeros_like(img1)
    img_wid = img1.shape[1]
    cut = int(img_wid*percent)
    img[:, cut:,:] = img1[:, cut:, :]
    img[:, :cut,:] = img2[:, :cut]
    # add a vertical red line to indicate the cut
    img[:, cut-1:cut+1, :] = [235, 0, 50]
    return img



def build_frame_list(images_init, images_after, frame=frame):

    img_list = []
    for i in range(0, frame):
        img = get_percent_image(images_init, images_after, i/frame)
        img = Image.fromarray(img)
        img_list.append(img)

    return img_list


def main():
    # load every image, resize it and concatenate them horizontally
    images_init = [cv2.imread(path)[...,::-1] for path in image_paths_init]
    images_init = [cv2.resize(image, (size, size)) for image in images_init]
    images_init = np.concatenate(images_init, axis=1)

    images_after = [cv2.imread(path)[...,::-1] for path in image_paths_after]
    images_after = [cv2.resize(image, (size, size)) for image in images_after]
    images_after = np.concatenate(images_after, axis=1)

    assert len(image_paths_init) == len(image_paths_after)
    # save as gif
    img_list = build_frame_list(images_init, images_after, frame=frame)
    img_list[0].save(save_name, save_all=True, append_images=img_list[1:], duration=duration, loop=0)


if __name__ == '__main__':
    main()


