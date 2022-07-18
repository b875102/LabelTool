# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 21:55:02 2022

@author: HUANG Chun-Huang
"""

import sys
from PIL import Image, ImageDraw, ImageFont

class Road():
    
    sections = ['North', 'East', 'South', 'West']
    directions = ['In', 'Out']
    
    __rotation_north = 90
    __rotation_east = 0
    __rotation_south = 90
    __rotation_west = 0
    
    __lane_width = 40
    __lane_length = 120
    
    __line_width = 4
    
    __road_offset = 4
    
    __color_background = (159, 159, 159)
    __color_road = (127, 127, 127)
    
    __color_black = (0, 0, 0)
    __color_white = (255, 255, 255)
    __color_yellow = (255, 192, 0)
    __color_amber = (255, 191, 0)
    __color_chartreuse = (223, 255, 0)
    
    __dotted_line = [12, 24, 12, 24, 12, 24, 12]
    __dotted_color = [__color_road, __color_white]
    
    def __init__(self):
        
        self.link_id = ''
        self.name = ''
        self.lane_num = ''
        self.section = ''
        self.direction = ''
        
    @classmethod
    def laneLength(cls):
        return cls.__lane_length
    
    @classmethod
    def laneWidth(cls, center = False):
        ln = cls.__lane_width
        if center:
            ln /= 2        
        return int(ln)
        
    @classmethod
    def roadOffset(cls):
        return cls.__road_offset
    
    @classmethod
    def backgroundColor(cls):
        return cls.__color_background
    
    @classmethod
    def roadColor(cls):
        return cls.__color_road
    
    def laneNum(self):
        return int(self.lane_num)
        
    def __baseImg(self, onewayroad):
        
        lane_num = self.laneNum()
        inner_h = self.__lane_width * lane_num
        
        offset_y = 0
        
        if self.section in ['North', 'East']:
            if self.direction == 'Out':
                swap = True
            elif self.direction == 'In':
                swap = False
        elif self.section in ['South', 'West']:
            if self.direction == 'Out':
                swap = False
            elif self.direction == 'In':
                swap = True
            
        if swap:
            offset_y = self.__road_offset
            xy_outer = (0, inner_h, self.__lane_length, inner_h)
            xy_inner = (0, offset_y, self.__lane_length, offset_y)
        else:
            xy_outer = (0, 0, self.__lane_length, 0)
            xy_inner = (0, inner_h, self.__lane_length, inner_h)
            
        outer = xy_outer, (self.__color_white), self.__line_width
        
        if onewayroad:
            inner = xy_inner, (self.__color_white), self.__line_width
        else:
            inner = xy_inner, (self.__color_yellow), self.__line_width
        
        lines = []
        lines.extend([outer, inner])
        
        dotteds = lane_num - 1
        for didx in range(dotteds):
            d_h = self.__lane_width * (didx + 1)
            
            for midx, masklen in enumerate(self.__dotted_line):
                
                s_w = sum(self.__dotted_line[0: midx])
                e_w = sum(self.__dotted_line[0: midx + 1])
                cidx = (midx % 2)
                
                dottedmask = (s_w, d_h, e_w, d_h), (self.__dotted_color[cidx]), self.__line_width
                lines.append(dottedmask)
                
        if self.direction == 'In':
            if self.section in ['North', 'East']:
                stop = (0, 0, 0, inner_h), self.__color_white, self.__line_width * 3
            elif self.section in ['South', 'West']:
                x = self.__lane_length - self.__line_width
                stop = (x, offset_y, x, inner_h), self.__color_white, self.__line_width * 3
            
            lines.append(stop)
                
        w, h = self.__lane_length, inner_h + self.__road_offset
        img = Image.new('RGB', (w, h))
        
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, w, h), fill = Road.roadColor())
            
        for line in lines:
            xy, color, width = line
            draw.line(xy, fill = color, width = width)
        
        return img
    
    def getImg(self, onewayroad):
        
        img = self.__baseImg(onewayroad)
        draw = ImageDraw.Draw(img)
        
        xy1 = (12, 12)
        xy2 = (12, 24)
        
        if sys.platform == 'win32':
            font = ImageFont.truetype('mingliu.ttc', 12)
        else:
            font = ImageFont.truetype('NotoSansCJK-Regular.ttc', 12)

        draw.text(xy1, self.link_id, font = font)
        draw.text(xy2, self.name, font = font)
        
        if self.section == 'North':
            img = img.rotate(self.__rotation_north, expand = True)
        elif self.section == 'South':
            img = img.rotate(self.__rotation_south, expand = True)
            
        return img
    
if __name__ == '__main__':
    
    road = Road()
    road.link_id = 'C0058001'
    road.name = 'xxxxxx'
    road.lane_num = '1'
    road.section = 'West'
    road.direction = 'In'
    
    img = road.getImg(False)
    img.show()
    print('done')