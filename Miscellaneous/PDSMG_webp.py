import os
import shutil
from PIL import Image

def convert_and_organize():
    # 1. Ask the user for the folder path
    directory_path = input("Paste the full path to your image folder: ").strip()
    
    if not os.path.exists(directory_path):
        print("Error: That folder doesn't exist. Please check the path and try again.")
        return

    # 2. Ask the user ONLY for the event code and year
    event_suffix = input("Enter the event code and year (e.g., DP_25 or SP_26): ").strip()
    
    # 3. Lock in "PDSMG_" permanently and combine it with your input
    prefix = f"PDSMG_{event_suffix}"
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    original_folder = os.path.join(directory_path, "original")
    preview_folder = os.path.join(directory_path, "preview")
    
    os.makedirs(original_folder, exist_ok=True)
    os.makedirs(preview_folder, exist_ok=True)
    
    counter = 1
    
    for filename in os.listdir(directory_path):
        old_path = os.path.join(directory_path, filename)
        
        if not os.path.isfile(old_path):
            continue
            
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext in valid_extensions:
            # The new name will automatically format as PDSMG_SP_26-1, etc.
            new_base_name = f"{prefix}-{counter}"
            
            new_original_path = os.path.join(original_folder, f"{new_base_name}{file_ext}")
            new_webp_path = os.path.join(preview_folder, f"{new_base_name}.webp")
            
            try:
                shutil.move(old_path, new_original_path)
                
                with Image.open(new_original_path) as img:
                    img.save(new_webp_path, "webp", quality=80)
                    
                print(f"Processed: {filename} -> {new_base_name}")
                counter += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    print("\nAll done! Check your 'original' and 'preview' folders.")

if __name__ == "__main__":
    convert_and_organize()