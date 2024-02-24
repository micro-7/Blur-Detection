import cv2 
from imutils import paths

def variance_of_laplacian(video):
    return cv2.Laplacian(video, cv2.CV_64F).var()

def process_video(video_path, threshold=100.0):
    # Open a connection to the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    result = []
    frame_count = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Break the loop if no frame is retrieved
        if not ret:
            break

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

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return result

if __name__ == "__main__":
    video_path =  "videos/Venice_5.mp4"
    out = process_video(video_path, 100.0)
    print(out)
