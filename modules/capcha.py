from PIL import Image, ImageFont, ImageDraw, ImageQt
from io import StringIO
import random
from PyQt5 import QtGui


def create_capcha():
    key = ''
    char_numbers = '1234567890'
    num_count = 0
    chars_lc = 'abcdefghijklnopqrstuvwxyz'
    chars_lc_count = 0
    current_char_count = 0
    chars = 'QWERTYUIOPLKJHGFDSAZXCVBNMabcdefghijklnopqrstuvwxyz1234567890'
    chars_count = random.randint(5, 10)
    pallete_5 = [(255, 0, 0), (255, 255, 0), (0, 128, 0), (0, 255, 255), (75, 0, 130)]
    pallete_15 = [
        (255, 0, 0),
        (255, 255, 0),
        (0, 128, 0),
        (0, 255, 255),
        (75, 0, 130),
        (255, 215, 0),
        (0, 250, 154),
        (72, 209, 204),
        (30, 144, 255),
        (138, 43, 226),
        (255, 0, 255),
        (240, 128, 128),
        (255, 160, 122),
        (255, 218, 185),
        (0, 0, 0)
    ]

    background = random.choice(pallete_15)
    pallete_15.remove(background)
    try:
        pallete_5.remove(background)
    except:
        pass
    for i in range(chars_count):
        if num_count < 1:
            key += random.choice(char_numbers)
            num_count += 1
            current_char_count += 1
        if chars_lc_count < 1:
            key += random.choice(chars_lc)
            current_char_count += 1
            chars_lc_count += 1

    if current_char_count < chars_count:
        for current_char_count in range(chars_count):
            key += random.choice(chars)
    else:
        key += random.choice(chars)

    key = ''.join(random.sample(key, len(key)))

    img = Image.new('RGB', (100, 50), '#%02x%02x%02x' % background)
    draw = ImageDraw.Draw(img)

    for i in range(100):
        draw.point((random.randint(0, 100), random.randint(0, 50)), fill=(255, 255, 255, 255))

    font = ImageFont.truetype('C:\\Windows\\Fonts\\arial.ttf', 15)

    text_color = random.choice(pallete_5)
    draw.text((0, random.randint(0, 35)), key, font=font, fill=(text_color))

    pallete_5.remove(text_color)
    pallete_15.remove(text_color)

    for i in range(5):
        line_color = random.choice(pallete_5)
        try:
            pallete_15.remove(line_color)
        except:
            pass
        draw.line([(random.randint(0, 100), random.randint(0, 50)),
                   (random.randint(0, 100), random.randint(0, 50))],
                  fill=line_color)

    img = img.convert("RGBA")
    QtImage = ImageQt.ImageQt(img)
    # QtImage = Image.open()
    pixmap = QtGui.QPixmap.fromImage(QtImage)

    return key, pixmap
