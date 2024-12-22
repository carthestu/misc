import time
from picamera2 import Picamera2
from PIL import Image
import numpy as np

def get_average_grayscale_values_and_modify_image(coordinates):
    # Initialize the Picamera2 object
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)
    
    # Start the camera and measure the capture time
    picam2.start()
    capture_start = time.time()
    image = picam2.capture_array()
    capture_end = time.time()
    picam2.stop()
    
    # Print the capture time
    print(f"Capture time: {capture_end - capture_start:.2f} seconds")
    
    # Convert the image array to a PIL Image
    pil_image = Image.fromarray(image)
    pixels = pil_image.load()
    
    # List to store the average grayscale values
    average_grayscale_values = []
    
    # Iterate over the coordinates to get the average grayscale values and modify pixels
    for coordinate in coordinates:
        x, y = coordinate
        total_red, total_green, total_blue = 0, 0, 0
        count = 0
        for i in range(-2, 3):
            for j in range(-2, 3):
                nx, ny = x + i, y + j
                if 0 <= nx < pil_image.width and 0 <= ny < pil_image.height:
                    red = int(image[ny, nx, 0])
                    green = int(image[ny, nx, 1])
                    blue = int(image[ny, nx, 2])
                    total_red += red
                    total_green += green
                    total_blue += blue
                    count += 1
                    pixels[nx, ny] = (255, 0, 0)
        avg_red = total_red / count
        avg_green = total_green / count
        avg_blue = total_blue / count
        average_grayscale = round((avg_red + avg_green + avg_blue) / 3)
        average_grayscale_values.append(average_grayscale)
    
    # Save the modified image as a JPEG
    pil_image.save("modified_image.jpg")
    
    return average_grayscale_values

# Example usage
coordinates = [[100, 100], [50, 200]]
average_grayscale_values = get_average_grayscale_values_and_modify_image(coordinates)
print(average_grayscale_values)
