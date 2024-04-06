from PIL import Image
import math
from tqdm import tqdm
import sys

def calculate_entropy(histogram):
    """Calculates the Shannon entropy of a histogram.

    Args:
        histogram: A list of pixel counts.

    Returns:
        The Shannon entropy of the histogram (in bits).
    """
    total_pixels = sum(histogram)
    entropy = 0
    for count in histogram:
        if count > 0:
            probability = count / total_pixels
            entropy -= probability * math.log2(probability)
    return entropy

def calculate_entropy_map(image, kernel_size=3):
    """Calculates the entropy map of the given image using local histograms.

    Args:
        image: A PIL Image object.
        kernel_size: Size of the kernel for calculating local entropy.

    Returns:
        A 2D list representing the entropy map of the image.
    """
    width, height = image.size
    entropy_map = [[0 for _ in range(width)] for _ in range(height)]

    print("Calculating entropy map...")
    with tqdm(total=width * height, desc="Progress") as pbar:
        for y in range(height):
            for x in range(width):
                
                local_histogram = [0] * 256
                
                for ky in range(-kernel_size // 2, kernel_size // 2 + 1):
                    for kx in range(-kernel_size // 2, kernel_size // 2 + 1):
                        
                        new_x = (x + kx) % width
                        new_y = (y + ky) % height
                        
                        pixel_value = image.getpixel((new_x, new_y))
                        grayscale_value = int(0.21 * pixel_value[0] + 0.72 * pixel_value[1] + 0.07 * pixel_value[2])
                        local_histogram[grayscale_value] += 1   
                        
                
                entropy_map[y][x] = calculate_entropy(local_histogram)
                pbar.update(1)
    return entropy_map

def modify_image_based_on_entropy(image, entropy_map):
    """Modifies the image based on the entropy map.

    Args:
        image: A PIL Image object.
        entropy_map: A 2D list representing the entropy map of the image.

    Returns:
        A modified PIL Image object.
    """
    width, height = image.size
    modified_image = Image.new(image.mode, image.size)

    print("Modifying image based on entropy...")
    with tqdm(total=width * height, desc="Progress") as pbar:
        for y in range(height):
            for x in range(width):
                current_pixel_value = image.getpixel((x, y))
                entropy = entropy_map[y][x]
                new_pixel_value = tuple([(channel + int(entropy * 10)) % 256 for channel in current_pixel_value])
                modified_image.putpixel((x, y), new_pixel_value)
                pbar.update(1)

    return modified_image



def main():
    
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    image = Image.open(image_path)
    entropy_map = calculate_entropy_map(image)
    modified_image = modify_image_based_on_entropy(image, entropy_map)
    current_file_name = image_path.split("\\")[-1].split(".")[0]
    modified_image_path = image_path.split(".")[0] + f"{current_file_name}_modified.png"        
    modified_image.show()
    modified_image.save(modified_image_path)

if __name__ == "__main__":
    main()
