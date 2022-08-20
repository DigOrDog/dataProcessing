import os

img_label = []


def find(label):
    for i in range(len(img_label)):
        if label == img_label[i]:
            return True
    return False


for file_name in os.listdir(r'F:\sourcesStudy\datasets\数据标注\annotation'):
    label = file_name.split('.')[0] + '.png'
    img_label.append(label)

for file_name in os.listdir(r'F:\sourcesStudy\datasets\数据标注\img\1001-2200'):
    if not find(file_name):
        print(file_name)
    # print(file_name)
    # label = file_name.split('.')[0] + '.xml'
#     # print(label)
# 36 (25).png
# 36 (4).png
# 45 (32).png
# 46 (22).png