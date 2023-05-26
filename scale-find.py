import cv2
import numpy as np
from tkinter import filedialog, simpledialog
from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont


def upload_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def select_reference(image):
    reference_points = []
    cv2.namedWindow("Select Reference Point")
    cv2.imshow("Select Reference Point", image)
    cv2.setMouseCallback("Select Reference Point", lambda event,
                         x, y, flags, param: reference_points.append((x, y)))
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    return reference_points


def input_scale():
    root = Tk()
    root.withdraw()
    actual_scale = simpledialog.askfloat(
        "Input Scale", "Enter the actual scale in metric system:")
    unit = simpledialog.askstring(
        "Input Scale", "Enter the unit of the scale (mm, cm, meter):")
    return actual_scale, unit


def generate_scale(image, reference_points, actual_scale, unit):
    font = ImageFont.truetype("arial.ttf", size=20)
    scale_width = int(0.1 * image.shape[1])
    scale_height = int(0.02 * image.shape[0])
    scale_image = Image.fromarray(image)
    draw = ImageDraw.Draw(scale_image)
    if unit == "mm":
        pixel_per_unit = actual_scale / \
            (reference_points[1][0] - reference_points[0][0])
        scale_text = "{} mm".format(int(actual_scale))
    elif unit == "cm":
        pixel_per_unit = (actual_scale / 10) / \
            (reference_points[1][0] - reference_points[0][0])
        scale_text = "{} cm".format(actual_scale)
    elif unit == "meter":
        pixel_per_unit = (actual_scale * 100) / \
            (reference_points[1][0] - reference_points[0][0])
        scale_text = "{} meter".format(actual_scale)
    else:
        raise ValueError("Invalid unit")
    scale_length = int(actual_scale / pixel_per_unit)
    draw.rectangle(((10, image.shape[0] - scale_height - 10), (10 +
                   scale_length, image.shape[0] - 10)), outline='white', width=2)
    draw.text((10, image.shape[0] - scale_height - 30),
              scale_text, font=font, fill='white')
    scale_image = np.array(scale_image)
    return scale_image


def main():
    image_path = upload_image()
    image = cv2.imread(image_path)
    reference_points = select_reference(image)
    actual_scale, unit = input_scale()
    scale_image = generate_scale(image, reference_points, actual_scale, unit)
    cv2.imshow("Scaled Image", scale_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("scaled_image.jpg", scale_image)


if __name__ == "__main__":
    main()
