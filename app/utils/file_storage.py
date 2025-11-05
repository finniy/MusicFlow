import os
import shutil
import uuid


def save_uploaded_file(src_path: str, dest_dir: str) -> str:
    os.makedirs(dest_dir, exist_ok=True)
    ext = os.path.splitext(src_path)[1]
    new_name = f"{uuid.uuid4()}{ext}"
    dest_path = os.path.join(dest_dir, new_name)
    shutil.copy(src_path, dest_path)
    return os.path.abspath(dest_path)


