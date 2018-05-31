import numpy as np

from test_base.tensorflow_captcha.cfg import MAX_CAPTCHA, CHAR_SET_LEN,gen_char_set
from PIL import Image


def char2pos(c):
    return gen_char_set.index(c)




def pos2char(char_idx):
    return gen_char_set[char_idx]




def convert2gray(img):

    img=Image.fromarray(img)
    img=img.convert('L')
    img=np.array(img)
    return img



def text2vec(text):
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        text=text[0:MAX_CAPTCHA-1]#原代码没有这一行，下一行取消注释，如果识别出大于预期验证码长度的字符串则强制截取避免报错
        # raise ValueError('验证码最长MAX_CAPTCHA个字符')
    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    for i, c in enumerate(text):
        idx = i * CHAR_SET_LEN + char2pos(c)
        vector[idx] = 1
    return vector


# 向量转回文本
def vec2text(vec):
    char_pos = vec.nonzero()[0]
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i
        char_idx = c % CHAR_SET_LEN
        char_code = pos2char(char_idx)
        text.append(char_code)
    return "".join(text)


