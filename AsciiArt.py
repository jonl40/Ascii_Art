# https://www.youtube.com/watch?v=v_raWlX7tZY
# http://paulbourke.net/dataformats/asciiart/

# Font used is Consolas size 16 on windows 10 Command Prompt 
#FONT = ImageFont.truetype('C:/Windows/Fonts/Consolas/consola.ttf', 16)

from PIL import Image, ImageOps, ImageFont
from math import floor 
import os 
import sys 

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)

# In grayscale 0 is black 255 is white 
# darkest to lightest
# black -> white 
ASCII_CHARS = ['@','%','#','*','+','=','-',':','.',' ']
#ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
MAX_GRAYSCALE = 255
ASCII_HEIGHT_WIDTH_RATIO = 2
ASCII_ART_FILENAME = 'ascii_image.txt'


class Image2Ascii:
    def __init__(self, image_name, new_width=100):
        self.image_name = image_name
        self.new_width = new_width
        self.new_height = None 
        self.resized_image = None 
        self.grayscaled_image = None 
        self.ascii_image = None 

    #Resize image and keep aspect ratio 
    def ResizeImage(self):
        try:
            img = Image.open(self.image_name)
            width, height = img.size
            aspect_ratio = width/height
            ascii_ratio = aspect_ratio * ASCII_HEIGHT_WIDTH_RATIO 
            self.new_height = int(self.new_width/ascii_ratio)
            new_size = (self.new_width,self.new_height)
            self.resized_image = img.resize(new_size)

            #print('aspect ratio: {}'.format(aspect_ratio))
            #print('width: {}\nheight: {}'.format(width, height))
            #print('new_width: {}\nnew_height: {}'.format(self.new_width, self.new_height))
            #self.resized_image.show()

        except Exception as e:
            print('Failed to open image: {}\n'.format(self.image_name))
            print(e)
            sys.exit(-1)
    

    #grayscale resized image   
    def GrayScale(self):
        self.grayscaled_image = ImageOps.grayscale(self.resized_image)
        #self.grayscaled_image.show()


    #replace grayscale values with ascii chars
    def Pixel2Ascii(self):
        ctr = 0 
        row = []
        ascii_array = []

        self.ResizeImage()
        self.GrayScale()
        pixels = list(self.grayscaled_image.getdata())
        
        for pixel in pixels:
            gray_level = floor(pixel * (len(ASCII_CHARS) / (MAX_GRAYSCALE+1)))
            row.append(ASCII_CHARS[gray_level])
            ctr += 1 

            if ctr == self.new_width:
                ascii_array.append(''.join(row))
                row = []
                ctr = 0

        self.ascii_image = '\n'.join(ascii_array)
        print(self.ascii_image)

        try:
            with open(ASCII_ART_FILENAME,'w') as f:
                f.write(self.ascii_image)
        except Exception as e:
            print(e)
            sys.exit(-1)


def DisplayAscii(filename, width=100):
    ASCII = Image2Ascii(filename, width)
    ASCII.Pixel2Ascii()
    print('\n\n')
        

DisplayAscii('image/banana.png', 100)
DisplayAscii('image/lime.png', 75)
DisplayAscii('image/lena.png', 150)
DisplayAscii('image/rocket.png', 90)
DisplayAscii('image/uorocketry.png')