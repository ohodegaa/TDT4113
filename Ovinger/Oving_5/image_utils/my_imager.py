__author__ = 'ohodegaa'

from image_utils import imager2
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance

class MyImager(imager2.Imager):

    def make_fancy_colors(self, image="images/arduino.jpeg"):
        im1 = imager2.Imager(image)
        im2 = im1.map_color_wta(thresh=0.25)
        im2.display()

    def make_fancy_and_tunnel(self, image="images/einstein.jpeg"):
        im1 = imager2.Imager(image)
        im2 = im1.map_color_wta(thresh=0.1)
        im3 = im2.tunnel(levels=10, scale=0.80)
        im3.display()

    def find_edges(self, image="images/einstein.jpeg"):
        im1 = Image.open(image)
        im_edges = im1.filter(ImageFilter.FIND_EDGES)
        im2 = imager2.Imager(image=im_edges)
        im2.display()

    def tunnel_max(self,image="images/einstein.jpeg"):
        im1 = imager2.Imager(image)
        im1.tunnel(levels=900, scale=0.75)
        im1.display()


    def sharpen(self, image="images/robot.jpeg", sharpness_factor=50.0):
        im1 = Image.open(image)
        enhancer = ImageEnhance.Sharpness(im1)
        enhancer.enhance(sharpness_factor).show()

    def contrast(self, image="images/einstein.jpeg", contrast_factor=50.0):
        im1 = Image.open(image)
        enhancer = ImageEnhance.Contrast(im1)
        enhancer.enhance(contrast_factor).show()


def main():
    cool_pic = MyImager()
    cool_pic.make_fancy_colors()
    cool_pic.make_fancy_and_tunnel()
    cool_pic.sharpen()
    cool_pic.tunnel_max()
    cool_pic.contrast()
if __name__ == '__main__':
    main()