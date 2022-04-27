import cv2
import numpy as np

diff_threshold = 1000000

def process_image(image_file:str):
    image = cv2.imread(image_file)

    # convert to grayscale and blur the image to factor out unneeded data
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.blur(image, (20, 20))
    
    cv2.imwrite(image_file.replace('.','_proc.'), image)
    return image

previous_processed_image = process_image('bat1.jpg')
processed_image = process_image('bat2.jpg')

images_diff = cv2.absdiff(previous_processed_image, processed_image)
diff_score = np.sum(images_diff)

if diff_score > diff_threshold:
    # processed_image is a numpy array :)
    print(f'Motion Detected:{processed_image}\tDiff Score:{diff_score}')