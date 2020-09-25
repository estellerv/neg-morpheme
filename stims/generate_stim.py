from PIL import Image, ImageDraw,ImageFont
import scipy.optimize
import scipy, math
from math import sin, cos, pi
from webcolors import name_to_rgb

#####STIM
#img size
x=200*30
y=200*30

def poly(sides, rotation = 0, radius = x/2, translation = [x/2, y/2]):
    one_segment = math.pi * 2 / sides
    points = [
            (math.sin(one_segment * i + rotation) * radius,
             math.cos(one_segment * i + rotation) * radius)
            for i in range(sides)] 
    if translation:
        points = [[sum(pair) for pair in zip(point, translation)]
        for point in points]
        points  = [(point[0], point[1]) for point in points]

    return points


def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
    # This uses the generalized formula for bezier curves
    # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
            tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n, memo={}):
# This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result

def heart():
    ts = [float(t)/x for t in range(x+1)]

    xys = [(x/2, x), (0.8*x, 0.8*x), (x, x/2)]
    bezier = make_bezier(xys)
    points = bezier(ts)

    xys = [(x, x/2), (x, 0), (x/2, 0), (x/2, 0.35*x)]
    bezier = make_bezier(xys)
    points.extend(bezier(ts))

    xys = [(0.5*x, 0.35*x), (0.5*x, 0), (0, 0), (0, x/2)]
    bezier = make_bezier(xys)
    points.extend(bezier(ts))

    xys = [(0, x/2), (0.35*x, 0.8*x), (x/2, x)]
    bezier = make_bezier(xys)
    points.extend(bezier(ts))
    return points

def tangram1():#ninja
    points = [(0, 0.6*y), (0.4*x, 0.2*y), (0.4*x, 0), (0.8*x,0.4*y), (x,0.4*y), (0.6*x, 0.8*y), (0.6*x, y), (0.2*x, 0.6*y)]
    exclude = [(0.4*x, 0.4*y), (0.6*x, 0.4*y), (0.6*x, 0.6*y), (0.4*x, 0.6*y)]
    return [points, exclude]

def tangram2():#poisson
    points = [(0.1*x, 0.5*y), (0.5*x, 0.1*y), (0.5*x, 0.2*y), (0.7*x, 0.4*y), (0.9*x, 0.2*y), (0.9*x, 0.8*y), (0.7*x, 0.6*y), (0.5*x, 0.8*y), (0.5*x, 0.9*y)]
    return points

def tangram3():#A
    points = [(0.2*x, 0.9*y), (0.2*x, 0.3*y), (0.4*x, 0.1*y), (0.6*x,0.1*y), (x*0.8,0.3*y), (0.8*x, 0.9*y), (0.6*x, 0.7*y), (0.4*x, 0.7*y)]
    exclude = [(0.4*x, 0.3*y), (0.6*x, 0.3*y), (0.6*x, 0.5*y), (0.4*x, 0.5*y)]
    return [points, exclude]

def tangram4():#M
    points = [(0.1*x, 0.1*y), (0.5*x, 0.5*y), (0.9*x, 0.1*y), (0.9*x, 0.9*y), (0.7*x, 0.7*y), (0.7*x, 0.5*y), (0.5*x, 0.7*y), (0.3*x, 0.5*y), (0.3*x, 0.7*y), (0.1*x, 0.9*y)]
    return points

def tangram5():#sapin
    points = [(0.5*x, 0.1*y), (0.9*x, 0.5*y), (0.7*x, 0.5*y), (0.9*x, 0.7*y), (0.6*x, 0.7*y), (0.6*x, 0.9*y), (0.4*x, 0.9*y), (0.4*x, 0.7*y), (0.1*x, 0.7*y), (0.3*x, 0.5*y), (0.1*x, 0.5*y)]
    return points

def tangram6():#fusee
    points = [(0.5*x, 0*y), (0.7*x, 0.2*y), (0.7*x, 0.6*y), (0.6*x, 0.6*y), (0.8*x, 0.8*y), (0.8*x, 1*y), (0.6*x, 0.8*y), (0.4*x, 0.8*y), (0.2*x, 1*y), (0.2*x, 0.8*y), (0.4*x, 0.6*y), (0.3*x, 0.6*y), (0.3*x, 0.2*y)]
    return points

def tangram7():#papillon
    points = [(0.1*x, 0.1*y), (0.5*x, 0.5*y), (0.9*x, 0.1*y), (0.9*x, 0.5*y), (0.7*x, 0.7*y), (0.7*x, 0.9*y), (0.5*x, 0.7*y), (0.3*x, 0.9*y), (0.3*x, 0.7*y), (0.1*x, 0.5*y)]
    return points
    
def tangram8():#sablier
    points = [(0.1*x, 0.21*y), (0.35*x, 0.5*y), (0.1*x, 0.79*y), (0.9*x, 0.79*y), (0.65*x, 0.5*y), (0.9*x, 0.21*y)]
    return points

def tangram9():#C
    points = [(0.1*x, 0.25*y), (0.1*x, 0.75*y), (0.9*x, 0.75*y), (0.9*x, 0.25*y), (0.70*x, 0.25*y), (0.70*x, 0.55*y), (0.30*x, 0.55*y),(0.30*x, 0.25*y)]
    return points

def tangram10():#fleche
    points = [(0.01*x, 0.5*y), (0.4*x, 0.9*y), (0.8*x, 0.9*y), (0.4*x, 0.5*y), (0.8*x, 0.1*y), (0.4*x, 0.1*y)]
    return points

def tangram11(): #moulin
    points = [(0*x, 0.5*y), (0.5*x, 0.5*y), (0.35*x, 0.65*y), (0.35*x, 0.85*y), (0.5*x, 1*y), (0.5*x, 0.5*y), (0.75*x, 0.75*y),  (1*x, 0.5*y),  (0.5*x, 0.5*y),  (0.65*x, 0.35*y), (0.65*x, 0.15*y), (0.5*x, 0*y), (0.5*x, 0.5*y), (0.25*x, 0.25*y)]
    return points

def tangram12(): #hexagon
    points = [(0.05*x,0.5*y),(0.35*x, 0.80*y),(0.65*x,0.80*y),(0.95*x,0.5*y),(0.65*x,0.20*y),(0.35*x, 0.20*y)] 
    return points

def diamond():
    points = [(0, 0.5*y),(0.5*x,y),(x,0.5*y),(0.5*x,0)]
    return points

def cross(x_bot, y_bot):
    points = [(0.05*x+x_bot, 0*y+y_bot), (0.05*x+x_bot, 0.05*y+y_bot), (0*x+x_bot, 0.05*y+y_bot), (0*x+x_bot, 0.13*y+y_bot), (0.05*x+x_bot, 0.13*y+y_bot), (0.05*x+x_bot, 0.19*y+y_bot), (0.13*x+x_bot, 0.19*y+y_bot),(0.13*x+x_bot, 0.13*y+y_bot), (0.19*x+x_bot, 0.13*y+y_bot), (0.19*x+x_bot, 0.05*y+y_bot), (0.13*x+x_bot, 0.05*y+y_bot), (0.13*x+x_bot, 0*y+y_bot)]
    return points

set_shapes=[tangram11(),tangram9(),tangram8()]
set_col=['lightgray','magenta','cyan']
col_neg = 'white'
neg = 0.1

for i in range(3):
    #cue shape
    imageC1 = Image.new('RGB',(x,y),'black')
    drawC1 = ImageDraw.Draw(imageC1)
    drawC1.polygon(set_shapes[i], fill = "mediumslateblue")
    imageC1 = imageC1.resize((x/10,y/10), resample=Image.ANTIALIAS )

    #cue Xshape
    imageCX1 = Image.new('RGB',(x,y),'black')
    drawCX1 = ImageDraw.Draw(imageCX1)
    drawCX1.polygon(set_shapes[i], fill = "mediumslateblue")

    drawCX1.polygon(cross(0,0),fill = col_neg, outline = None)
    drawCX1.polygon(cross(x*0.81,0),fill = col_neg, outline = None)
    drawCX1.polygon(cross(0,y*0.81),fill = col_neg, outline = None)
    drawCX1.polygon(cross(x*0.81,y*0.81),fill = col_neg, outline = None)

#    drawCX1.ellipse((0, 0, x*neg, y*neg), fill = 'magenta', outline = None)
#    drawCX1.ellipse((x*(1-neg), y*(1-neg), x, y), fill = 'magenta', outline = None)
#    drawCX1.ellipse((x*(1-neg), 0, x, y*neg), fill = 'magenta', outline = None)
#    drawCX1.ellipse((0, y*(1-neg), x*neg, y), fill = 'magenta', outline = None)
    imageCX1 = imageCX1.resize((x/10,y/10), resample=Image.ANTIALIAS )

    #cue col
    imageC2 = Image.new('RGB',(x,y),'black')
    drawC2 = ImageDraw.Draw(imageC2)
#    drawC2.ellipse((0.1*x, 0.1*x, 0.9*x, 0.9*y), fill = set_col[i], outline = None)
    drawC2.polygon(tangram10(), fill = set_col[i])
    imageC2 = imageC2.resize((x/10,y/10), resample=Image.ANTIALIAS )

       #shape
    image = Image.new('RGB',(x,y),'black')
    draw = ImageDraw.Draw(image)
    draw.polygon(set_shapes[i], fill = 'mediumslateblue')
    image = image.resize((x/10,y/10), resample=Image.ANTIALIAS )
   
   
    if i == 0:
        imageC1.save('./set1_cueA' + '.bmp')
        imageCX1.save('./set1_cueAx' + '.bmp')
        image.save('./set1_a' + '.bmp')
    elif i == 1:
        imageC1.save('./set1_cueB' + '.bmp')
        imageCX1.save('./set1_cueBx' + '.bmp')
        image.save('./set1_b' + '.bmp')
    elif i == 2:
        imageC1.save('./set1_cueC' + '.bmp')
        imageCX1.save('./set1_cueCx' + '.bmp')
        image.save('./set1_c' + '.bmp')



