from PIL import Image
import math
import os


MAX_WIDTH_IMAGE = 600


def max_width(imgs):
    newpath = imgs[0]['path'] + '/' + '600'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for img in imgs:
        try:
            i = Image.open(img['filepath'])
            i.thumbnail((MAX_WIDTH_IMAGE, MAX_WIDTH_IMAGE * i.height / i.width))
            i.save('{}/600_{}.png'.format(newpath, i.height))

        except IOError:
            print("cannot convert", img['filepath'])
    return newpath


# order images by height
def img_heights(a, newpath):

    for f in os.listdir(newpath):
        try:
            i = Image.open(newpath + '/' + f)
            a.append(i.height)
        except IOError:
            print("cannot open", f)
    a.sort()
    return a


def make_ads(newpath, imgs):
    pth = imgs[0]['path'] + '/'
    difference = [0, 0]
    r = []
    l = []
    heights = img_heights(a=[], newpath=newpath)
    r.extend([heights[4], heights[2]])
    l.extend([heights[0], heights[3], heights[1]])
    if sum(l) + 2 * 15 > sum(r) + 15:
        difference[0] = (sum(l) + 2 * 15 - sum(r) + 15) / 3
        ads = Image.new(mode='RGB', size=(1230, ((sum(l) + 2 * 15) + (math.ceil(difference[1] * 4)))), color='#E5DFD5')
        ads.save('{}/ads.png'.format(pth))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, l[0])), (0, math.floor(difference[1])))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, l[1])), (0, 2 * math.floor(difference[1]) + l[0] + 15))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, l[2])),
                  (0, 3 * math.floor(difference[1]) + l[0] + l[1] + 2 * 15))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, r[0])), (630, math.floor(difference[0])))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, r[1])), (630, 2 * math.floor(difference[0]) + r[0]))
        ads.save('{}/ads.png'.format(pth))
    else:
        difference[1] = (sum(r) + 15 - sum(l) + 2 * 15) / 4
        ads = Image.new(mode='RGB', size=(1230, ((sum(r) + 1 * 15) + (math.ceil(difference[0] * 3)))), color='#E5DFD5')
        ads.save('{}/ads.png'.format(pth))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, l[0])), (0, math.floor(difference[1])))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, l[1])), (0, 2 * math.floor(difference[1]) + l[0]))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, l[2])), (0, 3 * math.floor(difference[1]) + l[0] + l[1]))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, r[0])), (630, math.floor(difference[0])))
        ads.paste(Image.open('{}/600_{}.png'.format(newpath, r[1])), (630, 2 * math.floor(difference[0]) + r[0] + 15 ))
        ads.save('{}/ads.png'.format(pth))


def newsletter(output_path, process_id):
    ads = Image.open('image/proc_{}/ads.png'.format(process_id))
    head = Image.open('image/head.png')
    tail = Image.open('image/tail.png')
    nl = Image.new(mode='RGB', size=(1300, ads.height + 600) , color='#E5DFD5')
    nl.paste(head, (0, 0))
    nl.paste(tail, (0, ads.height+350))
    nl.paste(ads, (35, 300))
    nl.save(os.path.abspath(output_path) + '/newsletter_{}.png'.format(process_id))
    nl.show()


def main(output_path, imgs, process_id):
    for image in imgs:
        print(image)
        # {'path': '/home/gin/Desktop/pnu_news/image/proc_ab2ffd0f-68c6-4e28-8fa6-6da938081f3b', 'ext': '.jpg',
        # 'filepath': '/home/gin/Desktop/pnu_news/image/proc_ab2ffd0f-68c6-4e28-8fa6-6da938081f3b/49a238b5.jpg',
        # 'img_id': '49a238b5'}
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    newpath = max_width(imgs)
    make_ads(newpath, imgs)
    newsletter(output_path, process_id)
