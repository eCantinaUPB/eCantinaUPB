import numpy as np
from PIL import Image
import cv2
from common.options import opts


class Separator:
    @staticmethod
    def process_image(image: Image) -> np.array:
        gray_img = image.convert("L")
        gray_img.thumbnail((opts["sep_res"], opts["sep_res"]))
        np_img = np.array(gray_img)
        np_img = cv2.convertScaleAbs(
            np_img, alpha=opts["sep_alpha"], beta=opts["sep_beta"]
        )
        np_img = cv2.GaussianBlur(
            np_img,
            (opts["sep_gauss_ker_size"], opts["sep_gauss_ker_size"]),
            opts["sep_gauss_sigma"],
        )
        return np_img

    @staticmethod
    def interrogate_image(target: np.array) -> list:
        return cv2.HoughCircles(
            target,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=opts["sep_hough_mindist"],
            param1=opts["sep_canny_max"],
            param2=opts["sep_hough_cen"],
            minRadius=opts["sep_hough_minr"],
            maxRadius=opts["sep_hough_maxr"],
        )

    @staticmethod
    def get_images(source: Image) -> list:
        sep_images: list = []
        sep_source = Separator.process_image(source)
        ratio = (
            source.size[0] / sep_source.shape[1] + source.size[1] / sep_source.shape[0]
        ) / 2
        circles = Separator.interrogate_image(sep_source)
        image = source.convert("RGB")
        image = np.array(image)
        if circles is not None:
            for x, y, r in np.round(circles[0, :]).astype("int"):
                if (
                    x - r < 0
                    or y - r < 0
                    or x + r > sep_source.shape[1]
                    or y + r > sep_source.shape[0]
                ):
                    continue
                x_sc = int(x * ratio)
                y_sc = int(y * ratio)
                r_sc = int(r * ratio)
                sep_images.append(
                    Image.fromarray(
                        image[y_sc - r_sc : y_sc + r_sc, x_sc - r_sc : x_sc + r_sc, :]
                    ).resize((opts["storage_img_res"], opts["storage_img_res"]))
                )

        return sep_images
