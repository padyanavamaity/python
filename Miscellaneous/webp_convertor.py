import os
import shutil
from PIL import Image

def convert_and_organize():
    # 1. Ask the user for the folder path and the new file prefix
    directory_path = input("Paste the full path to your image folder: ").strip()
    
    # Check if the path actually exists before continuing
    if not os.path.exists(directory_path):
        print("Error: That folder doesn't exist. Please check the path and try again.")
        return

    # Ask the user what prefix they want to use for this batch
    prefix = input("Enter the prefix for the new files (e.g., MyImage_Batch): ").strip()
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # 2. Create the new folders inside the target directory
    original_folder = os.path.join(directory_path, "original")
    preview_folder = os.path.join(directory_path, "preview")
    
    os.makedirs(original_folder, exist_ok=True)
    os.makedirs(preview_folder, exist_ok=True)
    
    counter = 1
    
    # 3. Loop through files in the directory
    for filename in os.listdir(directory_path):
        old_path = os.path.join(directory_path, filename)
        
        # Skip directories (like the 'original' and 'preview' folders)
        if not os.path.isfile(old_path):
            continue
            
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Check if the file is an image we want to convert
        if file_ext in valid_extensions:
            # Create the new file names using your custom prefix
            new_base_name = f"{prefix}-{counter}"
            
            new_original_path = os.path.join(original_folder, f"{new_base_name}{file_ext}")
            new_webp_path = os.path.join(preview_folder, f"{new_base_name}.webp")
            
            try:
                # 4. Move and rename the original file
                shutil.move(old_path, new_original_path)
                
                # 5. Open the moved original and save it as WebP with optimized quality
                with Image.open(new_original_path) as img:
                    img.save(new_webp_path, "webp", quality=80)
                    
                print(f"Processed: {filename} -> {new_base_name}")
                counter += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    print("\nAll done! Check your 'original' and 'preview' folders.")

# Run the program
if __name__ == "__main__":
    convert_and_organize()