import cv2
from scipy import stats
import numpy as np
import os
import glob
from collections import OrderedDict
import shutil
from tqdm import tqdm
import fnmatch
import matplotlib.pyplot as plt
import matplotlib.cm as cm

classes_path = r"../classes.txt"
img_path = r"C:\Users\sprit\Desktop\P4data\data\obj"
time_split = r"./time_split"
heat_map_storage = r"./heat_maps"
templates_path = r"./Full_Template/Aug"
count_dictionary = {"Morning": 0, "Afternoon": 0, "Evening": 0, "Night": 0, "EarlyMorning": 0}
unreadable_image_path = r"./unreadable_images"
classes, heatmap_dict, co = {}, {}, 0
classes_raw = open(classes_path, "r")
classes_read = classes_raw.read()
classes_list = classes_read.split('\n')
for a_class in classes_list:
    classes[co] = a_class
    co += 1
print("Classes are", classes)


def img_crop(img, coord):
    height, width, c = img.shape
    x, y, w_size, h_size = coord
    center_x = int(x * width)
    center_y = int(y * height)
    w = int(w_size * width)
    h = int(h_size * height)
    x = center_x - (w / 2)
    y = center_y - (h / 2)
    img = img[int(y):int(y) + int(h), int(x):int(x) + int(w)]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def find_time(frame):
    height, width = frame.shape[:2]
    q1, q2, q3, q4 = [], [], [], []
    for i in range(10):
        for j in glob.glob(templates_path + "/*"):
            if i == int(j.split("\\")[-1]):
                for k in glob.glob(j + "/*.jpg"):
                    temp = cv2.imread(k, 0)
                    wi, hi = temp.shape[::-1]
                    res = cv2.matchTemplate(frame, temp, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.80
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):
                        (x1, y1), (x2, y2) = pt, (pt[0] + wi, pt[1] + hi)
                        cx = ((x1 + x2) / 2) / width
                        cy = ((y1 + y2) / 2) / height
                        if cx < 0.5:
                            q1.append(i) if cy < 0.5 else q4.append(i)
                        else:
                            q2.append(i) if cy < 0.5 else q3.append(i)
    line = ''
    for lent in [q1, q2, q4, q3]:
        if len(lent) > 0:
            line += str(stats.mode(lent)[0][0])
    return line


def time_check(input_time):
    time_list = {"Morning": [[7, 12]], "Afternoon": [[12, 16]], "Evening": [[16, 20]], "Night": [[20, 25], [0, 4]],
                 "EarlyMorning": [[4, 7]]}
    values = list(time_list.values())
    key = list(time_list.keys())
    for i in values:
        for j in i:
            if int(input_time) in range(j[0], j[1]):
                position = values.index(i)
                count_dictionary[key[position]] += 1
    return count_dictionary


def result_validation(raw_time):
    if len(raw_time) > 2:
        dum = "".join(OrderedDict.fromkeys(raw_time))
        if len(dum) < 2:
            dum = dum + dum
        raw_time = dum
    # proper_list.append(raw_time)
        if int(raw_time) > 24:
            # print("Before....", raw_time)
            raw_time = str(raw_time)
            raw_time = raw_time[-1:] + raw_time[1:-1] + raw_time[:1]
            # print("After...", raw_time)
    return str(raw_time)


def graph(diction):
    keys = list(diction.keys())
    va = list(diction.values())
    plt.figure(figsize=(8, 4))
    # creating the bar plot
    plt.bar(keys, va, color='green', width=0.4)
    for i in range(len(keys)):
        plt.text(i, va[i]//2, va[i], ha='center')
    plt.xlabel('Timing', weight='bold', style='italic')  # naming the x-axis
    plt.ylabel('Count', weight='bold', style='italic')  # naming the y-axis
    plt.title('Timing graph', weight='bold')  # Title of the chart
    # To plot value in center of graph
    plt.savefig("Timing Graph.jpg")
    plt.show()


def heat_map(datasets_path, folder_name):
    for d in os.listdir(datasets_path):
        dum = d.split(".")
        if dum[1] == "jpg":
            file = open(datasets_path + "/" + str(dum[0]) + ".txt").read()
            img = cv2.imread(datasets_path + "/" + str(dum[0]) + ".jpg")
            h, w, c = img.shape
            for lines in file.split("\n"):
                cord = lines.split(" ")
                if len(lines) > 0:
                    index, x1, y1, w_size, h_size = cord
                    if int(index) in list(classes.keys()):
                        if index not in heatmap_dict.keys():
                            heatmap_dict[index] = [np.zeros_like(np.ndarray(shape=(h, w))), img]
                        x_start = float(x1) - float(w_size) / 2
                        y_start = float(y1) - float(h_size) / 2
                        x_end = x_start + float(w_size)
                        y_end = y_start + float(h_size)
                        heatmap_dict[index][0][int(y_start * h):int(y_end * h), int(x_start * w):int(x_end * w)] += 1
    for cls in heatmap_dict.keys():
        plt.clf()
        plt.imshow(np.squeeze(cv2.cvtColor(heatmap_dict[cls][1], cv2.COLOR_BGR2RGB)))
        plt.imshow(heatmap_dict[cls][0], cmap=cm.hot, alpha=0.5)
        plt.colorbar()
        if int(cls) in list(classes.keys()):
            save_var = classes[int(cls)] + "_" + str(folder_name)
            storage_path = os.path.join(heat_map_storage, str(folder_name))
            plt.title("%s_heat_map.jpg" % save_var, weight='bold')
            plt.savefig(storage_path + "/%s_heat_map.jpg" % save_var)
        # plt.show()


if __name__ == "__main__":
    count, count_diction, result, check_count = 0, 0, 0, 0
    # for image_path in glob.glob(img_path + "/*.jpg"):
    for image_path in tqdm(glob.glob(img_path + "/*.jpg")):
        # coordinates = [[0.210938, 0.072222, 0.025000, 0.029630], [0.241406, 0.071759, 0.023438, 0.030556],
        #                [0.272656, 0.071759, 0.024479, 0.030556]]
        coordinates = [[0.242969, 0.074537, 0.025521, 0.032407]]
        image = cv2.imread(image_path)
        # h_1, w_1 = image.shape[:2]
        # if w_1 != 1080:
        #     image = cv2.resize(image, (1920, 1080))
        for coordinate in coordinates:
            crop_image = img_crop(image, coordinate)
            # cv2.imshow("hello", crop_image)
            # cv2.waitKey(0)
            result = find_time(crop_image)
        # print("........", result)
        proper_time = result_validation(result)
        filename = os.path.basename(image_path)
        only_name = filename.split(".")[0]
        # print("...............", filename)
        # print("........", int(proper_time))
        if len(proper_time) == 2 and int(proper_time) < 24:
            count_diction = time_check(proper_time)
            folder_name_string = ("".join(proper_time))
            storage = os.path.join(time_split, folder_name_string)
            heat_map_store = os.path.join(heat_map_storage, folder_name_string)
            # print(storage)
            if not os.path.exists(storage):
                os.makedirs(storage)
            shutil.copy(image_path, storage)
            shutil.copy(img_path + "/" + only_name + ".txt", storage)
            if not os.path.exists(heat_map_store):
                os.makedirs(heat_map_store)
        else:
            shutil.copy(image_path, unreadable_image_path)
            shutil.copy(img_path + "/" + only_name + ".txt", unreadable_image_path)
            count += 1
    print("Full Count :", count_diction)
    print("Total unreadable image count: ", count)
    print("Heat Map generation started......")
    graph(count_diction)
    heat_map_check = input("After moving unreadable images manually pls enter y  -  ")
    if heat_map_check == "y" or heat_map_check == "Y":
        for paths in tqdm(os.listdir(time_split)):
            full_path = (os.path.join(time_split, paths))
            heat_map(full_path, paths)
