import os
from itertools import combinations_with_replacement
from tqdm import tqdm
import collections
import shutil
import fnmatch

dataset_path = r"./dataset"  # dataset Path
class_path = r"./classes.txt"  # Dataset Classes.txt path


def combination(length, classes_data):
    global combinations_count
    comb = []
    for i in range(1, length + combinations_count):  # looping from 1 to 1 + combinations_count
        item = combinations_with_replacement(classes_data, i)  # creating combination with itertools library
        for loop in item:
            comb.append(list(loop))  # appending the created combinations
    return comb


def individual_count_check(data, combinations_list, text_path, img_path):
    global folder, numbers_dictionary
    check_num, folder_name = [], []
    for txt_data in data:  # Looping over txt file data
        if len(txt_data) > 0:  # check if line is empty or not
            class_index = int(txt_data.split(" ")[0])  # get yolo index class only [0 0.3245, 0.9875, 0.8764, 0.6543]
            # 0-> index
            if class_index >= 0:  # additional check for index vale
                check_num.append(class_index)  # appending all classes index in one txt file
    index_in_txt = check_num
    for num in sorted(check_num):  # sorting the index file
        class_name = idx_name_map[num]  # getting class name
        folder_name.append(class_name)
        folder = "".join(folder_name)
    new_path = r"./split/" + str(folder)  # full folder path
    else_path = r"./split/else/"  # else folder path
    for d in combinations_list:
        if collections.Counter(index_in_txt) == collections.Counter(d):  # sorting in same order and checking equality
            # print(d)
            numbers_dictionary[str(d)] += 1  # if combination matches the increment the count
            shutil.copy(text_path, new_path)  # copy the txt file to its new path
            shutil.copy(img_path, new_path)  # copy the image file to its new path
        elif sorted(check_num) not in combinations_list:  # if combinations are not equal
            shutil.copy(text_path, else_path)  # move image and txt file to else path
            shutil.copy(img_path, else_path)


def get_individual_txt(path, comb):
    text_file = [w for w in os.listdir(path) if w.endswith(".txt") and w != "classes.txt"]  # fetch all txt file
    for textFile in tqdm(text_file):
        without_extension = os.path.splitext(textFile)[0]  # getting only file name
        txt_data = []
        txt_path = path + "/" + without_extension + ".txt"  # Yolo individual txt file full path
        img_path = path + "/" + without_extension + ".jpg"  # txt respective image path
        if os.path.exists(txt_path) and os.path.exists(img_path):  # both image and txt file exists check
            fil = open(txt_path, "r")  # open yolo format txt file in read mode
            txt_data.append(fil.read().split("\n"))  # appending read lines
            individual_count_check(txt_data[0], comb, txt_path, img_path)  # combinations based image copy function


def converter(name_origin_dictionary, local_index):
    holder_dict = {}
    for k, v in name_origin_dictionary.items():
        holder_list = []
        for item in eval(k):
            holder_list.append(local_index[item])  # list that holds class name of combination
        holder_dict[str(holder_list)] = v  # dic with class name and combination count
    return holder_dict


def create_folder(combinations_path_names):
    el_path = r"./split/" + "else"
    for comb_path_name in combinations_path_names:
        dum = "".join(eval(comb_path_name))  # converting cls variables into string
        full_path = r"./split/" + str(dum)  # Full path so that images will save inside a folder split
        if not os.path.exists(full_path):
            os.makedirs(full_path)  # creating the folder if it is not pre exists
        if not os.path.exists(el_path):
            os.makedirs(el_path)  # Creating else folder to store data that are not covered in combinations


def delete_empty_dir(del_path):
    walk = list(os.walk(del_path))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:  # if folder length is empty loop in
            os.rmdir(path)  # remove that empty folder


if __name__ == "__main__":
    combinations_count = 4  # Enter the length of the combinations list eg-(2-> [aa, bb] 3-> [aaa, bbb])
    numbers_dictionary, idx_name_map, name_dictionary, folder = {}, {}, {}, ""  # Initializing Variables
    fi = open(class_path, "r")  # Opening classes.txt file in Read Mode
    dats_in_classes = fi.read()  # Reading the classes.txt file
    classes = dats_in_classes.split('\n')  # As read contains '/n' removing it
    # temp_cls_count = 0
    for cls_index_count, a_class in enumerate(classes):  # Looping classes to create a dictionary
        idx_name_map[cls_index_count] = a_class  # saving Dictionary with index 0, 1, 2, ....
        # temp_cls_count += 1
    print("Classes are", idx_name_map)
    print("Total image files in master folder are:", len(fnmatch.filter(os.listdir(dataset_path), '*.jpg')))
    # Using FN match Library to fetch the image count
    classes_count = len(classes)  # Getting classes Count
    classes_count_range = range(classes_count)  # for combination gen getting class range
    combinations_number = combination(classes_count, classes_count_range)  # Generating combination based on classes
    combinations_name = combination(classes_count, classes)  # Generating combinations based on classes name
    for dump in combinations_number:
        numbers_dictionary[str(dump)] = 0  # Creating dictionary with combinations number as key and '0' as value
    for dump_2 in combinations_name:
        name_dictionary[str(dump_2)] = 0  # Creating dictionary with combinations name as key and '0' as value
    create_folder(list(name_dictionary.keys()))  # creating a folders to save combinations
    # print("Combinations are:", name_combination)\

    # once Combinations are generated we need to read Yolo file and check for combination and put them in folders
    get_individual_txt(dataset_path, combinations_number)  # Read and check combinations function
    perfect_dictionary = converter(numbers_dictionary, idx_name_map)  # assign name to the class index
    delete_empty_dir(r"./split")  # delete empty folder
    if os.path.exists(r"./split/" + "else"):
        print("Else folder image count :", len(fnmatch.filter(os.listdir(r"./split/" + "else"), '*.jpg')))
    print("Classes count based on combinations are :", perfect_dictionary)
