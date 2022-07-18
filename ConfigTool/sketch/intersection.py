# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 21:54:23 2022

@author: HUANG Chun-Huang
"""

import sys
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont
from ConfigTool.sketch.road import Road

class Intersection():
    
    def __init__(self):
        
        self.name = ''
        self.version = ''
        self.date = ''
        self.intersection_id = ''
        self.road_type = ''
        self.road_num = ''
        self.pd = None
        
    def generate(self, path, save = False, inTrack = '', outTrack = ''):
        
        def shiftC(cTuple, s):
            inC = cTuple[0]
            outC = cTuple[1]
            if inC:
                inC = [ c + s for c in inC]
            if outC:
                outC = [ c + s for c in outC]
            return (inC, outC)
            
        sdict = {}
        wdict = {}
        cdict = {}
        
        for section in Road.sections:
            
            inRoad = None
            outRoad = None
            
            for direction in Road.directions:
                
                roadpd = self.pd[(self.pd['section'] == section) & (self.pd['direction'] == direction)]
                roadpd.reset_index(drop = True, inplace = True)
                
                if roadpd.shape[0] > 0:
                    
                    road = Road()
                    road.link_id = str(roadpd.loc[0]['link_id'])
                    road.name = str(roadpd.loc[0]['name.1'])
                    road.lane_num = roadpd.loc[0]['lane_num']
                    road.section = roadpd.loc[0]['section']
                    road.direction = roadpd.loc[0]['direction']
                    
                    if direction == Road.directions[0]:
                        inRoad = road
                    elif direction == Road.directions[1]:
                        outRoad = road
            
            if (inRoad or outRoad):
                img, onewayroad, cio = self.__getImg(section, inRoad, outRoad)
                sdict[section] = img
                wdict[section] = onewayroad
                cdict[section] = cio
            
        cw = max([sdict[section].size[0] for section in sdict if section in ['North', 'South']])
        ch = max([sdict[section].size[1] for section in sdict if section in ['East', 'West']])
        cw2 = cw // 2
        ch2 = ch // 2
        
        expand = Road.laneLength() * 2
        w, h = cw + expand, ch + expand
        w2, h2 = w // 2, h // 2
        
        img = Image.new('RGB', (w, h))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, w, h), fill = Road.backgroundColor())
        
        draw.rectangle((Road.laneLength(), Road.laneLength(), Road.laneLength() + cw, Road.laneLength() + ch), fill = Road.roadColor())
        
        xy1 = (12, 12)
        xy2 = (12, 24)
        
        if sys.platform == 'win32':
            font = ImageFont.truetype('mingliu.ttc', 12)
        else:
            font = ImageFont.truetype('NotoSansCJK-Regular.ttc', 12)
            
        draw.text(xy1, self.intersection_id, font = font)
        #draw.text(xy2, self.name, font = font)
        
        if 'North' in sdict:
            rimg = sdict['North']
            rw2, rh2 = rimg.size[0] // 2, rimg.size[1] // 2
            img.paste(rimg, (w2 - rw2, 0))
            
            sw = cw2 - rw2
            cdict['North'] = shiftC(cdict['North'], sw)
            
        if 'East' in sdict:
            rimg = sdict['East']
            rw, rh2 = rimg.size[0], rimg.size[1] // 2
            img.paste(rimg, (w - rw, h2 - rh2))
            
            sh = ch2 - rh2
            cdict['East'] = shiftC(cdict['East'], sh)
            
        if 'South' in sdict:
            rimg = sdict['South']
            rw2, rh = rimg.size[0] // 2, rimg.size[1]
            img.paste(rimg, (w2 - rw2, h - rh))
            
            sw = cw2 - rw2
            cdict['South'] = shiftC(cdict['South'], sw)
            
        if 'West' in sdict:
            rimg = sdict['West']
            rw2, rh2 = rimg.size[0] // 2, rimg.size[1] // 2
            img.paste(rimg, (0, h2 - rh2))            
            
            sh = ch2 - rh2
            cdict['West'] = shiftC(cdict['West'], sh)
            
            
        if (inTrack != '') and (outTrack != ''):
            img = self.__addTrack(img, sdict, cdict, inTrack, outTrack)
        
        if save:
            img.save(path)
            print('write png file {0} successfully'.format(path))
        else:
            #img.show()
            pass
            
        return img
        
    def __getImg(self, section, inRoad, outRoad):
        onewayroad = not (inRoad and outRoad)
        imglist = []
        for road in [inRoad, outRoad]:
            if road:
                imglist.append(road.getImg(onewayroad))
                
        if onewayroad:
            result = imglist[0]
            
            w, h = result.size
            
            if inRoad != None:
                ci = [Road.laneWidth(True) + Road.laneWidth() * ln for ln in range(inRoad.laneNum())]
                co = None
            
            if outRoad != None:
                ci = None
                co = [Road.laneWidth(True) + Road.laneWidth() * ln for ln in range(outRoad.laneNum())]
            
        else:
            
            inImg = imglist[0]
            outImg = imglist[1]
            
            w1, h1 = inImg.size
            w2, h2 = outImg.size
            
            if inRoad.section in ['North', 'South']:
                w, h = w1 + w2, h1
            elif inRoad.section in ['East', 'West']:
                w, h = w1, h1 + h2
                
            img = Image.new('RGB', (w, h))
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 0, w, h), fill = Road.backgroundColor())
            
            if inRoad.section == 'North':
                img.paste(inImg, (0, 0))
                img.paste(outImg, (w1 + 1, 0))
            elif inRoad.section == 'East':
                img.paste(inImg, (0, 0))
                img.paste(outImg, (0, h1 + 1))
            elif inRoad.section == 'South':
                img.paste(outImg, (0, 0))
                img.paste(inImg, (w2 + 1, 0))
            elif inRoad.section == 'West':
                img.paste(outImg, (0, 0))
                img.paste(inImg, (0, h2 + 1))
            
            ci = [Road.laneWidth(True) + Road.laneWidth() * ln for ln in range(inRoad.laneNum())]
            co = [Road.laneWidth(True) + Road.laneWidth() * ln for ln in range(outRoad.laneNum())]
            
            if inRoad.section in ['North', 'East']:
                rc = Road.laneWidth() * inRoad.laneNum()
                co = [c + rc + Road.roadOffset() for c in co]
            elif inRoad.section in ['South', 'West']:
                rc = Road.laneWidth() * outRoad.laneNum()
                ci = [c + rc + Road.roadOffset() for c in ci]
                
            result = img
            
        return result, onewayroad, (ci, co)
    
    def __addTrack(self, img, sdict, cdict, inTrack, outTrack):
        
        draw = ImageDraw.Draw(img)
        
        indf = self.pd[(self.pd['link_id'] == inTrack) & (self.pd['direction'] == 'In')]
        outdf = self.pd[(self.pd['link_id'] == outTrack) & (self.pd['direction'] == 'Out')]
        
        if (indf.shape[0] > 0) and (outdf.shape[0] > 0):
            indir = indf.iloc[0]['section']
            outdir = outdf.iloc[0]['section']
            
            cw, ch = img.size[0] - Road.laneLength() * 2, img.size[1] - Road.laneLength() * 2
            
            '''
            if ((indir in ['South', 'North']) and (outdir in ['East', 'West'])):
                shiftX = (cw - sdict[indir].size[0]) // 2
                shiftY = (ch - sdict[outdir].size[1]) // 2
            elif ((indir in ['East', 'West']) and (outdir in ['South', 'North'])):
                shiftX = (cw - sdict[outdir].size[0]) // 2
                shiftY = (ch - sdict[indir].size[1]) // 2
                
                
                elif ((indir in ['North', 'East']) and (outdir in ['South', 'West'])):
                    shiftX = 0
                    shiftY = 0                
                elif ((indir in ['South', 'West']) and (outdir in ['North', 'East'])):
                    shiftX = 0
                    shiftY = 0
            else:
                shiftX = 0
                shiftY = 0
            '''
            
            shiftX = 0
            shiftY = 0
                
            c1x = Road.laneLength() + shiftX
            c1y = Road.laneLength() + shiftY
            c2x = c1x + cw
            c2y = c1y + ch
            
            arc = False
            line = False
            polygon = False
            
            start = 0
            end = 0
            
            if indir == 'South':
                if outdir == 'East':
                    arc = True
                    polygon = True
                    start = 180
                    end = 270
                    
                    rci = cdict[indir][0][-1]
                    rco = cdict[outdir][1][-1]
                    
                    p1x = c1x + rci
                    p1y = c1y + rco
                    p2x = p1x + (cw - rci) * 2
                    p2y = p1y + (ch - rco) * 2
                    
                    arror = self.__drawArrow(c2x, p1y, 0)
                    
                elif outdir == 'North':
                    line = True
                    polygon = True
                    
                    rci = np.mean(cdict[indir][0]).astype(np.int) + 2
                    rco = np.mean(cdict[outdir][1]).astype(np.int) + 2
                    
                    p1x = c1x + rci
                    p1y = c2y
                    p2x = c1x + rco
                    p2y = c1y
                    
                    arror = self.__drawArrow(p2x - 6, c1y, 270)
                    
                elif outdir == 'West':
                    arc = True
                    polygon = True
                    start = 270
                    end = 0
                    
                    rci = cdict[indir][0][0]
                    rco = cdict[outdir][1][-1]
                    
                    p1x = c1x - rci
                    p1y = c1y + rco
                    p2x = c1x + rci
                    p2y = c2y + (ch - rco)
                    
                    arror = self.__drawArrow(c1x, p1y + 2, 180)
                    
            elif indir == 'East':
                if outdir == 'North':
                    arc = True
                    polygon = True
                    start = 90
                    end = 180
                    
                    rci = cdict[indir][0][0]
                    rco = cdict[outdir][1][-1]
                    
                    p1x = c1x + rco
                    p1y = c1y - rci
                    p2x = p1x + (cw - rco) * 2
                    p2y = p1y + rci * 2
                    
                    arror = self.__drawArrow(p1x - 2, c1y, 270)
                    
                elif outdir == 'West':
                    line = True
                    polygon = True
                    
                    rci = np.mean(cdict[indir][0]).astype(np.int) + 2
                    rco = np.mean(cdict[outdir][1]).astype(np.int) + 2
                    
                    p1x = c2x
                    p1y = c1y + rci
                    p2x = c1x
                    p2y = c1y + rco
                    
                    arror = self.__drawArrow(c1x - 6, p2y, 180)
                    
                elif outdir == 'South':
                    arc = True
                    polygon = True
                    start = 180
                    end = 270
                    
                    rci = cdict[indir][0][-1]
                    rco = cdict[outdir][1][-1]
                    
                    p1x = c1x + rco
                    p1y = c1y + rci
                    p2x = p1x + (cw - rco) * 2
                    p2y = p1y + (ch - rci) * 2
                    
                    arror = self.__drawArrow((c1x + rco) - 4, c2y, 90)
                    
            elif indir == 'North':
                if outdir == 'West':
                    arc = True
                    polygon = True
                    start = 0
                    end = 90
                    
                    rci = cdict[indir][0][0]
                    rco = cdict[outdir][1][0]
                    
                    p1x = c1x - rci
                    p1y = c1y - rco
                    p2x = c1x + rci
                    p2y = c1y + rco + 4
                    
                    arror = self.__drawArrow(c1x - 8, p2y, 180)
                    
                elif outdir == 'South':
                    line = True
                    polygon = True
                    
                    rci = np.mean(cdict[indir][0]).astype(np.int) + 2
                    rco = np.mean(cdict[outdir][1]).astype(np.int) + 2
                    
                    p1x = c1y + rci
                    p1y = c1y
                    p2x = c1y + rco
                    p2y = c2y
                    
                    arror = self.__drawArrow((c1x + rco) - 4, c2y, 90)
                    
                elif outdir == 'East':
                    arc = True
                    polygon = True
                    start = 90
                    end = 180
                    
                    rci = cdict[indir][0][-1]
                    rco = cdict[outdir][1][0]
                    
                    p1x = c1x + rci
                    p1y = c1y - rco
                    p2x = p1x + (cw - rci) * 2
                    p2y = p1y + rco * 2 + 4
                    
                    arror = self.__drawArrow(c2x, (c1y + rco) + 2, 0)
                    
            elif indir == 'West':
                if outdir == 'South':
                    arc = True
                    polygon = True
                    start = 270
                    end = 0
                    
                    rci = cdict[indir][0][-1]
                    rco = cdict[outdir][1][0]
                    
                    p1x = c1x - rco
                    p1y = c1y + rci
                    p2x = p1x + (rco) * 2 + 4
                    p2y = p1y + (ch - rci) * 2
                    
                    arror = self.__drawArrow((c1x + rco) - 2, c2y + 2, 90)
                    
                elif outdir == 'East':
                    line = True
                    polygon = True
                    
                    rci = np.mean(cdict[indir][0]).astype(np.int) + 2
                    rco = np.mean(cdict[outdir][1]).astype(np.int) + 2
                    
                    p1x = c1x
                    p1y = c1y + rci
                    p2x = c2x
                    p2y = c1y + rco
                    
                    arror = self.__drawArrow(c2x, c1y + rco, 0)
                    
                elif outdir == 'North':
                    arc = True
                    polygon = True
                    start = 0
                    end = 90
                    
                    rci = cdict[indir][0][0]
                    rco = cdict[outdir][1][0]
                    
                    p1x = c1x - rco
                    p1y = c1y - rci
                    p2x = c1x + rco + 6
                    p2y = c1y + rci
                    
                    arror = self.__drawArrow(c1x + rco, c1y - 2, 270)
                    
            xy = [(p1x, p1y), (p2x, p2y)]
            
            if arc:
                #draw.rectangle(xy, fill = (255, 255, 255))
                draw.arc(xy, start = start, end = end, fill = 'red', width = 4)
                
            if line:
                draw.line(xy, fill = 'red', width = 4)
                
            if polygon:
                #draw.polygon(arror, fill = 'red', width = 4)
                draw.polygon(arror, fill = 'red')
                
        return img
        
    def __drawArrow(self, x, y, angle = 0):
        
        def rotate(pos, angle):    
            cen = (5 + x, 0 + y)
            angle *= -(math.pi/180)
            cos_theta = math.cos(angle)
            sin_theta = math.sin(angle)
            ret = ((cos_theta * (pos[0] - cen[0]) - sin_theta * (pos[1] - cen[1])) + cen[0],
            (sin_theta * (pos[0] - cen[0]) + cos_theta * (pos[1] - cen[1])) + cen[1])
            return ret
        
        p0 = rotate((x, -8+y), 360-angle)
        p1 = rotate((x, 8+y), 360-angle)
        p2 = rotate((14+x, y), 360-angle)
    
        return [p0,p1,p2] 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        