"""
File: stanCodoshop.py
Name: 
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    return ((red-pixel.red)**2+(green-pixel.green)**2+(blue-pixel.blue)**2)**0.5


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    avg_red, avg_green, avg_blue = 0, 0, 0
    for ele in pixels:
        avg_red += ele.red
        avg_green += ele.green
        avg_blue += ele.blue
    return [avg_red//len(pixels), avg_green//len(pixels), avg_blue//len(pixels)]


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance",
    which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    avg_rgb = get_average(pixels)
    # avg_rgb == [avg_rgb.red, avg_rgb.green, avg_rgb.blue]
    color_distance = [(ele, get_pixel_dist(ele, avg_rgb[0], avg_rgb[1], avg_rgb[2])) for ele in pixels]
    # color_distance == [(pixel_1, distance_1), (pixel_2, distance_2) ... ]
    return sorted(color_distance, key=lambda t: t[1])[0][0]


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    
    # ----- YOUR CODE STARTS HERE ----- #
    # Write code to populate image and create the 'ghost' effect
    compare_pixels = []
    for x in range(result.width):
        for y in range(result.height):
            result_pixel = result.get_pixel(x, y)
            for img in images:
                compare_pixels.append(img.get_pixel(x, y))
            result_pixel.red = get_best_pixel(compare_pixels).red
            result_pixel.green = get_best_pixel(compare_pixels).green
            result_pixel.blue = get_best_pixel(compare_pixels).blue
            compare_pixels = []

    # ----- YOUR CODE ENDS HERE ----- #

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dire):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dire):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dire, filename))
    return filenames


def load_images(dire):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dire)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # # (provided, DO NOT MODIFY)
    # args = sys.argv[1:]
    # # We just take 1 argument, the folder containing all the images.
    # # The load_images() capability is provided above.
    # images = load_images(args[0])
    # solve(images)

    # # Below codes can compute all samples at once, each filename should be separated by a space.
    # # Ex : try "stanCodoshop.py hoover clock-tower math-corner monster" in terminal
    args = sys.argv[1:]
    for arg in args:
        # We just take 1 argument, the folder containing all the images.
        # The load_images() capability is provided above.
        images = load_images(arg)
        solve(images)


if __name__ == '__main__':
    main()
