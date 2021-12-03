from PIL import Image
from django.core.mail import send_mail


def add_watermark(input_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open('watermark.jpg')
    base_image.paste(watermark, (0, 0))
    base_image.save(str(input_image_path))
    return base_image


def send(client, like_client):
    send_mail(
        'Знакомство',
        f'Вы понравились пользователю - {client.first_name}, {client}',
        'tinderonline12345@gmail.com',
        [like_client],
        fail_silently=False,
    )
