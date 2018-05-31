# -*- coding: utf-8 -*-

#调用文件操作
import shutil
#调用操作系统接口
import os
import uuid
import requests
import re
import numpy as np
import tensorflow as tf
from test_base.tensorflow_captcha.cfg import MAX_CAPTCHA, CHAR_SET_LEN, model_path
from test_base.tensorflow_captcha.cnn_sys import crack_captcha_cnn, X, keep_prob
from test_base.tensorflow_captcha.predict import hack_function

#调用自定义方法
from test_base.captcha import *
from test_base.oper import *
from test_base.help import *

global_step = tf.Variable(0, trainable=False)
output = crack_captcha_cnn()
predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
saver = tf.train.Saver()
with tf.Session(config=tf.ConfigProto(device_count={'gpu': 0})) as sess:
    saver.restore(sess, tf.train.latest_checkpoint(model_path))
    while 1:
        #...此处略去了保存图片的过程
        image_path = 'E:\\1.png'
        image = image.convert('L')
        image = np.array(image)
        image = image.flatten() / 255
        predict_text = hack_function(sess, predict, image)
        uuidd = uuid.uuid1().hex
        father_path = os.path.abspath(os.path.join(image_path, ".."))
        new_path = father_path + '\\' + predict_text + '__' + uuidd + '.jpg'
        # print(predict_text,new_path)
        try:
            os.rename(image_path, new_path)
        except Exception:
            os.remove(image_path)
