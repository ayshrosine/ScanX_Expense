import cv2 
import os 

input_folder = 'bill_images'
output_folder = 'image_cleaning_one_folder' 

def image_cleaning(input_folder, output_folder):
    valide_extension = ( '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    converted_images = 0


    # telling  which folder to read the images from and which folder to save the cleaned images
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valide_extension):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try: 
                color_image = cv2.imread(input_path)

                #converting  the color image to grayscale / black and white image
                gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

                # removing  noise from the image using Gaussian blur
                blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

                #otsu's  binarization method to convert the image to binary
                ret , binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                cv2.imwrite(output_path, binary_image)
                converted_images += 1
                print(f"Converted {filename} to black and white and saved to {output_path}")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
      image_cleaning(input_folder, output_folder)

