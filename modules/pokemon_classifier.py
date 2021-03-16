import cv2
import os


def load_images(path):
    cv2_images = []

    for image in os.listdir(path):
        img = cv2.imread(f"{path}/{image}", 0)
        cv2_images.append(img)

    return cv2_images


def load_classes(path):
    names = [name.replace(".png", "") for name in os.listdir(path)]

    return names


def find_descriptors(orb, images):
    des_list = []

    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        des_list.append(des)

    return des_list


def find_similar_image(orb, img, descriptors):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()

    similar_photo_index = -1

    match_list = []
    for des in descriptors:
        matches = bf.knnMatch(des, des2, k=2)
        good_matches = []

        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append([m])

        match_list.append(len(good_matches))

    if len(match_list) > 0:
        max_value = max(match_list)
        if max_value > 15:
            similar_photo_index = match_list.index(max_value)

    return similar_photo_index
