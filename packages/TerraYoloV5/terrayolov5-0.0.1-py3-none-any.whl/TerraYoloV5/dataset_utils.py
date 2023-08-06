# check

import os
import shutil
import random
from math import ceil

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

""" Набор функций для манипулирования  датасетами yolov5"""


def get_lab_classes(lab_list):

    #Функция принимает список меток yolov5 и возвращает список первых значений как список классов

    return [int(line.split(' ')[0]) for line in lab_list]


def get_file_labels(lab_path):
    """
    Функция парсит координаты из текстового файла

    :param lab_path: путь к файлу аннотаций
    :return:
    lab_list:list - список списков, где каждый элемент списка соответствует метке,
    первое значение  каждого вложенного списка - классу объекта
    следующие значения  - координатам рамок
    lab_classes_list: - список классов объектов приведенных к типу int,
    соответствующих каждой рамке

    NOTE: метки не проверяются, в результат попадут списки соответствующие всем строкам
    NOTE: классы и координаты в lab_list типа строка, в классы в lab_classes_list - int
    """

    lab_list, lab_classes_list = [], []
    if os.path.isfile(lab_path):
        with open(lab_path, 'r') as ann_file:
            lab_list = ann_file.read()
            lab_list = lab_list.splitlines()
            lab_list = [lab for lab in lab_list]
            lab_classes_list = get_lab_classes(lab_list)
    return lab_list, lab_classes_list


def get_filtered_label(lab_path, class_filter: list):
    """

    :param lab_path: путь к файлу с аннотацией
    :param class_filter: массив вида [class_id_1_int, class_id_2_int, ...]
    :return: список списков где элементы вложенного списка (типа str) соответствуют
    координатам bbox. Первый - классу объекта, остальные - координатам
    NOTE: координаты  НЕ проверяются, в результат попадут списки соответствующие
    всем строкам, удовлетворяющим фильтру
    """
    res = []
    if os.path.isfile(lab_path):
        lab_list, lab_classes_list = get_file_labels(lab_path)
        mask = np.in1d(lab_classes_list, class_filter)
        if np.any(mask) == True:
            res = list(np.array(lab_list)[mask])
    return res




def xywhn2xyxy_uno(x, w=640, h=640):

    """
    Преобразование координат bbox для вывода рамок объекта
    переработано из утилит yolov5
    # from general.py import xywhn2xyxy
    в yolo все функции выполнены под матричные и тензорные операции

    # Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    # y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)

    в тч для наглядности переделано под едничные значения _uno
    """


    y = np.copy(x)
    y[0] = w * (x[0] - x[2] / 2)  # + padw  # top left x
    y[1] = h * (x[1] - x[3] / 2)  # + padh  # top left y
    y[2] = w * (x[0] + x[2] / 2)  # + padw  # bottom right x
    y[3] = h * (x[1] + x[3] / 2)  # + padh  # bottom right y
    return y


def transform_label(trans_dict, label_dir, new_label_dir=None, class_filter=None):

    """
    Экспериментальная заготовка модуля трансформации координат


    :param trans_dict:
    :param label_dir:
    :param new_label_dir:
    :param class_filter:
    :return:
    """
    if not (new_label_dir):
        new_label_dir = label_dir
        #print(new_label_dir)

    if os.path.isdir(new_label_dir) == False:
        os.mkdir(new_label_dir)

    # xywhn метки ожидаются
    # trans_dict.keys = 'stretch'
    def stretch(class_xywh_list, param):
        """
        Растяжение (сжатие) рамки, умножает предпоследнюю и последнюю координату рамки
        на множитель param
        в перспективе множители могли бы быть разные по ширине и высоте
        а также адаптивные к размеру метки и изображения

        :param class_xywh_list:
        :param param:
        :return:
        """
        # растягиваем рамку на заданый  множитель param
        # print(params)
        return class_xywh_list[:-2] + [str(float(class_xywh_list[-2]) * param),
                                       str(float(class_xywh_list[-1]) * param)]

    metaop_dict = dict()
    metaop_dict['stretch'] = stretch

    for k, param in trans_dict.items():
        for f_name in os.listdir(label_dir):
            lab_list, _ = get_file_labels(label_dir + os.sep + f_name)
            new_lab_list = []
            for label in lab_list:
                if class_filter:
                    # print(f_name, lab_list, class_filter)
                    # if (class_filter): print('class_filter')
                    # break
                    ann_list = label.split()
                    if int(ann_list[0]) in class_filter:
                        new_ann = metaop_dict[k](ann_list, param)
                        new_lab_list.append(' '.join(new_ann))
                else:
                    new_lab_list.append(label)
            if len(new_lab_list) > 0:
                #отладочно if len(new_lab_list) > 1:
                    #print(f_name, len(new_lab_list))
                with open(new_label_dir + os.sep + f_name, 'w') as f:
                    # print(new_lab_list)
                    f.write('\n'.join(new_lab_list))


def copy_labels(source_lab_dir, dest_lab_dir,
                class_filter=None,
                filter_label=True
                ):
    """
    Функция копирует файлы с аннотациями, содержащими классы из class_filter
    из source_lab_dir в dest_lab_dir

    :param source_lab_dir:
    :param dest_lab_dir:
    :param class_filter:
    :param filter_label: если True - из файлов аннотаций будут также удалены метки
    классов, не входящих в class_filter
    :return:

    NOTE: если class_filter не задан будут скопированы все файлы

    """
    if (os.path.isdir(source_lab_dir) == False) or (
            len(os.listdir(source_lab_dir)) == 0):
        print(source_lab_dir, 'не найден или пуст каталог с метками')
        return

    if os.path.isdir(dest_lab_dir) == False:
        # будет ошибка если нет каталого верхнего уровня
        os.mkdir(dest_lab_dir)

    if class_filter == None:
        # тут и выше нужен фильтр по txt
        #shutil.copytree(source_lab_dir, dest_lab_dir)
        for f_name in os.listdir(source_lab_dir):
            if os.path.isfile(os.path.join(source_lab_dir, f_name)):
                shutil.copy(os.path.join(source_lab_dir, f_name),
                            os.path.join(dest_lab_dir, f_name))
    else:
        for f_name in os.listdir(source_lab_dir):
            source_path = source_lab_dir + os.sep + f_name
            lab_filtered_list = get_filtered_label(source_path, class_filter)
            if len(lab_filtered_list) > 0:
                '''
                for lab in lab_filtered_list:
                    if len(lab.split())<5: 
                        print('source_path', source_path, len() )
                        break
                '''
                # !cat {source_path}
                # print('\n**************')
                # print(f_name, lab_filtered_list)
                if filter_label == True:
                    # print(dest_lab_path+os.sep+f_name, lab_filtered_list)
                    with open(dest_lab_dir + os.sep + f_name, 'w') as lab_filtered_f:
                        # print('\n'.join(lab_filtered_list))
                        # lab_filtered_f.write('\n'.join(lab_filtered_list))
                        lab_filtered_f.write('\n'.join(lab_filtered_list))
                else:
                    shutil.copyfile(source_path, dest_lab_dir+f_name)
                # break
            pass


def show_images(img_list, box_list,
                ncols=4,
                show_label=True,
                img_size=(4, 3)):
    """
    Функция выводит изображения из списка img_list с рамками из box_list
    :param img_list: список путей к файлоам изображений
    :param box_list: список меток обектов, соответствующих файлам изображений
    :param ncols:
    :param show_label:
    :param img_size:
    :return:
    """
    nrows = ceil(len(img_list) / ncols)
    # print(img_list, box_list, nrows, ncols)
    figsize = np.array([img_size[0] * ncols, img_size[1] * nrows])
    print(figsize)
    fig, axs = plt.subplots(nrows, ncols=ncols, figsize=figsize)
    axs = axs.flat
    for ind, f_name in enumerate(img_list):
        ax = axs[ind]
        # print(f_name)
        with Image.open(f_name) as img:
            ax.imshow(img)
            if show_label == True:
                # print([int(coord) for coord in box_list[ind].split(' ')[1:]])
                for box in box_list[ind]:
                    box_xywhn = [float(coord) for coord in box.split(' ')[1:]]
                    # print(box_xywhn)
                    box_xyxy = xywhn2xyxy_uno(box_xywhn,
                                              w=img.width,
                                              h=img.height)  # 640, padw=0, padh=0
                    # print(box_xyxy, img.width, img.height)
                    ax.add_patch(
                        patches.Rectangle((box_xyxy[0:2]), box_xyxy[2] - box_xyxy[0],
                                          box_xyxy[3] - box_xyxy[1],
                                          linewidth=1, edgecolor='r', facecolor='none'))

        # if ind%len_chunk == 0:
        # plt.show()
    plt.show()
    return



def count_classes_in_lab_dir(lab_path):
    # заодно посмотрим баланс классов

    """
    Подсчет классов объектов в файлах аннотаций из каталога lab_path
    :param lab_path:
    :return:
    """
    box_list = []
    for f_name in os.listdir(lab_path):
        with open(lab_path + os.sep + f_name, 'r') as f:
            boxes = f.readlines()
            try:
                box_list += [int(box.split(' ')[0]) for box in boxes]
            except:
                print(lab_path + os.sep + f_name, boxes)
                return
            # TODO пустая строка вызовет ошибку
    value, counts = np.unique(box_list, return_counts=True)
    return value, counts, len(os.listdir(lab_path)), lab_path  # , counts/np.sum(counts)


def cut_labels(lab_dir):
    """
    Проверяет все файлы из каталога lab_dir и оставляет в каждой строке не больше
    пяти значений (четырех пробелов): подразумевается, что в каждой строке останется
    class + xywhn

    :param lab_dir:
    :return:
    NOTE: проверка bbox не производится, например bbox с недостаточным количеством
    координат останутся в файле
    """
    # TODO статистику добавить бы еще какую-нибудь
    for f_name in os.listdir(lab_dir):
        with open(lab_dir + os.sep + f_name, 'r') as f:
            box_list = f.read().splitlines()
            lab_cut = [' '.join(box.split(' ')[:5]) for box in box_list]
        with open(lab_dir + os.sep + f_name, 'w') as f:
            f.write('\n'.join(lab_cut))
    return


def check_lab_by_name(new_lab_dir, exist_lab_dir):
    """
    Функция по именам файлов без расширений проверяет наличие изображения для
    соответствующего файла аннотации

    :param new_lab_dir: путь к каталогу новых аннотаций предполагается, что эти метки
     будут добавляться в существующий каталог)
    :param exist_lab_dir: путь к каталогу обновляемых меток
    :return: возвращает мнодество общих имкен файлов - если пустое - старые аннотации
    однозначно не будут изменены при добавлении
    """
    # TODO в идеале нужно в тч под списки и генераторы как вариант переделать
    # можно также под список директорий любой длины сделать только не ясно нужно ли
    new_lab_f_name_set = set([name for name in os.listdir(new_lab_dir)
                              if name.endswith('txt')])
    exist_lab_f_name_set = set([name for name in os.listdir(exist_lab_dir)
                                if name.endswith('txt')])

    return new_lab_f_name_set & exist_lab_f_name_set


def check_img_for_lab(lab_dir, img_dir):
    """
    Функция по именам файлов без расширений проверяет наличие изображения для
    соответствующего файла аннотации
    """
    # TODO в идеале нужно в тч под списки и генераторы как вариант переделать
    lab_f_name_set = set([name[:-4] for name in os.listdir(lab_dir)
                          if name.endswith('txt')])
    img_f_name_set = set([name[:-4] for name in os.listdir(img_dir)
                          if name.endswith('jpg')])
    return lab_f_name_set & img_f_name_set


def add_img_by_lab(lab_dir, img_source_dir, img_dest_dir):
    lab_f_name_set = set([name[:-4] for name in os.listdir(lab_dir)
                          if name.endswith('txt')])

    # можно сделать словарем имя без расширения: полное имя
    img_f_name_set = set([name[:-4] for name in os.listdir(img_source_dir)
                          if name.endswith('jpg')])
    img_f_name_set = img_f_name_set & lab_f_name_set
    print(f'найдено {len(img_f_name_set)} для {len(lab_f_name_set)} файлов аннотаций')

    for f_name in img_f_name_set:
        # файлы *.JPG *.JPg и тп не скопирует
        shutil.copy(img_source_dir + os.sep + f_name + '.jpg', img_dest_dir)


def show_class_images(img_dir,
                      show_label=True,
                      lab_dir=None,
                      class_filter=(0), #если не задать - ограничит без сообщения
                      ncols=4,
                      # subdir_list=['train'],
                      img_nbr=9,
                      n_part=1,  # число частей, на которые разобъем данные
                      part_nbr=None,
                      # номер части питон (0..n_parts-1) если n_parts определено а parts_nbr покажем случайную, parts_nbr>n_parts - последнюю
                      # interact=False
                      ):
    # TODO нет подписей

    if os.path.isdir(img_dir) != True:
        print('Не найден каталог с изображениями')
        return

    if show_label == True:
        print('lab_dir', lab_dir)
        print(os.path.isdir(lab_dir))
        if os.path.isdir(lab_dir) != True:
            # Если не задан попытаемся найти относительно изображений
            new_lab_dir = os.path.abspath(img_dir + os.sep + '..' + os.sep + 'labels/')
            print(new_lab_dir)
            if lab_dir:
                print(
                    f'Не найден каталог {lab_dir}, пробуем найти метки в каталоге {new_lab_dir}')
            if os.path.isdir(new_lab_dir) == False:
                print('каталог с метками не найден')
                show_label = False

    class_filter_arr = np.array(class_filter)
    # def get_other_path():
    img_filtered, box_filtered = [], []
    # for subdir in subdir_list:

    for f_name in os.listdir(lab_dir):
        # пока пропускаем случай, когда img_nbr=-1
        with open(lab_dir + f_name, 'r') as ann_file:
            lab_list = ann_file.read().splitlines()
            lab_classes_list = np.array(get_lab_classes(lab_list))
            mask = np.in1d(lab_classes_list, class_filter)
            if np.any(mask) == True:
                # print('len(mask)',len(mask), mask, f_name)
                img_filtered.append(img_dir + f_name[:-3] + 'jpg')
                box_filtered.append(list(np.array(lab_list)[mask]))
        # print(img_nbr==False, f_name, len(img_filtered), box_filtered)
        if img_nbr > 0:
            if (len(img_filtered) > 0) & (len(img_filtered) % img_nbr == 0):
                # print(box_filtered)
                show_images(img_filtered, box_filtered,
                            ncols=ncols)  ###
                img_filtered, box_filtered = [], []
                break
    print(len(img_filtered), ' images filtered from classes ', class_filter)
    # print(img_filtered)
    if len(img_filtered) > 0:
        start_idx, end_idx = 0, None  # покажем все если что-то пойдет не так
        if img_nbr <= 0:
            print(img_nbr, n_part)
            if n_part > 0:
                part_len = len(img_filtered) / n_part
                if (part_nbr == None) or (part_nbr < 0):  # если n_part задано, а part_nbr не задано или меньше 0 - покажем случайную часть из n_part
                    part_nbr = random.randint(0, n_part - 1)
                elif part_nbr >= n_part:  # если part_nbr>n_part - покажем последнюю часть из n_part
                    part_nbr = n_part - 1

                start_idx = round(part_len * part_nbr)
                end_idx = round(start_idx + part_len)
        print(f'show images from {start_idx} to {end_idx}')
        show_images(img_filtered[start_idx:end_idx],
                    box_filtered[start_idx:end_idx],
                    ncols=ncols)  ###