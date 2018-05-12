import json
import sys
import argparse
from PIL import Image, ImageDraw
from ast import literal_eval

class Palette:
    def __init__(self, palette_dict, screen_dict):
        self.colors = palette_dict
        
        self.default_color = self.color_decoder(screen_dict['fg_color'])
  
    def get_color(self, input_dict):

        if 'color' in input_dict.keys():
            return self.color_decoder(input_dict['color'])
        
        elif 'bg_color' in input_dict.keys():
            return self.color_decoder(input_dict['bg_color'])
        
        else:
            return self.default_color
        
    def color_decoder(self, color):
        
        if color[0] == '#':
            return color
        
        if color[0] == '(':
            return literal_eval(color)
        
        else: 
            return self.colors[color]


class Figure_factory:
    @staticmethod
    def get_figure(figure_dict, palette):
        figure_type = figure_dict['type']
        
        if figure_type == 'point':
            return Point(figure_dict, palette)
        
        elif figure_type == 'polygon':
            return Polygon(figure_dict, palette)
        
        elif figure_type == 'square':
            return Square(figure_dict, palette)
        
        elif figure_type == 'rectangle':
            return Rectangle(figure_dict, palette)
        
        elif figure_type == 'circle':
            return Circle(figure_dict, palette)
        
        else:
            return None

        
class Point:
    def __init__(self, point_dict, palette):
        self.x = point_dict['x']
        self.y = point_dict['y']
        self.color = palette.get_color(point_dict)
        
    def draw(self, drawer):
        drawer.point((self.x, self.y), self.color)

        
class Polygon:
    def __init__(self, polygon_dict, palette):
        self.points = [tuple(i) for i in polygon_dict['points']]
        self.color = palette.get_color(polygon_dict)
        
    def draw(self, drawer):
        drawer.polygon(self.points,  self.color)

        
class Rectangle:
    def __init__(self, rectangle_dict, palette):
        self.x = rectangle_dict['x']
        self.y = rectangle_dict['y']
        self.height = rectangle_dict['height']
        self.width = rectangle_dict['width']
        self.color = palette.get_color(rectangle_dict)
        
    def draw(self, drawer):
        drawer.rectangle(xy = [(self.x, self.y), 
                            (self.x + self.height, self.y + self.width)], 
                      fill = self.color)

        
class Square:
    def __init__(self, square_dict, palette):
        self.x = square_dict['x']
        self.y = square_dict['y']
        self.size = square_dict['size']
        self.color = palette.get_color(square_dict)
           
    def draw(self, drawer):
        drawer.rectangle(xy = [(self.x, self.y), 
                            (self.x + self.size, self.y + self.size)], 
                      fill = self.color)

        
class Circle:
    def __init__(self, circle_dict, palette):
        self.center_x = circle_dict['x']
        self.center_y = circle_dict['y']
        self.radius = circle_dict['radius']
        self.color = palette.get_color(circle_dict)
        
        
    def draw(self, drawer):
        drawer.pieslice(xy = [(self.center_x - self.radius, self.center_y - self.radius), 
                            (self.center_x + self.radius, self.center_y + self.radius)], 
                      start = 0, 
                      end = 360, 
                      fill = self.color)

class Drawing:
    def __init__(self, input_file):
        
        with open(input_file) as json_data:
            self.input_dict = json.load(json_data)
        
        self.palette = Palette(self.input_dict['Palette'], self.input_dict['Screen'])
        
        self.screen_height = self.input_dict['Screen']['height']
        self.screen_width = self.input_dict['Screen']['width']
         
        self.screen_color = self.palette.get_color(self.input_dict['Screen'])
        
        self.screen = Image.new('RGB', (self.screen_width, self.screen_height), self.screen_color)
        
        self.drawer = ImageDraw.Draw(self.screen)
        
        self.figures = [Figure_factory.get_figure(i, self.palette) for i in self.input_dict['Figures']]
        
    def draw(self):
        for figure in self.figures:
            figure.draw(self.drawer)
            
    def show(self):
        self.screen.show()
        
    def save(self, file_name):
        self.screen.save(file_name)
    



def main():
    parser = argparse.ArgumentParser(description="Draw an image from a json file and save it")
    parser.add_argument("input", help="input json image file", type=str)
    parser.add_argument("output", help="name of a file with a proper extension", type=str)
    args = parser.parse_args()

    drawer = Drawing(args.input)
    drawer.draw()
    drawer.show()
    drawer.save(args.output)

if __name__ == "__main__":  
    main()