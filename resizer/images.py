import os

from PIL import Image

from resizer.annotation import open_xml


def resizer(image_path, image_list, annotation_path=None, annotation_list=None, size=(128, 128), image_output="./output"
            , annotation_output="./output"):

    resizer_size = None
    if isinstance(size, dict):
        resizer_size = (size["height"], size["width"])
    else:
        resizer_size = size

    if annotation_list is not None:
        for image, annotation in zip(image_list, annotation_list):
            pil_image = Image.open(os.path.join(image_path, image))
            pil_image = pil_image.resize(resizer_size)
            output_imagename = image.split("\\")[-1]
            open_xml(os.path.join(annotation_path, annotation), size, annotation_output)
            pil_image.save(image_output + "/{0}".format(output_imagename))
    else:
        for image in image_list:
            pil_image = Image.open(os.path.join(image_path, image))
            pil_image = pil_image.resize(resizer_size)
            output_imagename = image.split("\\")[-1]
            pil_image.save(image_output + "/{0}".format(output_imagename))
