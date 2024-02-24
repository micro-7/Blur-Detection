import cv2

def remove_blur_from_video(video_path, blur_frames_dict, output_path):
    '''removes blurry frames from video, based on the dictionary provided 
    {'frame_count': x, 'blur': False}
    '''
    cap = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if not blur_frames_dict[frame_count]['blur']:
            print(f"Frame {frame_count} is not blurry, keeping it")
            out.write(frame)
            cv2.imshow('frame', frame)
        else:
            print(f"Frame {frame_count} is blurry, removing it")

        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    cap.release()
    out.release()

    return output_path

if __name__ == "__main__":
    from blur_vid import process_video
    
    # Process the video to detect blurry frames
    out = process_video("videos/blurr2.mp4", 100.0)
    print(out) 
    
    # Remove blurry frames and save the processed video
    output_path = remove_blur_from_video("videos/blurr2.mp4", out, "videos/blurry_removedd.mp4")
    print("Output video saved at:", output_path)
