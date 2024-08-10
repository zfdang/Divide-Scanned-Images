"""
File: run.py
Author: Zhengfa Dang
Description: This script divides scanned images into multiple smaller images based on specified minimum width and height.

CMD to remove all generated crop images: 
$ find . -name "*-Crop-*" -type f -exec rm -f {} \;
"""

import os
import cv2
import piexif
import re
import argparse


image_min_width = 500
image_min_height = 500


def iterate_image_files(target_directory):
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                # process each image file
                process_image(root, file)


def process_image(root, file):
    # Split the file name into prefix and suffix
    file_name = os.path.splitext(file)[0]
    file_suffix = os.path.splitext(file)[1]

    # Find the last part of the root path, we expect this to be the creation year of the image
    root_parts = root.split(os.path.sep)
    last_part_of_root = root_parts[-1]

    # now to process the image
    image_path = os.path.join(root, file)

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found")

    # divide the image
    # https://learnopencv.com/contour-detection-using-opencv-python-c/
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, thresh = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # res_image = cv2.drawContours(image, cnts, -1, (255,0,0), 3)
    # cv2.imshow('res_image', res_image)
    # cv2.waitKey(0)

    # Iterate through contours and filter for crop image
    image_number = 0
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w < image_min_width or h < image_min_height:
            continue
        # cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
        cropimage = original[y:y + h, x:x + w]
        cropfile = "{}-Crop-{}{}".format(file_name, image_number, file_suffix)
        cv2.imwrite(os.path.join(root, cropfile), cropimage)

        # Modify the EXIF information of the cropfile
        if re.match(r"\d{4}$", last_part_of_root):
            exif_dict = piexif.load(os.path.join(root, cropfile))
            # Set the creation date to the last part of the root path
            exif_dict["0th"][piexif.ImageIFD.DateTime] = "{}:06:01 00:00:00".format(last_part_of_root)
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, os.path.join(root, cropfile))

        image_number += 1

    print("{}: {} images detected".format(image_path, image_number))

    # Display the detected results
    # cv2.imshow('image', image)
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()


def main():
    global image_min_width, image_min_height
    image_width = input("Enter the minimum width of detected image (default = 500):")
    if len(image_width) > 0:
        image_min_width = int(image_width)

    image_height = input("Enter the minimum height of detected image (default = 500): ")
    if len(image_height) > 0:
        image_min_height = int(image_height)

    target_directory = input("Enter the path to your target directory (default = ./images) : ")
    if len(target_directory) == 0:
        target_directory = "./images/"

    iterate_image_files(target_directory)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Divide scanned images into multiple smaller images")
    parser.add_argument("-c", "--clean", action="store_true", help="Remove all generated crop images")
    args = parser.parse_args()

    if args.clean:
        target_directory = input("Enter the path to your target directory (default = ./images) : ")
        if len(target_directory) == 0:
            target_directory = "./images/"

        # CMD to remove all generated crop images
        cmd = "find " + target_directory + " -name \"*-Crop-*\" -type f -exec rm -f {} \;"
        print("CMD: {}".format(cmd))
        os.system(cmd)
        print("All generated crop images have been removed.")
        exit(0)

    main()
