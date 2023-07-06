import random
import string
import numpy as np
import matplotlib.pyplot as plt
import requests
from captcha.image import ImageCaptcha

characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
print(characters)

width, height, n_len, n_class = 150, 50, 6, len(characters)

generator = ImageCaptcha(width=width, height=height)
random_str = ''.join([random.choice(characters) for j in range(4)])
random_str = 'j10O'


# img = generator.generate_image(random_str)
# generator.write(random_str, './images/j10O.png')

# plt.imshow(img)
# plt.title(random_str)


def gen1(batch_size=32):
    for i in range(batch_size):
        i += 50273
        random_str_len = random.randint(4, 6)
        random_str = ''.join([random.choice(characters) for j in range(6)])
        # generator.write(random_str, 'D:/captcha/dataset/train/%s_%d.png' % (random_str, i))
        generator.write(random_str, 'E:/datasets/captcha/train3/%d_%s.png' % (i, random_str))


def gen(batch_size=32):
    X = np.zeros((batch_size, height, width, 3), dtype=np.uint8)
    y = [np.zeros((batch_size, n_class), dtype=np.uint8) for i in range(n_len)]
    generator = ImageCaptcha(width=width, height=height)
    while True:
        for i in range(batch_size):
            random_str_len = random.randint(4, 6)
            random_str = ''.join([random.choice(characters) for j in range(random_str_len)])
            X[i] = generator.generate_image(random_str)
            if random_str_len < n_len:
                for k in range(n_len - random_str_len):
                    random_str += ' '
            for j, ch in enumerate(random_str):
                y[j][i, :] = 0
                y[j][i, characters.find(ch)] = 1

        yield X, y


def decode(y):
    y = np.argmax(np.array(y), axis=2)[:, 0]
    return ''.join([characters[x] for x in y])


def generate_captcha(path, count):
    r"""
     生成一定数量的图形验证码用于训练以及测试模型
    :param path: 图形验证码存放路径
    :param count: 生成数量
    :return:
    """
    url = 'http://crm.gouyashop.com/api/gycmphome/unifiedAuth/get/captcha/tianqisen'
    header = {
        "X-GW-APPID": "1000004082",
        "X-GW-PLATFORM": "tms.gouyashop",
        "X-GW-TENANTID": "gouyashop",
        "X-GW-TIMESTAMP": "1688624954598"
    }
    for num in range(0, count):
        response = requests.get(url, headers=header)
        with open('{path}{num}.png'.format(path=path, num=num), 'wb') as f:
            f.write(response.content)


# X, y = next(gen(1))
# plt.imshow(X[0])
# plt.title(decode(y))

if __name__ == '__main__':
    generate_captcha('/Users/tianqisen/PycharmProjects/captcha_ocr/lstm_ctc/test_set/', 1000)
    # gen1(49727)
    # import os
    # import re
    # for root, dir, files in os.walk('E:/datasets/captcha/train3/'):
    #     for file in files:
    #         pattern = re.compile('.*?_(.*?)\.')
    #         # pattern = re.compile('(.*?)_')
    #         m = pattern.match(file)
    #         if m is not None:
    #             print(m.group())
    #             print(m.group(1))
    #         break
    print('===END===')
