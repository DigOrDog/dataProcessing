"""
(1) 读取文件夹的图片和xml文件
(2) 根据命名筛选，拷贝到对应文件
"""
import os
import xml.etree.ElementTree as ET
import shutil
from sklearn.model_selection import train_test_split
import win32gui

negative_instance = [532]


def copy_files(origin_path, new_path, begin_index, end_index):
    for file_name in os.listdir(origin_path):
        index = int(file_name.split('.')[0])
        # print(file_name, type(file_name), index, type(index))
        for instance in negative_instance:
            if instance == index:
                continue
        if begin_index <= index < end_index:
            origin_file_path = os.path.join(origin_path, file_name)
            new_file_path = os.path.join(new_path, file_name)
            shutil.copy(origin_file_path, new_file_path)
            print(str(index) + "completed")


def split_train_valid(train_data_path, valid_data_path, train_size):
    img_path = r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\images'
    label_path = r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\labels'
    img_name = []
    label_name = []
    x = []
    for _, _, filenames in os.walk(img_path):
        for filename in filenames:
            img_name.append(filename)
    for _, _, filenames in os.walk(label_path):
        for filename in filenames:
            label_name.append(filename)
    img_name.sort()
    label_name.sort()
    for i in range(len(img_name)):
        x.append([img_name[i], label_name[i]])
    x_train, x_valid = train_test_split(x, train_size=train_size, random_state=10)
    # x_train, x_valid  [img_name, label_name]
    for name_img, name_label in x_train:
        shutil.copy(os.path.join(img_path, name_img), os.path.join(os.path.join(train_data_path, 'images'), name_img))
        shutil.copy(os.path.join(label_path, name_label),
                    os.path.join(os.path.join(train_data_path, 'labels'), name_label))

    for name_img, name_label in x_valid:
        shutil.copy(os.path.join(img_path, name_img), os.path.join(os.path.join(valid_data_path, 'images'), name_img))
        shutil.copy(os.path.join(label_path, name_label),
                    os.path.join(os.path.join(valid_data_path, 'labels'), name_label))

    print(len(img_name), len(label_name))


def delete_some_category(origin_path, save_path, category_name):
    for _, _, files in os.walk(origin_path):
        cnt = 0
        for file_name in files:
            cnt = cnt + 1
            print(str(cnt) + '/' + str(len(files)) + ' is working!')
            tree = ET.parse(os.path.join(origin_path, file_name))
            root = tree.getroot()
            for object_detection in root.findall('object'):
                name = object_detection.find('name')
                # print('========================')
                # print(name.text, type(name.text))
                # print(category_name, type(category_name))
                # print('========================')
                if category_name.count(name.text) > 0:
                    root.remove(object_detection)
            tree.write(os.path.join(save_path, file_name))


def according_to_file_to_add_scrollbar(target_path, to_add_objects_path):
    for _, _, files in os.walk(target_path):
        for file_name in files:
            tree = ET.parse(os.path.join(target_path, file_name))
            root = tree.getroot()
            for thing in ET.parse(os.path.join(to_add_objects_path, file_name)).getroot().findall('object'):
                root.append(thing)
            tree.write(os.path.join(target_path, file_name))


def add_objects(to_add_objects_path, file_path=None, begin_index=None, end_index=None):
    """
    :param to_add_objects_path:    待添加的目标集合
    :param file_path:              xml文件路径
    :param begin_index:            开始位置【包含】
    :param end_index:              结束位置【不包含】
    :return:
    """
    tree = ET.parse(to_add_objects_path)
    # print(tree)
    root = tree.getroot()
    object_detection = root.findall('object')
    for _, _, files in os.walk(file_path):
        for file_name in files:
            if begin_index <= int(file_name.split('.')[0]) < end_index:
                t = ET.parse(os.path.join(file_path, file_name))
                rt = t.getroot()
                for kiss in object_detection:
                    rt.append(kiss)
                t.write(os.path.join(file_path, file_name))

        # print(object_detection.find('name').text)


def remove(file_path=None, begin_index=None, end_index=None):
    for _, _, files in os.walk(file_path):
        for file_name in files:
            if begin_index <= int(file_name.split('.')[0]) < end_index:
                duplicate_remove(os.path.join(file_path, file_name))


def duplicate_remove(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    clickable_set, input_set, scrollbar_set = set(), set(), set()
    object_detection = root.findall('object')
    for my_object in object_detection:
        last_clickable_cnt, last_input_cnt, last_scrollbar_cnt = len(clickable_set), len(input_set), len(scrollbar_set)
        kind = my_object.find('name').text
        box = my_object.find('bndbox')
        x_min, y_min, x_max, y_max = int(box.find('xmin').text), int(box.find('ymin').text), int(box.find('xmax').text), \
                                     int(box.find('ymax').text)
        if x_max - x_min <= 3 or y_max - y_min <= 3:
            root.remove(my_object)
            continue
        if kind == 'Clickable':
            clickable_set.add((x_min, y_min, x_max, y_max))
            if last_clickable_cnt == len(clickable_set):
                root.remove(my_object)
        elif kind == 'Input':
            input_set.add((x_min, y_min, x_max, y_max))
            if last_input_cnt == len(input_set):
                root.remove(my_object)
        elif kind == 'ScrollBar':
            scrollbar_set.add((x_min, y_min, x_max, y_max))
            if last_scrollbar_cnt == len(scrollbar_set):
                root.remove(my_object)
    tree.write(file_path)


def test_set():
    add = set()
    add.add(('1', '2', '3', '4'))
    add.add(('1', '2', '4', '3'))
    add.add(('1', '2', '3', '4'))
    print(len(add))
    for ap in add:
        print(ap)


def test_find_findall(file_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\xmls\1060.xml'):
    "find与finall均只能查找儿子节点，子孙无法查询，后者返回的是list，前着返回的是值"
    tree = ET.parse(file_path)
    root = tree.getroot()
    x = root.findall('object')
    print(x, type(x))
    y = root.find('object')
    print(y, type(y))

    z = y.find('bndbox').findall('xmin')
    print(z, type(z))
    t = y.find('bndbox').find('xmin')
    print(t, type(t))


def copy_parallel_files(target_path, origin_path, new_path):
    index_name = []
    for file_name in os.listdir(target_path):
        index = int(file_name.split('.')[0])
        index_name.append(index)
    for file_name in os.listdir(origin_path):
        index = int(file_name.split('.')[0])
        # print(file_name, type(file_name), index, type(index))
        if index_name.count(index) > 0:
            origin_file_path = os.path.join(origin_path, file_name)
            new_file_path = os.path.join(new_path, file_name)
            shutil.copy(origin_file_path, new_file_path)
            print(str(index) + "completed")


if __name__ == '__main__':
    according_to_file_to_add_scrollbar(target_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\latestData\valid\Annotations',
                                       to_add_objects_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\scrollBarExperiment\scrollBarData\valid\Annotations')
    according_to_file_to_add_scrollbar(
        target_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\latestData\test\Annotations',
        to_add_objects_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\scrollBarExperiment\scrollBarData\test\Annotations')
    # copy_parallel_files(
    #     target_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\test\images',
    #     origin_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\rawImages',
    #     new_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\rawData\test\images')
    # copy_parallel_files(
    #     target_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\valid\Annotations',
    #     origin_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\processXmls',
    #     new_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\rawData\valid\Annotations')
    # copy_parallel_files(
    #     target_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\valid\Annotations',
    #     origin_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\newProcessXmls',
    #     new_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\secondData\valid\Annotations')
    # index = [1, 2, 3, 5, 7, 9, 2]
    # print(index.count(3))
    # print(index.count(2), type(index.count(2)))
    # remove(r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\xmls', begin_index=0, end_index=5000)
    # duplicate_remove(r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\xmls\1060.xml')
    # test_find_findall()
    # test_set()
    # add_objects(r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\copy\g.xml',
    #             r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\xmls',
    #             1423, 1531)
    # 7.xml~310.xml
    # category_name = ['ScrollBar']
    # # text = 'Clickable'
    # # print(category_name.count(text))
    # delete_some_category(
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\train\Annotations',
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\latestData\train\Annotations',
    #     category_name)
    # delete_some_category(
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\valid\Annotations',
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\latestData\valid\Annotations',
    #     category_name)
    # delete_some_category(
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\test\Annotations',
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\latestData\test\Annotations',
    #     category_name)
    # delete_some_category(
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\valid\Annotations',
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\scrollBarExperiment\myData\valid\Annotations',
    #     category_name)
    # delete_some_category(
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\myData\test\Annotations',
    #     r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\scrollBarExperiment\myData\test\Annotations',
    #     category_name)

    # split_train_valid(r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\train',
    #                   r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\valid',
    #                   0.8)
    # for instance in negative_instance:
    #     print(instance, type(instance))
    # # print(win32gui.GetDesktopWindow())
    # # print('test')
    # copy_files(origin_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\images',
    #            new_path=r'F:\sourcesStudy\master\datasetProduce\manual\newVersion\some\experiment\images',
    #            begin_index=0,
    #            end_index=1036)
# f1
# [0,1036)
# [1202,3803)

# f2
# [3909,4313)
# [4375,7306)

# f3
# [7306,9004)

# test
# [1036,1202)
# [3803,3909)
# [4313,4375)
