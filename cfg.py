# _*_coding:utf-8_*_
from os.path import join
import os
home_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"."))
f=open(home_root+'\\chinese.txt','rb')#加载3500个常用汉字
CH_CHAR=[]
lines=f.read().decode('utf-8')
f.close()
CH_CHAR=eval(lines)
# print(CH_CHAR)

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

gen_char_set =alphabet#+ number+  #+CH_CHAR + ['_'] # 用于生成验证码的数据集,'_'为不定长验证码的占位符
#gen_char_set=number+ALPHABET+['_']
# 有先后的顺序的

# 图像大小
# IMAGE_HEIGHT = 36
# IMAGE_WIDTH = 90

IMAGE_HEIGHT = 70
IMAGE_WIDTH = 200

MAX_CAPTCHA = 4  # 验证码最大长度
print("验证码文本最长字符数", MAX_CAPTCHA)  # 验证码最长6字符; 我全部固定为6,可以不固定. 如果验证码长度小于6，用'_'补齐


CHAR_SET_LEN = len(gen_char_set)

print('CHAR_SET_LEN:', CHAR_SET_LEN)

# home_root = 'F:\\tensorflow'
# print('home_root:',home_root)

model_path = join(home_root, 'model')
model_tag = 'crack_capcha.model'
save_model = join(model_path, model_tag)

print('model_path:', save_model)

# 输出日志 tensorboard监控的内容
tb_log_path =join(home_root, 'tmp\mnist_logs')
print('tb_log_path:',tb_log_path)
