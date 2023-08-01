from PIL import Image
import os

def split_movie_photo_to_one_phone(path,start=0,end=0, isShowLast=False, outputPath='./result/'):
    # 获取目录下所有文件
    files = os.listdir(path)
    # 遍历文件, 按照文件的时间倒序排列
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    images = []
    i = 0
    for file in files:
        # 截取从第二张开始的图片
        # 只保留从底部100像素开始，到200像素结束的图片
        if i==0:
            img = Image.open(path + file)
            images.append(img)
            i = i+1
            continue
        if isShowLast:
            if i == len(files)-1:
                img = Image.open(path + file)

                images.append(img)
                i = i+1
                continue
        
        img = Image.open(path + file)
        img = img.crop((0, start, img.width, end))
        # 如果出现了重复的图片，就不添加到images中
        if len(images) > 0:
            if images.__contains__(img):
                continue
        images.append(img)
        i = i+1
    # 将第一张图片和images中的图片合并
    # images中的图片拼接到第一张图片的下方
    # 创建一个新的图片，大小为第一张图片的大小 + (images中图片的数目-1)*100
    image1 = images[0]
    imageEnd = images[len(images)-1]
    step = end-start
    new_image = None
    if isShowLast:
        new_image = Image.new('RGB', (image1.width, image1.height + (len(images)-2)*step+imageEnd.height))
        # 将第一张图片放到新图片的最上方
        new_image.paste(image1, (0, 0))
        # 将images中的图片依次放到新图片中
        for i in range(1, len(images)-1):
            new_image.paste(images[i], (0, image1.height + i*step))
        new_image.paste(imageEnd, (0, image1.height + (len(images)-2)*87))
    else:
        new_image = Image.new('RGB', (image1.width, image1.height + (len(images)-1)*step))
        # 将第一张图片放到新图片的最上方
        new_image.paste(image1, (0, 0))
        # 将images中的图片依次放到新图片中
        for i in range(1, len(images)):
            new_image.paste(images[i], (0, image1.height + i*step))
    # 保存图片
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    new_image.save(outputPath + path.split('/')[-2] + '.jpg')
    print('图片合并完成')
    
 
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 读取 合并 目录下的所有文件夹
    path = './合成/'
    dirs = os.listdir(path)
    for dir in dirs:
        print(dir)
        split_movie_photo_to_one_phone(path+dir+'/',1413,1500, isShowLast=False, outputPath='./result2/')
    print('全部完成')


 