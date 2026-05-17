from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio.v2 as imageio
import numpy as np
from pathlib import Path

# =====================
# 基本設定
# =====================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_PATH = BASE_DIR / "output_hitoyasumi.mp4"

WIDTH = 1080
HEIGHT = 1920
FPS = 24
SECONDS_PER_SLIDE = 5

# 背景画像
BACKGROUND_IMAGE = ASSETS_DIR / "forest.jpg"

slides = [
    "なんとなく\n疲れてしまう日って\nありますよね",

    "ちゃんとしなきゃ\nと思うほど、\n苦しくなる時もあります",

    "「ひと休み相談室」は\n少し気持ちを整理したい時に\n使える場所です",

    "うまく言葉に\nできなくても\n大丈夫です",

    "まずは、\n今の気持ちを\n書けるところから",

]

# =====================
# フォント設定
# =====================
FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]

font_path = None

for path in FONT_PATHS:
    if Path(path).exists():
        font_path = path
        break

if font_path is None:
    raise FileNotFoundError(
        "日本語フォントが見つかりません"
    )

font = ImageFont.truetype(font_path, 72)
small_font = ImageFont.truetype(font_path, 42)

# =====================
# 背景生成
# =====================
def create_background():

    if BACKGROUND_IMAGE.exists():

        bg = Image.open(BACKGROUND_IMAGE).convert("RGB")
        bg = bg.resize((WIDTH, HEIGHT))
        bg = bg.filter(ImageFilter.GaussianBlur(1.5))

        return bg

    # 背景画像がない場合
    bg = Image.new("RGB", (WIDTH, HEIGHT), (225, 242, 235))

    draw = ImageDraw.Draw(bg)

    draw.ellipse(
        (-180, -120, 420, 480),
        fill=(190, 225, 210)
    )

    draw.ellipse(
        (760, 1350, 1260, 1900),
        fill=(185, 220, 215)
    )

    draw.ellipse(
        (120, 1450, 420, 1750),
        fill=(205, 232, 220)
    )

    return bg

# =====================
# 動画生成
# =====================
frames = []

for index, text in enumerate(slides):

    bg = create_background().convert("RGBA")

    # 背景を少し淡く
    soft_layer = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (230, 245, 240, 95)
    )

    bg = Image.alpha_composite(bg, soft_layer)

    draw = ImageDraw.Draw(bg)

    bbox = draw.multiline_textbbox(
        (0, 0),
        text,
        font=font,
        spacing=30,
        align="center",
    )

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (WIDTH - text_w) // 2
    y = (HEIGHT - text_h) // 2

    # 半透明カード
    padding_x = 90
    padding_y = 70

    card_x1 = max(60, x - padding_x)
    card_y1 = y - padding_y
    card_x2 = min(WIDTH - 60, x + text_w + padding_x)
    card_y2 = y + text_h + padding_y

    card = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    card_draw = ImageDraw.Draw(card)

    card_draw.rounded_rectangle(
        (card_x1, card_y1, card_x2, card_y2),
        radius=60,
        fill=(255, 255, 255, 185),
    )

    bg = Image.alpha_composite(bg, card)

    draw = ImageDraw.Draw(bg)

    # 影
    draw.multiline_text(
        (x + 2, y + 2),
        text,
        font=font,
        fill=(120, 150, 145, 120),
        align="center",
        spacing=30,
    )

    # 本文
    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill=(38, 92, 82),
        align="center",
        spacing=30,
    )

    # 最後だけ補足
    if index == len(slides) - 1:

        sub_text = "プロフィールURLからどうぞ"

        sub_bbox = draw.textbbox(
            (0, 0),
            sub_text,
            font=small_font
        )

        sub_w = sub_bbox[2] - sub_bbox[0]

        draw.text(
            ((WIDTH - sub_w) // 2, card_y2 + 60),
            sub_text,
            font=small_font,
            fill=(55, 115, 105),
        )

    frame = np.array(bg.convert("RGB"))

    for _ in range(FPS * SECONDS_PER_SLIDE):
        frames.append(frame)

# =====================
# 保存
# =====================
imageio.mimsave(
    OUTPUT_PATH,
    frames,
    fps=FPS,
    macro_block_size=1
)

print("Saved video to:")
print(OUTPUT_PATH.resolve())