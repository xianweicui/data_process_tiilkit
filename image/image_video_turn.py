from PIL import Image
import cv2
import numpy as np
import os

import re

re_digits = re.compile(r'(\d+)')


def embedded_numbers(s):
    pieces = re_digits.split(s)  # 切成数字和非数字
    pieces[1::2] = map(int, pieces[1::2])  # 将数字部分转成整数
    return pieces


def sort_string(lst):
    return sorted(lst, key=embedded_numbers)  # 将前面的函数作为key来排序


# todo image to video
def image_to_video(input_path: str, output_path: str, fps: int):
    filelist = os.listdir(input_path)
    filelist = sort_string(filelist)

    img = cv2.imread(os.path.join(input_path, filelist[0]))
    # 获取图片尺寸
    imgInfo = img.shape
    size = (imgInfo[1], imgInfo[0])
    print(size)

    # fps = 30  # 视频每秒组成的原始帧数，尽量保持与原始视频一致
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 设置视频编码格式 XVID -> avi
    video = cv2.VideoWriter(output_path, fourcc, fps, size)
    print('a')
    # 视频保存在当前目录下
    for item in filelist:
        if item.endswith('.jpg') or item.endswith('.JPG'):
            print(item)
            item = os.path.join(input_path, item)
            # 路径中若存在为中文名
            # img = cv2.imdecode(np.fromfile(item, dtype=np.uint8), 1)
            # 路径为英文名
            img = cv2.imread(item)
            video.write(img)

    video.release()
    cv2.destroyAllWindows()
    print('end')


def image_to_gif(input_path: str, output_path: str):
    filelist = os.listdir(input_path)
    image_files = sort_string(filelist)

    # 打开第一张图片，以便获取图像尺寸
    with Image.open(os.path.join(input_path, image_files[0])) as first_image:
        # 创建一个新的 GIF 图像，并设置帧速率和循环次数
        gif_image = Image.new('RGB', first_image.size)
        gif_image_info = first_image.info
        gif_image_info['duration'] = 500  # 每帧显示的时间（毫秒）
        gif_image_info['loop'] = 0  # 循环次数（0 表示无限循环）

        # 打开每个图片文件并将其添加到 GIF 图像中
        frames = []
        for image_file in image_files:
            item = os.path.join(input_path, image_file)
            with Image.open(item) as image:
                frames.append(image.convert('RGB'))

        # 将图像列表作为帧添加到 GIF 图像中
        gif_image.save(output_path, save_all=True, append_images=frames, **gif_image_info)


def convert_images_to_gif(input_path: str, output_path: str, duration: int = 200):
    """
    图片转gif
    :param input_path: 输入图片路径
    :param output_path: 输出gif路径
    :param duration: 每一帧之间的延迟时间（毫秒）
    :return:
    """
    image_list = sort_string(os.listdir(input_path))
    images = []
    for path in image_list:
        item = os.path.join(input_path, path)
        img = Image.open(item)
        images.append(img)

    images[0].save(output_path, format='GIF', append_images=images[1:], save_all=True, duration=duration, loop=0)



if __name__ == '__main__':
    input_path = '/Users/admin/Desktop/temp/gif2'
    output_path = '/Users/admin/Desktop/temp/2.gif'
    convert_images_to_gif(input_path, output_path, 200)
    # image_to_gif(input_path, output_path)
    # image_to_video(input_path, output_path, 30)
