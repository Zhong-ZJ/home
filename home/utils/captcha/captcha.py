#coding=utf-8
from random import randint,choice
from PIL import Image,ImageDraw,ImageFont         #图像，绘制，字体
from cStringIO import StringIO                    #cStringIO内存文件
from string import printable                      #0~9,a~z,A~Z


def pillow_test():
    # img = Image.open('handlers/files/upload_files/image1.jpg')
    # out = StringIO()
    # img.save(out,format='jpeg')
    # content = out.getvalue()
    # out.close()
    # return content

    # In[1]设置字体路径,字体颜色,线颜色,点颜色
    font_path = "utils/captcha/font/Arial.ttf"
    font_color = (randint(150,200),randint(0,0),randint(0,0))
    line_color = (randint(0,0),randint(0,0),randint(150,200))
    point_color = (randint(0,150),randint(50,150),randint(150,200))

    # In[2]绘制
    width,height = 100,40
    image = Image.new('RGB',(width,height),(255,255,255))              #创建一个画布
    font = ImageFont.truetype(font_path,height-10)                     #设置字体
    draw = ImageDraw.Draw(image)                                       #绘制

    # In[3]生成验证码
    text = ''.join([choice(printable[:62]) for i in xrange(4)])        #遍历字符
    font_width,font_height = font.getsize(text)                        #获取字体大小

    # In[4]把验证码写到画布上
    draw.text((10,10),text,font = font,fill=font_color)

    # In[5]绘制线条
    for i in xrange(0,5):
        draw.line((randint(0,width),randint(0,height)),
                  ((randint(0,width), randint(0,height))),
                  fill=line_color,width=2)

    # In[6]绘制点
    for i in xrange(0,300):
        draw.point((randint(0,width),randint(0,height)),fill=point_color)

    # In[7]输出
    out = StringIO()
    image.save(out, format='jpeg')
    content = out.getvalue()
    out.close()
    return text,content