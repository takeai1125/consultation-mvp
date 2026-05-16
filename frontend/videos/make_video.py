from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio.v2 as imageio
import numpy as np

# ------------------------
# SETTINGS
# ------------------------

width, height = 1080, 1920
fps = 24
seconds_per_slide = 5

slides = [
    "なんとなく\n疲れてしまう日って\nありますよね",
    
    "ちゃんとしなきゃ\nと思うほど、\n苦しくなる時もあります",
    
    "「ひと休み相談室」は\n少し気持ちを整理したい時に\n使える場所です",
    
    "うまく言葉に\nできなくても\n大丈夫です",
    
    "LINEから\nご相談できます\nプロフィールURLからどうぞ"
]

out_path = "hitoyasumi_short.mp4"

# ------------------------
# FONT
# ------------------------

# FONT
font = ImageFont.truetype(
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    66
)

small_font = ImageFont.truetype(
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    40
)

# ------------------------
# BACKGROUND
# ------------------------

bg = Image.open(
    "frontend/videos/assets/forest.jpg"
).convert("RGB")

bg = bg.resize((width, height))
bg = bg.filter(ImageFilter.GaussianBlur(1))

frames = []

# ------------------------
# CREATE SLIDES
# ------------------------

for i, text in enumerate(slides):

    img = bg.copy()

    # 背景を少しやわらかく
    soft_overlay = Image.new(
        "RGBA",
        (width, height),
        (225, 245, 240, 65)
    )
    img.paste(soft_overlay, (0, 0), soft_overlay)

    draw = ImageDraw.Draw(img)

    bbox = draw.multiline_textbbox(
        (0, 0),
        text,
        font=font,
        spacing=24
    )

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w) // 2
    y = (height - text_h) // 2

    # 文字の後ろに半透明の丸いカード
    padding_x = 70
    padding_y = 55

    card_x1 = x - padding_x
    card_y1 = y - padding_y
    card_x2 = x + text_w + padding_x
    card_y2 = y + text_h + padding_y

    card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)

    card_draw.rounded_rectangle(
        (card_x1, card_y1, card_x2, card_y2),
        radius=48,
        fill=(255, 255, 255, 170)
    )

    img = Image.alpha_composite(img.convert("RGBA"), card)
    draw = ImageDraw.Draw(img)

    # 影はかなり薄く
    draw.multiline_text(
        (x + 2, y + 2),
        text,
        font=font,
        fill=(130, 160, 150, 120),
        align="center",
        spacing=24
    )

    # メイン文字：緑〜青に映える落ち着いた深緑
    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill=(45, 95, 85),
        align="center",
        spacing=24
    )

    # 最後のスライドだけ補足
    if i == len(slides) - 1:

        sub = "LINE追加後、気軽にご相談ください"

        sbbox = draw.textbbox(
            (0, 0),
            sub,
            font=small_font
        )

        sw = sbbox[2] - sbbox[0]

        draw.text(
            ((width - sw)//2, card_y2 + 50),
            sub,
            font=small_font,
            fill=(65, 120, 110)
        )

    frame = np.array(img.convert("RGB"))
# ------------------------
# EXPORT
# ------------------------

imageio.mimsave(
    out_path,
    frames,
    fps=fps
)

import os
print("Saved video to:", os.path.abspath(out_path))