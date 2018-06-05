from PIL import Image
import os
from functools import reduce


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
        self.fixed_images_dir = os.path.abspath('../../image')
        self.images = images
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.output_path = output_path
        self.process_id = process_id
        self.MAX_WIDTH = 600
        self.directory = working_d + '/' + '600'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_editied_image(self, image):
        try:
            i = Image.open(image['filepath'])
            i.thumbnail((self.MAX_WIDTH, self.MAX_WIDTH * i.height / i.width))
            image['height'] = i.height
            image['edited_filepath'] = '{}/{}_{}_{}.png'\
                .format(self.directory, image['position'], self.MAX_WIDTH, i.height)
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
        r = [i for i in self.images if i['position'] % 2]
        l = [i for i in self.images if not i['position'] % 2]
        r_sum = 0
        l_sum = 0
        if r:
            r_sum = reduce((lambda h1, h2: h1 + h2), [i['height'] for i in r])
        if l:
            l_sum = reduce((lambda h1, h2: h1 + h2), [i['height'] for i in l])

        ads = Image.new(mode='RGB', size=(1230, (l_sum if r_sum < l_sum else r_sum) + 2 * 15), color='#E5DFD5')
        ads.save('{}/ads.png'.format(self.directory))

        for i, x in zip(r, range(len(r))):
            print(i, x)
            ads.paste(Image.open(i['edited_filepath']),
                      (630, (x * 15 + sum([i['height'] for i in r[0:x]]) if x > 0 else 0)))

        for i, x in zip(l, range(len(l))):
            ads.paste(Image.open(i['edited_filepath']),
                      (0, x * 15 + sum([i['height'] for i in l[0:x]]) if x > 0 else 0))

        ads.save('{}/ads.png'.format(self.directory))

    def newsletter(self):
        ads = Image.open('{}/ads.png'.format(self.directory))
        head = Image.open('{}/head.png'.format(self.fixed_images_dir))
        tail = Image.open('{}/tail.png'.format(self.fixed_images_dir))
        nl = Image.new(mode='RGB', size=(1300, ads.height + 600), color='#E5DFD5')
        nl.paste(head, (0, 0))
        nl.paste(tail, (0, ads.height + 350))
        nl.paste(ads, (35, 300))
        nl.save(os.path.abspath(self.output_path) + '/newsletter_{}.png'.format(self.process_id))
        nl.show()

    def main(self):
        for i in self.images:
            self.save_editied_image(i)
        self.make_ad()
        self.newsletter()
