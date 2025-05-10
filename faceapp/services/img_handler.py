


import os

from django.conf import settings


async def handle_file_upload(file):
    file_name = file.name
    # Save the file
    local_storage_path = os.path.join(settings.BASE_DIR, 'storage', file_name)
    # Create storage if does not exist
    os.makedirs(os.path.dirname(local_storage_path), exist_ok=True)
    
    with open(local_storage_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return local_storage_path