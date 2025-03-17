from fastapi import APIRouter, Response
from captcha.image import ImageCaptcha
import random
from io import BytesIO

router = APIRouter()
captcha = ImageCaptcha()


# Generate a random captcha code
def generate_captcha():
    return ''.join(random.choices('0123456789', k=4))


# Store captcha code and its corresponding solution
captcha_store = {}


@router.get("/captcha")
async def get_captcha():
    captcha_code = generate_captcha()
    captcha_image = captcha.generate(captcha_code)
    captcha_store[captcha_code] = captcha_code.lower()

    # Convert image to bytes
    image_bytes = BytesIO()
    image_bytes.write(captcha_image.getvalue())
    image_bytes.seek(0)

    return Response(content=image_bytes.read(), media_type="image/png")
