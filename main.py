import datetime
import sys
from enum import Enum

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime
import os


class LoadingBar:

    def __init__(self, goal):
        self.__starttime = datetime.now()
        self.__goal = goal
        self.__current_status = 1

    def update(self):
        if self.__current_status > self.__goal:
            raise IndexError('More elements than expected found!')
        print('\r' + self.print_status(self.__current_status), end='', flush=True)
        self.__current_status = self.__current_status + 1
        sys.stdout.flush()

    def print_status(self, status):
        bar_str = '=' * status + '-' * int(self.__goal - status) + '> : ' + str(status) + '/' + str(self.__goal)
        return bar_str


def create_a4_page_with_images(image_paths, output_pdf, card_format):
    # Create a canvas object with the specified output PDF file and page size
    c = canvas.Canvas(output_pdf, A4)
    A4_WIDTH, A4_HEIGHT = A4
    if card_format.value == CardFormat.YUGIOH.value:
        CARD_WIDTH, CARD_HEIGHT = get_ygo_card_size_as_points()
    elif card_format.value == CardFormat.MAGIC.value:
        CARD_WIDTH, CARD_HEIGHT = get_mtg_card_size_as_points()
    else:
        raise ValueError(f"No Card Format found for Card Format Enum {card_format}")

    xpadding = int((A4_WIDTH - (3 * CARD_WIDTH)) / 2)
    ypadding = int((A4_HEIGHT - (3 * CARD_HEIGHT)) / 2)
    x, y = xpadding, ypadding
    img_num = len(image_paths)
    bar = LoadingBar(img_num)

    for i in range(img_num):
        if x + CARD_WIDTH > A4_WIDTH - xpadding:
            x = xpadding
            y += CARD_HEIGHT

        if y + CARD_HEIGHT > A4_HEIGHT - ypadding:  # when page is full of cards
            c.showPage()
            x, y = xpadding, ypadding

        c.drawImage(image_paths[i], x, y, width=CARD_WIDTH, height=CARD_HEIGHT)
        bar.update()
        x += CARD_WIDTH

    c.save()
    return 0


def get_mtg_card_size_as_points():
    card_width = 63 * mm
    card_height = 88 * mm
    return card_width, card_height


def get_ygo_card_size_as_points():
    card_width = 59 * mm
    card_height = 86 * mm
    return card_width, card_height


class CardFormat(Enum):
    MAGIC = 1
    YUGIOH = 2


def main(image_folder, output_pdf, card_format):
    image_paths = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder) if
                   fname.endswith(('png', 'jpg', 'jpeg'))]

    # Create the A4 page with the images
    status = create_a4_page_with_images(image_paths, output_pdf, card_format)


if __name__ == '__main__':
    folder_path = '/home/wiliam/Documents/MTG Decks/chishiro addons'  # path to directory holding image files
    pdf_path = 'resource/addons.pdf'  # path where the finished pdf file will be stored
    main(folder_path, pdf_path, CardFormat.MAGIC)
