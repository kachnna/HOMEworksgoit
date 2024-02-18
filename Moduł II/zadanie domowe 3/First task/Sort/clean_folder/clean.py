import os
import shutil
import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def replace_polish_char(text):
    polish_char = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
    normal_char = "acelnoszzACELNOSZZ"
    translation_table = str.maketrans(polish_char, normal_char)
    return text.translate(translation_table)


def normalize_file_name(filename):
    normalized_filename = replace_polish_char(filename)
    normalized_filename = re.sub(r'[^\w\ .]', '_', normalized_filename)
    return normalized_filename


def unpack_archevies(file_path):
    unpacked_files_dir = os.path.join(folder_path, "unpacked_files")
    os.makedirs(unpacked_files_dir, exist_ok=True)
    shutil.unpack_archive(file_path, unpacked_files_dir)

    for unpacked_root, _, unpacked_files_list in os.walk(unpacked_files_dir):
        for unpacked_filename in unpacked_files_list:
            normalize_unpacked_filename = normalize_file_name(
                unpacked_filename)
            if normalize_unpacked_filename != unpacked_filename:
                print(
                    f"Nazwa pliku została znormalizowana {unpacked_filename} na {normalize_unpacked_filename}")
            destination_folder = folder_path
            if destination_folder == folder_path:
                destination_folder = UNKNOWN_FOLDER
            for category, extensions in type_directories.items():
                if normalize_unpacked_filename.lower().endswith(extensions):
                    destination_folder = category
                    break
            destination_directory = os.path.join(
                folder_path, destination_folder)
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            shutil.move(
                os.path.join(unpacked_root, unpacked_filename),
                os.path.join(destination_directory,
                             normalize_unpacked_filename)
            )

    shutil.rmtree(unpacked_files_dir)


def process_files(root, files_list, folder_path):
    for filename in files_list:
        # normalizowanie nazwy pliku
        normalize_filename = normalize_file_name(filename)
        if normalize_filename != filename:
            print(
                f"Nazwa pliku została znormalizowana {filename} na {normalize_filename}")

        # file_path - ścieżka pliku
        file_path = os.path.join(root, filename)
        # file_extension - typ dokumentu np.: .mp3
        name, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()

        # Rozpakowanie i sortowanie plików w ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2')
        if file_extension in ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'):
            unpack_archevies(file_path)

        destination_folder = folder_path
        if destination_folder == folder_path:
            destination_folder = UNKNOWN_FOLDER

        for category, extensions in type_directories.items():
            if file_extension in extensions:
                destination_folder = category
                break

        # Tworzenie folderu jak nie istnieje
        destination_directory = os.path.join(folder_path, destination_folder)
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)  # tworzenie folderu

        # Przenoszenie pliku do odpowiedniego folderu
        shutil.move(file_path, os.path.join(
            destination_directory, normalize_filename))
        print(
            f"Plik {filename} został przeniesiony do folderu {destination_folder}")

    # Usuwanie folderu
    for root, dirs, files_list in os.walk(folder_path, False):
        for folder in dirs:
            directory_path = os.path.join(root, folder)
            # sprawdza czy jest lista plikami w danym folderze
            if not os.listdir(directory_path):
                # usuwanie os.rmidr - usuwa folder jedynie jak jest pusty
                os.rmdir(directory_path)
                print(f"Usunięto folder: {folder}")
    print("Pliki posortowane i nazwa plików znormalizowane")

    print("Aktualny status folderu")
    print(f"Ścieżka folderu: {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            files_in_subfolder = os.listdir(subfolder_path)
            print(f"Podfolder: {subfolder} ({len(files_in_subfolder)} pliki)")
            for file_in_subfolder in files_in_subfolder:
                print(f"- {file_in_subfolder}")


if len(sys.argv) != 2:
    print("Usage: clean-folder <folder_path>")
    sys.exit(1)

# Ścieżka
folder_path = Path(sys.argv[1])

# Słownik
type_directories = {
    'Audio': ('.mp3', '.wav', '.flac', '.ogg', '.amr'),
    'Images': ('.jpg', '.jpeg', '.png', '.gif'),
    'Documents': ('.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'),
    'Archives': ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'),
    'Video': ('.avi', '.mp4', '.mov', '.mkv')
}
UNKNOWN_FOLDER = "UNKNOWN"


def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        for root, dirs, files_list in os.walk(folder_path):
            executor.submit(process_files, root, files_list, folder_path)


if __name__ == "__main__":
    main()
