import qrcode
from PIL import ImageFont, ImageDraw

import io
import zipfile


def generate_qr_code(url: str, invite_code: str):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=12,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Monaco", 64)

    draw.text((200, 550), invite_code, (0, 0, 0), font=font)

    return img


def zip_images(images: list[dict]):
    """
    :param images: Images to zip, format [{name: str, image: Image}]
    :return: zipped images
    """
    temp_file = io.BytesIO()
    # temp_file = "sample.zip"
    with zipfile.ZipFile(temp_file, "w", zipfile.ZIP_DEFLATED) as file:
        for image in images:
            img_byte_arr = io.BytesIO()
            image["image"].save(img_byte_arr, format="PNG")
            file.writestr(f"{image['name']}.png", img_byte_arr.getvalue())

    return temp_file.getvalue()
