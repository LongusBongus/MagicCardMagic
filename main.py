import datetime
import sys

from reportlab.pdfgen import canvas
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
        print('\r'+self.print_status(self.__current_status), end='', flush=True)
        self.__current_status = self.__current_status + 1
        sys.stdout.flush()

    def print_status(self, status):
        bar_str = '=' * status + '-' * int(self.__goal - status) + '> : ' + str(status) + '/' + str(self.__goal)
        return bar_str


def create_a4_page_with_images(image_paths, output_pdf, page_size=(2480, 3508)):
    # Create a canvas object with the specified output PDF file and page size
    c = canvas.Canvas(output_pdf, page_size)
    A4_WIDTH, A4_HEIGHT = page_size
    CARD_WIDTH, CARD_HEIGHT = get_card_size(A4_WIDTH, A4_HEIGHT)

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


def get_card_size(canvas_width, canvas_height):  # expected a A4 format
    card_width = int((canvas_width / 210) * 63)
    card_height = int((canvas_height / 297) * 88)
    return card_width, card_height


def main(image_folder, output_pdf):
    image_paths = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder) if
                   fname.endswith(('png', 'jpg', 'jpeg'))]

    # Create the A4 page with the images
    status = create_a4_page_with_images(image_paths, output_pdf)


if __name__ == '__main__':
    folder_path = ''    # path to directory holding image files
    pdf_path = ''       # path where the finished pdf file will be stored
    main(folder_path, pdf_path)
