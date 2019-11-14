import xml.etree.ElementTree as ET
from glob import glob
import os

# xml 을 train.txt 로 변경하는 코드


dir_data = 'dataset'
folder = '/*'
filenames = glob(dir_data + folder + '/*.xml')

# with open('model_data/coco_classes.txt') as f:
with open('model_data/custom_classes.txt') as f:
    classes = f.read().split('\n')

result = []
for filepath in filenames:
    root = ET.parse(filepath).getroot()
    filename = os.path.splitext(filepath)[0] + '.jpg'
    temp = ''
    for obj in root.iter('object'):
        classname = obj.find('name').text

        # 유사한 라벨을 하나로 취급.
        # if classname == ['human', 'people']:
            # classname = 'person'

        if classname not in classes:
            continue
        cls_id = classes.index(classname)
        box = obj.find('bndbox')
        values = [box.find(k).text for k in [
            'xmin', 'ymin', 'xmax', 'ymax']] + [str(cls_id)]
        temp += ' ' + ','.join(values)
    if temp:
        result.append(filename + temp)
        print(filename + temp)


with open('train.txt', 'w') as f:
    f.writelines('\n'.join(result))

