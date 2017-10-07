# coding=utf-8
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont  # 图片，绘制，字体
from cStringIO import StringIO  # 返回一个类似stringio的流，用于读取或写入
from string import printable


def pillow_test():
    # In[创建画布]
    width, height = 100, 40  # 宽,高
    image = Image.new('RGB', (width, height), (255, 255, 255))          # 创建具有给定模式和大小的新图像
    draw = ImageDraw.Draw(image)
    # In[创建字体]
    font_path = 'utils/captcha/font/Arial.ttf'                          # 字体路径
    font = ImageFont.truetype(font_path, height - 10)                   # 给定的文件加载一个字体对象，并创建字体对象的字体大小

    font_color = (randint(150, 200), randint(0, 0), randint(0, 0))      # 字体颜色
    line_color = (randint(50, 200), randint(50, 200), randint(50, 200)) # 线颜色
    point_color = (randint(0, 255), randint(0, 255), randint(0, 255))   # 点颜色

    # In[生成验证码]
    text = ''.join([choice(printable[:62]) for i in xrange(4)])         # choice随机选择,
    # In[把验证码写到画布上]							                    # printable一种包含所有被认为可打印的字符的字符串
    draw.text((10, 10), text, fill=font_color, font=font)
    # In[绘制线条]
    for i in xrange(0, 4):
        draw.line(((randint(0, width), randint(0, height)), (randint(0, width), randint(0, height))), fill=line_color,
                  width=2)
    # In[绘制点]
    for i in xrange(randint(30, 300)):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)

    # In[输出]
    out = StringIO()
    image.save(out, format='jpeg')  # format格式
    content = out.getvalue()  # 取内容
    out.close()
    return content, text







