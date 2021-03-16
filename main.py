import cv2
from concurrent.futures import ThreadPoolExecutor

from modules.card_detector.main_detector import get_class_names, create_net
from modules.pokemon_classifier import load_images, load_classes, find_descriptors, find_similar_image
from modules.price_checker import get_product_data
from modules.google_sheets_api.google_sheets import write_data


class_names = get_class_names("modules/card_detector")
net = create_net("modules/card_detector")

orb = cv2.ORB_create()

cv2images = load_images("database/shining_fates")
classes = load_classes("database/shining_fates")
descriptors = find_descriptors(orb, cv2images)

executor = ThreadPoolExecutor()
running_tasks = []

cap = cv2.VideoCapture(0)

previous_image = ""


def foo(future):
    data = future.result()

    print(f"{data['name']} - {data['lowest_price']}")


while True:
    res, frame = cap.read()
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    class_ids, confs, bbox = net.detect(frame, confThreshold=0.5)

    if len(class_ids) > 0:
        for class_id, conidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
            if class_id == 84 or class_id == 77:

                cv2.rectangle(frame, box, color=(0, 0, 255), thickness=2)

                similar_image_index = find_similar_image(orb, frame_grey, descriptors)
                found_class = classes[similar_image_index]

                if similar_image_index != -1 and found_class != previous_image:
                    previous_image = found_class

                    future = executor.submit(get_product_data, "Shining-Fates", found_class)
                    executor.submit(write_data, "pokemon-ocr", future)

    cv2.putText(frame, f"{previous_image}", (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('image', frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

