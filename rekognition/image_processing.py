from PIL import Image
import os
import datetime
from config_handler import config

def create_crop(original_image, bounding_box, filename):
    crop_image_url = None
    width_px = original_image.size[0]
    height_px = original_image.size[1]

    top = bounding_box.get('Top', 0.0) * 1.0
    left = bounding_box.get('Left', 0.0) * 1.0
    width = bounding_box.get('Width', 0.0) * 1.0
    height = bounding_box.get('Height', 0.0) * 1.0

    if top < 0.0:
        top = 0.0
    if left < 0.0:
        left = 0.0

    left_px =  left * width_px
    top_px =  top * height_px

    dx_px = width * width_px
    dy_px = height * height_px

    right_px = left_px + dx_px
    bottom_px = top_px + dy_px

    crop_image = original_image.crop((
        int(left_px), int(top_px), int(right_px), int(bottom_px)))
    print('Saving: %s' % filename)
    crop_image.save(filename)
    crop_image_url = filename
    return crop_image_url

def create_face_crops(original_image_url, face_details):
    face_images_urls = []
    original_image = Image.open(original_image_url)
    now_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
    tmp_folder = config.get('rekognition', 'tmp_folder', fallback='')
    for k, face_detail in enumerate(face_details):
        filename = '%s%s_%s.jpg' % (tmp_folder, now_str, str(k))
        detected_face_image = create_crop(original_image, face_detail.get('BoundingBox'), filename)
        face_images_urls.append(detected_face_image)
    return face_images_urls

def delete_picture_file(file_url):
    print('Deleting: %s' %file_url)
    os.remove(file_url)
    return

def delete_picture_files(file_urls):
    for file_url in file_urls:
        delete_picture_file(file_url)
    return