import os
from itertools import combinations_with_replacement
from tqdm import tqdm
import collections
import shutil
import fnmatch


def combination(length, classes_data):
    comb = []
    for i in range(1, length + combinations_count):
        item = combinations_with_replacement(classes_data, i)
        for loop in item:
            comb.append(list(loop))
    return comb


def individual_count_check(data, list_check, text_path, img_path):
    global folder
    check_num, folder_name = [], []
    for txt_data in data:
        if len(txt_data) > 0:
            dum = int(txt_data.split(" ")[0])
            if dum >= 0:
                check_num.append(dum)
    index_in_txt = check_num
    for num in sorted(check_num):
        val = idx_name_map[num]
        folder_name.append(val)
        folder = "".join(folder_name)
    new_path = r"./split/" + str(folder)
    else_path = r"./split/else/"
    for d in list_check:
        if collections.Counter(index_in_txt) == collections.Counter(d):
            # print(d)
            dictionary[str(d)] += 1
            shutil.copy(text_path, new_path)
            shutil.copy(img_path, new_path)
        elif sorted(check_num) not in list_check:
            shutil.copy(text_path, else_path)
            shutil.copy(img_path, else_path)


def get_individual_txt(path, comb):
    text_file = [w for w in os.listdir(path) if w.endswith(".txt") and w != "classes.txt"]
    for textFile in tqdm(text_file):
        without_extension = textFile.split(".")[0]
        txt_data = []
        txt_path = path + "/" + without_extension + ".txt"
        img_path = path + "/" + without_extension + ".jpg"
        fil = open(txt_path, "r")
        txt_data.append(fil.read().split("\n"))
        individual_count_check(txt_data[0], comb, txt_path, img_path)


def converter(count_dictionary, local_index):
    holder_dict = {}
    for k, v in count_dictionary.items():
        holder_list = []
        for item in eval(k):
            holder_list.append(local_index[item])
        holder_dict[str(holder_list)] = v
    return holder_dict


def create_folder(half_path):
    for h_path in half_path:
        dum = "".join(eval(h_path))
        full_path = r"./split/" + str(dum)
        el_path = r"./split/" + "else"
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        if not os.path.exists(el_path):
            os.makedirs(el_path)


def delete_empty_dir(del_path):
    walk = list(os.walk(del_path))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.rmdir(path)


if __name__ == "__main__":
    # split_check = input("Inorder to start dataset split based on combinations press   y    -  ")
    # if split_check == "y" or split_check == "Y":
    dataset_path = r"./obj"
    class_path = r"./classes.txt"
    combinations_count = 4
    dictionary, idx_name_map, name_dictionary, folder = {}, {}, {}, ""
    fi = open(class_path, "r")
    da = fi.read()
    classes = da.split('\n')
    co = 0
    for a_class in classes:
        idx_name_map[co] = a_class
        co += 1
    print("Classes are", idx_name_map)
    print("Total image files in master folder are:", len(fnmatch.filter(os.listdir(dataset_path), '*.jpg')))
    size = len(classes)
    classes_count = range(size)
    combinations_value = combination(size, classes_count)
    name_combination = combination(size, classes)
    for dump in combinations_value:
        dictionary[str(dump)] = 0
    for dump_2 in name_combination:
        name_dictionary[str(dump_2)] = 0
    create_folder(list(name_dictionary.keys()))
    # print("Combinations are:", name_combination)
    get_individual_txt(dataset_path, combinations_value)
    perfect_dictionary = converter(dictionary, idx_name_map)
    delete_empty_dir(r"./split")
    print("Else folder image count :", len(fnmatch.filter(os.listdir(r"./split/" + "else"), '*.jpg')))
    print("Classes count based on combinations are :", perfect_dictionary)
