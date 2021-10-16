import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import numpy as np

health_dic, Count_add_dic, value_1 = {}, {}, []


def classes_count_check(cla, txt_path):
    text_files = [w for w in os.listdir(txt_path) if w.endswith(".txt") and w != "classes.txt"]
    cla = [d.strip() for d in cla]
    idx_name_map = {}
    count = 0
    for a_class in cla:
        idx_name_map[count] = a_class
        count += 1
    counted_classes = {}
    for file in tqdm(text_files):
        with open(os.path.join(txt_path, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split()
                class_read = line[0]
                class_read = int(class_read)  # type casting
                actual_class = idx_name_map[class_read]
                if actual_class not in counted_classes:
                    counted_classes[actual_class] = 0
                counted_classes[actual_class] += 1
    return counted_classes


def classes_graph(dic):
    data_x = list(dic.keys())  # x axis names form dictionary
    data_height = list(dic.values())  # Y axis values form dictionary
    data_height_normalized = [x / max(data_height) for x in data_height]
    fig, ax = plt.subplots(figsize=(7, 4))  # Used to get different bar charts in same image
    my_cmap = plt.cm.get_cmap('RdYlGn')
    colors = my_cmap(data_height_normalized)
    ax.bar(data_x, data_height, color=colors)
    sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, max(data_height)))
    sm.set_array(np.array([]))
    cbar = plt.colorbar(sm)
    cbar.set_label('Color', rotation=270, labelpad=25)
    plt.xticks(list(dic.keys()))  # x-axis names to put below each bar
    plt.xlabel('Classes Name')  # naming the x-axis
    plt.ylabel('Classes Count')  # naming the y-axis
    plt.title('Classes Count Graph')  # Title of the chart
    # To plot value in center of graph
    for index, data in enumerate(data_height):
        plt.text(x=index, y=int(data / 2), s=f"{data}", fontdict=dict(fontsize=10), ha="center")
    plt.tight_layout()
    # Saving the figure.
    plt.savefig("Classes Count Graph.jpg")
    plt.show()


def health_check_detector_crisp(value_dic):
    value = list(value_dic.values())
    print("Current Max value is ", max(value))
    # max_check = input("Do you want to change it. If yes please enter (y/n)  : ")
    # if max_check == "y" or max_check == "Y":
    #     max_num = int(input("Please Enter the Max value, that all you classes count will be to checked - "))
    # else:
    max_num = max(value)
    remaining = {}
    print("New Max Number is", max_num)
    for key, val in value_dic.items():
        remaining[key] = {'classes_needed': max_num - val,
                          'percentage': int((val / max_num) * 100)}
    return remaining


def health_bal_graph_try(count_bal, real_count):
    key_1 = list(count_bal.keys())
    value_dum = list(count_bal.values())
    for i in value_dum:
        value_1.append(i["classes_needed"])
    value_2 = list(real_count.values())
    y1 = value_1
    y2 = value_2
    width = 0.35  # the width of the bars: can also be len(x) sequence
    fig2, ax2 = plt.subplots()
    ax2.bar(key_1, y2, width, align="center", color="green", label='Existing Count')
    # To plot value in center of graph
    for index, data_1 in enumerate(value_2):
        position_1 = int(data_1 / 2)
        plt.text(x=index, y=position_1, s=f"{data_1}", fontdict=dict(fontsize=10), ha="center")
    plt.tight_layout()
    ax2.bar(key_1, y1, width, align="center", color="red", bottom=y2, label='Count needed')
    # To plot value in center of graph
    for index, data_2 in enumerate(value_1):
        midpoint_sum = data_2 + value_2[index]
        position_2 = int((value_2[index] + midpoint_sum) / 2)
        plt.text(x=index, y=position_2, s=f"{data_2}", fontdict=dict(fontsize=10), ha="center")
    plt.tight_layout()
    ax2.set_ylabel('Count')
    ax2.set_title('Classes Count balance Graph')
    ax2.legend()
    plt.savefig("Classes Count balance Graph.jpg")
    plt.show()


if __name__ == "__main__":
    current_dataset_path = r"./obj"
    classes_path = r"./classes.txt"
    classes = []
    fi = open(classes_path, "r")
    for xi in fi:
        if len(xi) > 1:
            classes.append(xi.strip())
    print("classes are:", classes)
    diction = classes_count_check(classes, current_dataset_path)
    print("Classes count", diction)
    classes_graph(diction)
    # check_2 = input("Do you want to check dataset health (y/n)  : ")
    # if check_2 == "y" or check_2 == "Y":
    print("Starting classes health check detector.....")
    full_dictionary = health_check_detector_crisp(diction)
    health_bal_graph_try(full_dictionary, diction)
