from picamera2 import Picamera2
from PIL import Image
import numpy as np

def get_average_grayscale_values(coordinates):
    # Initialize the Picamera2 object
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()
    
    # Capture an image and store it in an array
    image = picam2.capture_array()
    
    # Convert the image array to a PIL Image
    pil_image = Image.fromarray(image)
    pixels = pil_image.load()
    
    # List to store the average grayscale values
    average_grayscale_values = []
    
    # Iterate over the coordinates to get the average grayscale values
    for coordinate in coordinates:
        x, y = coordinate
        total_red, total_green, total_blue = 0, 0, 0
        count = 0
        
        # Iterate over the 5x5 neighborhood
        for i in range(-2, 3):
            for j in range(-2, 3):
                nx, ny = x + i, y + j
                if 0 <= nx < pil_image.width and 0 <= ny < pil_image.height:
                    red = int(image[ny, nx, 0])   # Red value
                    green = int(image[ny, nx, 1]) # Green value
                    blue = int(image[ny, nx, 2])  # Blue value
                    total_red += red
                    total_green += green
                    total_blue += blue
                    count += 1
        
        # Calculate the average grayscale value
        avg_red = total_red / count
        avg_green = total_green / count
        avg_blue = total_blue / count
        average_grayscale = round((avg_red + avg_green + avg_blue) / 3)
        
        # Append the average grayscale value to the list
        average_grayscale_values.append(average_grayscale)
        
        # Change the center pixel to bright red
        pixels[x, y] = (255, 0, 0)
    
    # Save the modified image as a JPEG
    pil_image.save("modified_image.jpg")
    
    picam2.stop()
    return average_grayscale_values

# Example usage
coordinates = [[100, 100], [50, 200]]
average_grayscale_values = get_average_grayscale_values(coordinates)
print(average_grayscale_values)
