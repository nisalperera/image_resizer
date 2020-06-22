import argparse
import json
import logging
import os

from resizer.annotation import open_xml
from resizer.images import resizer

image_formats = [".jpg", ".png", ".jpeg"]


def check_image_format(image_file_ext):
    if image_file_ext in image_formats:
        return True
    else:
        return False


def load_images_annotations(image_path, annotation_path, image_size, image_output, annotations_output,
                            same_output_folder):

    if image_path is None or not os.path.isdir(image_path):
        raise ValueError("Please provide the image folder path")
    # if annotation_path is None or not os.path.isdir(annotation_path):
    #     raise ValueError("Please provide the annotations folder path")
    # if image_size is None or not isinstance(image_size, tuple) or not isinstance(image_size, dict):
    #     raise ValueError("Please provide the image size as a tuple or a dictionary")
    if same_output_folder:
        annotations_output = image_output

    image_list = os.listdir(image_path)
    wrong_image_formats = []
    for image in image_list:
        if check_image_format(os.path.splitext(image)[-1]):
            continue
        else:
            wrong_image_formats.append(image)
            logger.warning("Image extension {ext} not supported.".format(ext=os.path.splitext(image)[-1]))
            image_list.remove(image)

    if annotation_path is not None:
        annotations_list = os.listdir(annotation_path)
        wrong_annotation_formats = []
        for annotation in annotations_list:
            xml = os.path.splitext(annotation)[-1]
            if xml == ".xml":
                # correct_annotations.append(annotation)
                continue
            else:
                wrong_annotation_formats.append(annotation)
                logger.warning("Annotation file extension {0} does not support".format(os.path.splitext(annotation)[-1]))
                annotations_list.remove(annotation)
        resizer(image_path, image_list, annotation_path, annotations_list, image_size, image_output, annotations_output)
    else:
        image_list = os.listdir(image_path)
        wrong_image_formats = []
        for image in image_list:
            if check_image_format(os.path.splitext(image)[1]):
                continue
            else:
                wrong_image_formats.append(image)
                logger.warning("Image extension {ext} not supported.".format(ext=os.path.splitext(image)[1]))
                image_list.remove(image)
        resizer(image_path, image_list, size=image_size)


if __name__ == '__main__':
    logger = logging.getLogger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the config file")
    args = parser.parse_args()

    config = args.config

    with open(config, "r") as conf:
        config_file = json.load(conf)

    load_images_annotations(config_file["image_path"], config_file["annotations_path"], tuple(config_file["image_size"]),
                            config_file["image_output"], config_file["annotations_output"],
                            bool(config_file["same_folder"]))

