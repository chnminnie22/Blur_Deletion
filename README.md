# Blur_Deletion

Blur Deletion is a photo library cleanup tool, focusing on specifically photos that are blurry or out of focus. This tool has two main components:
1. Detecting blurry images
2. Deleting images selected by the user
Users are able to choose if they want to keep or delete images from the blurry photos that are detected, streamlining the process of gallery cleanup. 

This package depends on OpenCV, NumPy, and Matplotlib.

The script `blurDelete.py` contains the main code necessary to perform the Blur Deletion function. To pass in a photo library as input, run the following line with your path:

```# run on a directory of images
python blurDelete.py -i <input_directory>/ 
```

Once this is run, the code processes the images, determines which images are blurry, and successively displays them in order of decreasing blurriness. Users have several key options on what they want to do with the image or how to proceed. Pressing the keys below perform their own respective functions. Some may display confirmation messages on the terminal. Any other key selected during the image selection process will not select the image for deletion and instead will move on to the next image.

`d`: selects the image displayed for deletion
`a`: deletes all the images that have been selected by the algorithm
  * Confirmation message ensuring you want to delete all photos, including ones that have not been displayed yet.
    * `y`: will perform functions as stated above
    * `n`: abandons the delete-all and proceeds as normal with the next image
`s`: deletes only the images that have been selected and keeps the rest in their original directory

At the end of the image selection, the selected images will be displayed in a list, followed by a confirmation to delete all photos listed. If “y” is pressed, the photos will be deleted from the original image directory provided.
