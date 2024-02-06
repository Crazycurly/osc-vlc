import cv2
import numpy as np

# Video properties
width, height = 1920, 1080
fps = 30
duration = 10
font_scale = 10

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for i in range(1, 10):
    video = cv2.VideoWriter(f'{i}.mp4', fourcc, fps, (width, height))

    # Generate frames
    for j in range(fps * duration+1):
        # Create a black image
        img = np.zeros((height, width, 3), dtype=np.uint8)

        # Draw a circle with animation from small to big to small
        radius = int(abs(1100 * np.sin(j * 2 * np.pi / (fps * duration))))
        cv2.circle(img, (width // 2, height // 2), radius, (255, 255, 255), -1)

        # Draw a big number 1 in the middle
        cv2.putText(img, str(i), (width // 2 - font_scale*10, height // 2 + font_scale*10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 20)

        # Write the frame into the file
        video.write(img)

    # Release the VideoWriter
    video.release()
