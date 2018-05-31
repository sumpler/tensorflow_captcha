import random
from os import path,listdir
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageFilter
#from captcha.image import ImageCaptcha  # pip install captcha
from test_base.tensorflow_captcha.captcha_modifyed.image import ImageCaptcha
from test_base.tensorflow_captcha.cfg import MAX_CAPTCHA,IMAGE_HEIGHT, IMAGE_WIDTH, CHAR_SET_LEN
from test_base.tensorflow_captcha.cfg import gen_char_set,number,ALPHABET,CH_CHAR,alphabet
import uuid
import os
import shutil
import test_base.tensorflow_captcha.globalvar as gl

WHITE=0
WHITE_THRES=0
def choice_set(if_no_chinese):
    if if_no_chinese==1:
        set_choice=random.randint(1,2)#取随机数1-2
    else:
        set_choice=random.randint(1,3)#取随机数1-3
    if set_choice==1 :
        return number#数字
    elif set_choice==2:
        return alphabet#小写字母
    else:
        return CH_CHAR#中文

def random_captcha_text(captcha_size=MAX_CAPTCHA):#获取验证码字符
    # _size=random.randint(1,captcha_size)#设置验证码长度,不定长
    _size=captcha_size#设置验证码长度，定长
    captcha_text = []
    # is_no_chinese=random.randint(0,2)
    for i in range(_size):
        c = random.choice(choice_set(1))#返回list的随机项，如alphabet内的随机一个字母
        captcha_text.append(c)#把随机项加到captcha_text的末尾
    if len(captcha_text)<MAX_CAPTCHA:#如果captcha_text长度小于MAX_CAPTCHA就在末尾补足'_'，对于定长验证码没用
        for i in range(MAX_CAPTCHA-len(captcha_text)):
            captcha_text.append('_')
    # print(captcha_text)
    return captcha_text

def _inittable():
    table=[]
    global WHITE,WHITE_THRES

    for i in range(256):
        if i>WHITE_THRES:
            table.append(WHITE)
        else:
            table.append(0)
    return table

def gen_captcha_text_and_image():
    """
    生成字符对应的验证码
    :return:
    """
    path='C:\\Users\Administrator\PycharmProjects\personal\\tensorflow-master\chinese_captcha_crack\\font\\'#英文字体目录
    path2='C:\\Users\Administrator\PycharmProjects\personal\\tensorflow-master\chinese_captcha_crack\\font2\\'#中文字体目录
    all_font=listdir(path)
    # print('all_font:',all_font)
    font_list=[]
    font_list2=[]
    for i in all_font:
        font_list.append(path+i)
    # print('font_list:',font_list)
    # all_font=listdir(path2)
    # for i in all_font:
    #     font_list2.append(path2+i)
    # image = ImageCaptcha(width=180,height=72,fonts=font_list)#,fonts2=font_list2)
    image = ImageCaptcha(width=150,height=56,fonts=font_list)#,fonts2=font_list2)
    # print('image:',image)
    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text)
    str=captcha_text.replace('_','')
    captcha = image.generate(str)
    captcha_image = Image.open(captcha)
    # captcha_image=captcha_image.resize((90,36))
    captcha_image=captcha_image.resize((75,28))
    captcha_image=captcha_image.convert('L')
    global WHITE,WHITE_THRES
    WHITE_THRES=random.randint(110,120)
    # WHITE=random.randint(210,220)
    WHITE=255#控制了背景色
    captcha_image=captcha_image.point(_inittable())
    captcha_image = captcha_image.filter(ImageFilter.SMOOTH)
    captcha_image = np.array(captcha_image)
    # print('captcha_text, captcha_image:',captcha_text, captcha_image)
    return captcha_text, captcha_image


def wrap_gen_captcha_text_and_image(x=1):#获得一张图就移除一张图
    # text, image = gen_captcha_text_and_image()
    RightFilePath = gl.get_value('RightFilePath')
    UsedFilePath = gl.get_value('UsedFilePath')
    FileList = gl.get_value('FileList')
    RandomFile = random.choice(FileList)
    FileName = os.path.splitext(RandomFile)[0]
    if '_' in FileName:
        text=FileName.split('_')[0]
    else:
        text=FileName
    if x:
        shutil.move(RightFilePath+'\\'+RandomFile,UsedFilePath)
        FileList.remove(RandomFile)
        gl.set_value('FileList',FileList)
        try:
            image = Image.open(UsedFilePath + '\\' + RandomFile)
        except Exception:
            wrap_gen_captcha_text_and_image()
    else:
        image = Image.open(RightFilePath + '\\' + RandomFile)
    im = image
    im = im.convert("L")
    # 打印像素直方图
    # his = im.histogram()
    # values = {}
    # for i in range(0, 256):
    #     values[i] = his[i]

    # 排序，x:x[1]是按照括号内第二个字段进行排序,x:x[0]是按照第一个字段
    # temp = sorted(values.items(), key=lambda x: x[1], reverse=True)

    # 占比最多的10种颜色
    # for j, k in temp[:10]:
        # print(j, k)
        # pass
    # 255 12177
    # 0 772
    # 254 94
    # 获取图片大小，生成一张白底255的图片
    im2 = Image.new("P", im.size, 255)
    for y in range(im.size[1]):
        # 获得y坐标
        for x in range(im.size[0]):
            # 获得坐标(x,y)的RGB值
            pix = im.getpixel((x, y))
            # print(pix)
            if pix <249:
                # 将黑色0填充到im2中
                im2.putpixel((x, y), 0)
    image = im2.convert('L')
    image = np.array(image)
    return text, image


def __gen_and_save_image():
    """
    可以批量生成验证图片集，并保存到本地，方便做本地的实验
    :return:
    """
    for i in range(10):
        text, image = wrap_gen_captcha_text_and_image()
        # text, image = gen_captcha_text_and_image()
        im = Image.fromarray(image)
        uuidd = uuid.uuid1().hex
        image_name = '__%s__%s.png' % (text, uuidd)
        img_root = join('F:\\tensorflow', 'train')#训练样本的系统路径
        image_file = path.join(img_root, image_name)
        im.save(image_file)

if __name__ == '__main__':
    # print(capt.cfg.workspace)
    gl._init()
    gl.set_value('RightFilePath','E:\\人才新验证码\\new')
    RightFilePath=gl.get_value('RightFilePath')
    gl.set_value('FileList',os.listdir(RightFilePath))
    __gen_and_save_image()
    pass


