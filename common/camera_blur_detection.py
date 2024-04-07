from imutils import paths
import cv2

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def process_camera( camera_ip="http://192.168.18.9:4747/video",threshold=100.0):
    # Open a connection to the camera (0 is usually the default camera)
    print(camera_ip)
    cap = cv2.VideoCapture(camera_ip)

    result = []
    frame_count = 0

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute the focus measure of the frame using the Variance of Laplacian method
        fm = variance_of_laplacian(gray)

        text = "Not Blurry"
        blur = False

        # If the focus measure is less than the supplied threshold,
        # then the frame should be considered "blurry"
        if fm < threshold:
            text = "Blurry"
            blur = True

        # Display the result on the frame (optional)
        cv2.putText(frame, "{}: {:.2f}".format(text, fm), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Result", frame)

        # Add the result to the list
        result.append({
            'frame_count': frame_count,
            'blur': blur
        })
        frame_count += 1

        # Add a delay and check for a key event
        key = cv2.waitKey(1)  # Change the delay time as needed

        # Check if the 'Esc' key is pressed (ASCII code 27)
        if key == 27:
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return result

if __name__ == "__main__":
    out = process_camera()
    print(out)
