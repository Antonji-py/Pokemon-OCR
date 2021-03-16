import cv2


def create_net(path):
    config_path = f"{path}/ssd_config.pbtxt"
    weights_path = f"{path}/frozen_inference_graph.pb"

    net = cv2.dnn_DetectionModel(weights_path, config_path)
    net.setInputSize(320, 320)
    net.setInputScale(1 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    return net


def get_class_names(path):
    class_names = open(f"{path}/coco.names").read().rstrip("\n").split("\n")

    return class_names
