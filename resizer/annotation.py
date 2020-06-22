import os
from xml.etree import ElementTree


def process_annotation(annotation, image_size):
    root = annotation.getroot()
    size = root.findall("size")
    annot_image_height = 0
    annot_image_width = 0
    if len(size) == 1:
        annot_image_height = int(size[0].find("height").text)
        annot_image_width = int(size[0].find("width").text)

    size[0].find("height").text = str(image_size[1])
    size[0].find("width").text = str(image_size[0])

    for object in root.findall("object"):
        for i, boundingbox in enumerate(object.findall("bndbox")):

            # bbox[i] = {}
            # bbox[i]["xmin"] = boundingbox.find("xmin") // annot_image_height / image_size[0]
            # bbox[i]["ymin"] = boundingbox.find("ymin") // annot_image_width / image_size[1]
            # bbox[i]["xmax"] = boundingbox.find("xmax") // annot_image_height / image_size[0]
            # bbox[i]["ymax"] = boundingbox.find("ymax") // annot_image_width / image_size[1]
            new_xmin = round(int(boundingbox.find("xmin").text) / (annot_image_width / image_size[0]))
            new_ymin = round(int(boundingbox.find("ymin").text) / (annot_image_height / image_size[1]))
            new_xmax = round(int(boundingbox.find("xmax").text) / (annot_image_width / image_size[0]))
            new_ymax = round(int(boundingbox.find("ymax").text) / (annot_image_height / image_size[1]))
            boundingbox.find("xmin").text = str(new_xmin)
            boundingbox.find("ymin").text = str(new_ymin)
            boundingbox.find("xmax").text = str(new_xmax)
            boundingbox.find("ymax").text = str(new_ymax)
    return annotation, root.find("filename").text


def open_xml(annotation, image_size, output):

    resizer_size = None
    if isinstance(image_size, dict):
        resizer_size = (image_size["height"], image_size["width"])
    else:
        resizer_size = image_size

    if not os.path.exists(output):
        os.mkdir(output)

    annot = ElementTree.parse(annotation)
    updated_annot, file_name = process_annotation(annot, resizer_size)
    updated_annot.write(output+"/{0}.xml".format(file_name.split(".")[0]))


