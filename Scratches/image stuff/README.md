# Instructions for Segmentation App
_by Miles Robertson, SDL, July 29th 2020 -- Miles.Robertson@sdl.usu.edu_

# 
## Checking COCO Segmentation

- No matter the quantity of pictures you wish to examine, you must provide the COCO data set. 
    - Note that only polygonal segmentation data (`"iscrowd" = 0`) can be displayed, not RLE segmentation data (`"iscrowd" = 1`). This data can be visualized by using the poorly-developed program in the _Extra_ folder.
- If you want to check a single file, either select its location via the __pick file__ button, or type in the image's corresponding photo id according to the attached COCO data set.
    - Accessing photos by photo id is only available for url images.
- If you want to check all the pictures of the COCO data set, check the corresponding checkbox to enable the __pick folder__ button to point the program towards the pictures.
    - Alternatively, if all the images are catalogued by URL and you wish to check all images, 
- After entering the needed information, press the __Start__ button.
- Some rudamentary mistakes are accompanied by warning labels and a program crash. The rest are likely to crash without explanation.
- The utility of key presses are identified underneath the image.

### Example 1

Open the included `Example.json` file. Identify the photo id of the only image there (in this case, `289343`). Type or paste it into the photo id text box. Select `Example.json` for the COCO data option. Hit start. You will see the image appear with segmentation data and small labels. The color can be changed by pressing "c" if the masks are not clearly visible. Hit "p" to progress (aka close).

### Example 2

Note: This example will appear identical to the one above unless Example 1 or 2 of the following section is completed first.

Only attach the `Example.json` file for the COCO data option. Hit start. You will receive an information message but just hit OK and it will continue. Now, when you hit "p", the program will progress from one image to the next in the COCO data set. Note that this example only works if all the pictures are linked by URL.

# 
## Making COCO Segmentation

- No matter the quantity of pictures you wish to examine, you must provide the COCO data set. 
    - Note that only polygonal segmentation data (`"iscrowd" = 0"`) can be created, not RLE segmentation data (`"iscrowd" = 1"`).
- Checking a single file can be done by picking a file or including a photo URL. This image does not have to be included in the COCO data set before running for this to be successful.
- If you want to segment many images by the same category, click the corresponding checkbox and select the folder that contains the images. 
    - Note that the folder can only contain images.
- Select a COCO data set and type in a category. The category must be included in the COCO data set for success (see Example 2 below).

### Example 1

Add this URL to the entry box: https://storage.googleapis.com/petbacker/images/blog/2017/dog-and-cat-cover.jpg

If the URL above is broken by the time you use it, find another URL that points to a picture of a dog and a cat, and use it instead.

Select `Example.json` for the COCO data set, and enter "dog" as the category. Hit start. Follow the instructions, and press "p" when the outlining of the dog is completed. Successful segmentation can be verified using the _Check COCO Segmentation_ option.

### Example 2

Open the `Example.json` file for editing. Add the following to the _categories_ section in any position, including appropriate commas before/after the addition:
```
{
    "supercategory": "animal",
    "id": 19,
    "name": "cat"
}
```
After saving, this category will be accessible for segmentation.

Add the same URL from Example 1 to the entry box.

Select `Example.json` for the COCO data set, and enter "cat" as the category. Hit start. Follow the instructions, and press "p" when the outlining of the cat is completed. Successful segmentation can be verified using the _Check COCO Segmentation_ option. Note that if Example 1 and 2 has been completed correctly, both the dog and the cat have masks.