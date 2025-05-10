import os
from PIL import Image
import random


class FacePictureService():
    
    def save_image(self, file, name):

        rand_name = random.randint(1, 100)
        
        pil_image = Image.open(file)
        pil_image = pil_image.convert('RGB')
        
        current_path = os.path.dirname(os.path.dirname(__file__))
        root_project = current_path.removesuffix("/infrastructure/face")
        storage_path = os.path.join(root_project, "storage/face/")
        
        # if not os.path.exists(storage_path):
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        image_path = os.path.join(storage_path, name)
        
        pil_image.save(image_path)
        
        return image_path

        
    def delete_image(self, file_path):

        # print(f"Attempting to delete files in: {file_path}")
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
                # print(f"Deleted file: {file_path}")
                return "File has been deleted."
            elif os.path.isdir(file_path):
                for filename in os.listdir(file_path):
                    file_path_to_delete = os.path.join(file_path, filename)
                    try:
                        if os.path.isfile(file_path_to_delete) or os.path.islink(file_path_to_delete):
                            os.unlink(file_path_to_delete)
                            # print(f"Deleted file: {file_path_to_delete}")
                        # Skip subdirectories
                    except Exception as e:
                        print(f"Failed to delete {file_path_to_delete}. Reason: {e}")
                        return f"Failed to delete {file_path_to_delete}. Reason: {e}"
                print(f"All files in the directory {file_path} have been deleted, but the directory is kept.")
                return "All files in the directory have been deleted, but the directory is kept."
        else:
            print(f"The file or directory {file_path} is not found.")
            return "The file or directory is not found."

