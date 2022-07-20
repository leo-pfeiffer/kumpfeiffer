import qrcode
from PIL import ImageFont, ImageDraw, Image

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

    draw.text((170, 460), invite_code, (0, 0, 0), font=font)

    # img.save(f"{invite_code}.png")
    return img


def zip_images(images: list[(str, Image)]):
    # temp_file = io.BytesIO()
    temp_file = "sample.zip"
    with zipfile.ZipFile(temp_file, "w", zipfile.ZIP_DEFLATED) as file:
        for name, image in images:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            file.writestr(f"{name}.png", img_byte_arr.getvalue())


img1 = generate_qr_code("My Silly Test", "abc")
img2 = generate_qr_code("My Silly Test", "def")
img3 = generate_qr_code("My Silly Test", "ghi")

zip_images([("img1", img1), ("img2", img2), ("img3", img3)])
