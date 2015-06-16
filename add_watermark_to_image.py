#!/usr/bin/env python

import argparse
import os

__info__ = {
	'title': "Add a watermark to an image",
    'description': "Add a watermark to an image",
    'url': "http://github.com/TonkWorks/watermark_on_an_image/archive/master.zip",
    'input': [
        {
            'label': 'Image / Images to put watermark on',
            'type': 'file',
            'map': 'image',
        },
        {
            'label': 'Watermark',
            'type': 'file',
            'map': 'watermark',
        }
    ]
}

def script():
    from PIL import Image

    parser=argparse.ArgumentParser()
    parser.add_argument('--image')
    parser.add_argument('--watermark')

    args=parser.parse_args()
    image = args.image
    image_file_name = os.path.basename(image)

    watermark = args.watermark

    image = Image.open(image)
    mark = Image.open(watermark)
    image = make_watermark(image, mark, (100, 100), 0.5)


    image.save(image_file_name, "JPEG")


#http://code.activestate.com/recipes/362879/
def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    from PIL import ImageEnhance

    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def make_watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    from PIL import Image

    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)


if __name__ == '__main__':
	script()
