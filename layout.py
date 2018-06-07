from PIL import Image
import os
from functools import reduce
import math


class Layout:

    def __init__(self, images, working_d, output_path, process_id):
        """
        :param images: a list of dictionaries containing the image
            filepath,
            filename,
            extension,
            position

            # later added:
            height
            edited_filepath
        """
        self.fixed_images_dir = os.path.abspath(os.getcwd() + '{}image'.format(os.path.sep))

        self.images = images
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.output_path = output_path
        self.process_id = process_id
        self.MAX_WIDTH = 600
        self.directory = working_d + os.path.sep + '600'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_editied_image(self, image):
        try:
            i = Image.open(image['filepath'])
            i.thumbnail((self.MAX_WIDTH, self.MAX_WIDTH * i.height / i.width))
            image['height'] = i.height
            image['edited_filepath'] = '{}{}{}_{}_{}.png'\
                .format(self.directory,os.path.sep, image['position'], self.MAX_WIDTH, i.height)
            i.save(image['edited_filepath'])

        except IOError:
            print("cannot edit", image['filepath'])


class GridLayout(Layout):

    def __init__(self, images, working_d, output_path, process_id):
        super().__init__(images, working_d, output_path, process_id)
        self.main()

    def make_ad(self):
        """
        POSITION MAP:
        even numbers = l | odd numbers = r
        :return:
        """
        MARGIN = 15
        r = [i for i in self.images if i['position'] % 2]
        l = [i for i in self.images if not i['position'] % 2]
        r_sum = 0
        l_sum = 0
        if r:
            r_sum = reduce((lambda h1, h2: h1 + h2), [i['height'] for i in r])
        if l:
            l_sum = reduce((lambda h1, h2: h1 + h2), [i['height'] for i in l])

        # + l is bigger - r is larger
        difference = (l_sum + MARGIN * (len(l) - 1)) - (r_sum + MARGIN * (len(r) - 1))
        print("the difference", difference)
        ads = Image.new(mode='RGBA', size=(1230, (l_sum if r_sum < l_sum else r_sum) + 2 * MARGIN))
        ads.save('{}{}ads.png'.format(self.directory, os.path.sep))
        for i, x in zip(r, range(len(r))):
            image = Image.open(i['edited_filepath'])
            ads.paste(image,
                      (630, (
                              x * MARGIN
                              + (sum([i['height'] for i in r[0:x]]) if x > 0 else 0)
                              + ((x + 1) * math.floor(math.fabs(difference / (len(r) + 1)) if difference > 0 else 0))
                            )))

        for i, x in zip(l, range(len(l))):
            image = Image.open(i['edited_filepath'])
            ads.paste(image,
                      (0, (
                              x * MARGIN
                              + (sum([i['height'] for i in l[0:x]]) if x > 0 else 0)
                              + ((x + 1) * math.floor(math.fabs(difference / (len(l) + 1)) if difference < 0 else 0))
                            )))
        ads.save('{}{}ads.png'.format(self.directory, os.path.sep))

    def newsletter(self):
        ads = Image.open('{}{}ads.png'.format(self.directory, os.path.sep))
        head = Image.open('{}{}headT.png'.format(self.fixed_images_dir, os.path.sep))
        tail = Image.open('{}{}tailT.png'.format(self.fixed_images_dir, os.path.sep))
        size = (1300, ads.height + 600)
        nl = Image.new(mode='RGB', size=size, color='#E5DFD5')
        gb = self.make_repeated_background('{}{}bg.jpg'.format(self.fixed_images_dir, os.path.sep), size)
        gb.putalpha(50)
        nl.paste(gb, gb)
        nl.paste(head, (0, 0), head)
        # nl.paste(tail, (0, ads.height + 350), tail)
        nl.paste(ads, (35, 300), ads)
        nl.save(os.path.abspath(self.output_path) + '{}newsletter_{}.png'.format(os.path.sep, self.process_id))
        nl.show()

    def make_repeated_background(self, background_filepath, size):
        bg = Image.open(background_filepath)

        bg_w, bg_h = bg.size

        new_im = Image.new('RGB', size)

        w, h = new_im.size

        for i in range(0, w, bg_w):
            for j in range(0, h, bg_h):
                # bg = Image.eval(bg, lambda x: x + (i + j) / 1000)

                new_im.paste(bg, (i, j))
        return new_im

    def main(self):
        for i in self.images:
            self.save_editied_image(i)
        self.make_ad()
        self.newsletter()

