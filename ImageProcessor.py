from PIL import ImageGrab, Image
import pytesseract


class ImageProcessor:
    def __init__(self):
        pass

    def process_image(self, canvas):
        x = canvas.winfo_rootx() + canvas.winfo_x()
        y = canvas.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()

        image = ImageGrab.grab().crop((x, y, x1, y1))

        text = pytesseract.image_to_string(image, lang='eng')

        return text
