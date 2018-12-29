import pygame as pg


def load_images(img_locs, scale_factor=None):
    """Loads and scales the images found in `img_locs`."""
    images = [pg.image.load(img_loc) for img_loc in img_locs]
    if scale_factor:
        images = [pg.transform.scale(img, (img.get_width() * scale_factor,
                                           img.get_height() * scale_factor))
                  for img in images]
    # Assert all images have the same dimensions.
    assert(all(map(lambda i: i.get_width() == images[0].get_width() and i.get_height() == images[0].get_height(), images)))
    return images
