from yolo.yolo import YOLO
from PIL import Image
from glob import glob
import os

yolo_defaults = {
    "model_path": 'yolo/model_data/custom_model_test9.h5',
    "classes_path": 'yolo/model_data/custom_classes4.txt'
}


# yolo = YOLO()  # coco dataset h5
yolo = YOLO(**yolo_defaults)  # custom h5

def detect_img(filename, output=None, car_dist_mode=False):
    image = Image.open(filename)
    image.thumbnail((640,640), Image.ANTIALIAS)
    image.save(filename)
    r_image = yolo.detect_image(image, car_dist_mode=car_dist_mode)
    print("image Detect by Yolo : {}".format(filename))
    if output:
        r_image.save(output)


def main():
    path2 = 'D:/기타/sample/'
    files = glob(path2 + '*.jpg')
    for file in files:
        name = os.path.split(file)[-1]
        detect_img(file, path2+'out/{}'.format(name))


if __name__ == '__main__':
    main()