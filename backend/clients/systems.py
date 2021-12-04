import base64

from PIL import Image
from django.core.mail import send_mail

from math import sin, cos, radians, degrees, acos


def calc_dist(lat_a, long_a, lat_b, long_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    return degrees(acos(distance)) * 69.09


def add_watermark(input_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open('watermark.jpg')
    base_image.paste(watermark, (0, 0))
    base_image.save(str(input_image_path))
    with open(str(input_image_path), 'rb') as file:
        picture = base64.b64encode(file.read()).decode()
    return picture


def send(client, like_client):
    send_mail(
        'Знакомство',
        f'Вы понравились пользователю - {client.first_name}, {client}',
        'tinderonline12345@gmail.com',
        [like_client],
        fail_silently=False,
    )
