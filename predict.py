"""
专门做预测的
"""
import time

import numpy as np
import tensorflow as tf

from test_base.tensorflow_captcha.utils import convert2gray, vec2text
from test_base.tensorflow_captcha.cfg import MAX_CAPTCHA, CHAR_SET_LEN, model_path
from test_base.tensorflow_captcha.cnn_sys import crack_captcha_cnn, X, keep_prob
from test_base.tensorflow_captcha.gen_captcha import wrap_gen_captcha_text_and_image

from PIL import Image
import os
import uuid
import test_base.tensorflow_captcha.globalvar as gl

def hack_function(sess, predict, captcha_image):
    text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

    text = text_list[0].tolist()
    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    i = 0
    for n in text:
        vector[i * CHAR_SET_LEN + n] = 1
        i += 1
    return vec2text(vector)


def batch_hack_captcha():

    # 定义预测计算图
    global_step = tf.Variable(0, trainable=False)
    output = crack_captcha_cnn()
    predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    saver = tf.train.Saver()

    with tf.Session(config=tf.ConfigProto(device_count={'gpu':0})) as sess:
        # saver = tf.train.import_meta_graph(save_model + ".meta")


        saver.restore(sess, tf.train.latest_checkpoint(model_path))

        stime = time.time()
        task_cnt = 1000
        right_cnt = 0
        for i in range(task_cnt):
            text, image = wrap_gen_captcha_text_and_image(x=0)
            image = image.flatten() / 255
            predict_text = hack_function(sess, predict, image)
            if text == predict_text:
                # print()
                text=text.replace('_','')
                print("----MATCH: {}".format(text))
                # print()
                right_cnt += 1
            else:
                print("标记: {}  预测: {}".format(text, predict_text))


        print('task:', task_cnt, ' cost time:', (time.time() - stime), 's')
        print('right/total-----', right_cnt, '/', task_cnt)

def test_hack_captcha_training_data(sess,output):

    predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    stime = time.time()

    right_cnt = 0
    task_cnt = 100
    for i in range(task_cnt):
        text, image= wrap_gen_captcha_text_and_image(x=0)
        #image = convert2gray(image)
        image = image.flatten() / 255
        predict_text = hack_function(sess, predict, image)
        #predict_text=predict_text.replace('_','')
        if text == predict_text:
            print("----标记: {}  预测: {}".format(text, predict_text))
            right_cnt += 1
        else:
           print("标记: {}  预测: {}".format(text, predict_text))


    #print('task:', task_cnt, ' cost time:', (time.time() - stime), 's')
    #print('right/total-----', right_cnt, '/', task_cnt)
    return right_cnt/task_cnt

def captcha_regenize(image_path):
    global_step = tf.Variable(0, trainable=False)
    output = crack_captcha_cnn()
    predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    saver = tf.train.Saver()

    with tf.Session(config=tf.ConfigProto(device_count={'gpu':0})) as sess:
        saver.restore(sess, tf.train.latest_checkpoint(model_path))
        image = Image.open(image_path)
        image = image.convert('L')
        image = np.array(image)
        image = image.flatten() / 255
        predict_text = hack_function(sess, predict, image)
    uuidd = uuid.uuid1().hex
    father_path = os.path.abspath(os.path.join(image_path,".."))
    new_path=father_path+'\\' + predict_text + '__' + uuidd + '.jpg'
    try:
        os.rename(image_path,new_path)
    except Exception:
        os.remove(image_path)
    return predict_text,new_path


if __name__ == '__main__':
    gl._init()
    gl.set_value('RightFilePath','E:\\captcha\\new')
    RightFilePath=gl.get_value('RightFilePath')
    gl.set_value('FileList',os.listdir(RightFilePath))
    batch_hack_captcha()
    # print(captcha_regenize('E:\\1.png'))
    print('end...')
