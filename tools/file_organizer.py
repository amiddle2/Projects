from pathlib import Path
import shutil

file_path = input("Enter filepath of folder to be organized: ")
BASE_DIR = Path(file_path) 


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
}

def get_category(file_path: Path) -> str:
    for category, extensions in FILE_TYPES.items():
        if file_path.suffix.lower() in extensions:
            return category
    return "Others"

def organize_files(base_dir: Path):
    for item in base_dir.iterdir():
        if item.is_file():
            category = get_category(item)
            target_dir = base_dir / category
            target_dir.mkdir(exist_ok=True)

            destination = target_dir / item.name
            shutil.move(str(item), str(destination))

if __name__ == "__main__":
    organize_files(BASE_DIR)
    print("Files organized successfully!")
