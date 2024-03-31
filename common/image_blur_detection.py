from imutils import paths
import cv2

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

def process_images(image_path, threshold=100.0):
    # loop over the input images
    result = []
    for imagePath in paths.list_images(image_path):
        # load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian
        # method
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        text = "Not Blurry"
        blur = False
        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        if fm < threshold:
            text = "Blurry"
            blur = True


        # Add a delay and check for a key event
        key = cv2.waitKey(0)  # Change the delay time as needed

        # Check if the 'Esc' key is pressed (ASCII code 27)
        if key == 27:
            break
        result.append({
            'frame': imagePath,
            'blur': blur
        })
    cv2.destroyAllWindows()  # Close all OpenCV windows when the script ends
    return result

def detect_img_blur(image_path) -> bool:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    return fm < 100.0

if __name__ == "__main__":
    out = process_images("images", 100.0)
    print(out)