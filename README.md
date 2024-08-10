# Divide Scanned Images

自动分割扫描的图片

This script divides scanned images into multiple smaller images based on specified minimum width and height.

## Usage

1. Install the required dependencies:
    ```
    pip install opencv-python piexif
    ```

2. Place your scanned images in the target directory.

3. Run the script:
    ```
    python run.py
    ```

4. Follow the prompts to specify the minimum width and height of the detected images, as well as the target directory.

5. The script will process the images and generate cropped images in the target directory.

6. The EXIF information of the cropped images will be modified to include the creation date based on the last part of the root path.

7. The script will display the number of images detected and cropped for each input image.

8. To remove all generated crop images, run the following command:

    ```
    python run.py --clean
    ```

## Requirements

- Python 3.6 or higher
- OpenCV (cv2)
- piexif

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
