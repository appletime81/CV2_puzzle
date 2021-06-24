import cv2
import numpy as np
import random

click_count = 0
click_img_pos = []


def split_image():
    orig_img = cv2.imread("new_dog.jpg")
    h, w, _ = orig_img.shape
    sub_h = int(h / 3)
    sub_w = int(w / 3)

    img_dict = dict([(str(i + 1), None) for i in range(9)])

    # 分割圖片
    count = 0
    for i in range(3):
        for j in range(3):
            img_dict[str(count + 1)] = orig_img[sub_h * i:sub_h * (i + 1), sub_w * j:sub_w * (j + 1), :]
            count += 1

    list_index = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(list_index)

    new_dict = dict([(str(i + 1), None) for i in range(9)])
    for x in list_index:
        new_dict[str(list_index.index(x) + 1)] = img_dict[str(x)]

    return new_dict, orig_img


def combine_image(img_dict):
    img_list = []
    temp_list = []
    for i in range(9):
        if not i % 3:
            if temp_list:
                img_list.append(temp_list)
            temp_list = []
            temp_list.append(img_dict[str(i + 1)])
        else:
            temp_list.append(img_dict[str(i + 1)])
    img_list.append(temp_list)

    new_img_list = []
    for img in img_list:
        new_img_list.append(np.vstack(tuple([sub_img for sub_img in img])))
    new_img = np.hstack(tuple([new_sub_img for new_sub_img in new_img_list]))
    return new_img


def record_click():
    global new_img
    h, w, _ = new_img.shape
    sub_h = int(h / 3)
    sub_w = int(w / 3)
    click_dict = dict([(str(i + 1), []) for i in range(9)])
    count = 0
    for i in range(3):
        for j in range(3):
            y_pos = [y for y in range(sub_h * i, sub_h * (i + 1))]
            x_pos = [x for x in range(sub_w * j, sub_w * (j + 1))]
            for y in y_pos:
                for x in x_pos:
                    click_dict[str(count + 1)] += [[y, x]]
            count += 1
    return click_dict


def get_pos(x_coord, y_coord):
    global click_count
    global click_img_pos
    global new_img
    global new_dict
    global orig_img
    global click_dict

    click_count += 1

    for k, v in click_dict.items():
        if [x_coord, y_coord] in v:
            print(k)
            click_img_pos.append(k)

    if click_count == 2:
        new_dict[str(click_img_pos[0])], new_dict[str(click_img_pos[1])] = new_dict[str(click_img_pos[1])], new_dict[str(click_img_pos[0])]
        new_img = combine_image(new_dict)
        click_count = 0
        click_img_pos = []

        print(new_img.shape)
        print(orig_img.shape)
    if (new_img == orig_img).all():
        vic_img = cv2.imread("vic.jpg")
        cv2.namedWindow('VIC')
        cv2.imshow('VIC', vic_img)


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        get_pos(x, y)
        

if __name__ == "__main__":
    new_dict, orig_img = split_image()
    new_img = combine_image(new_dict)
    click_dict = record_click()

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', click_event)
    while (1):
        cv2.imshow('image', new_img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
