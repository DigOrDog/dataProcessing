import xml.etree.ElementTree as ET


def duplicate_remove(file_path):
    """
    :param file_path: xml文件夹路径
    :return:
    """
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
