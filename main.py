import requests
import os
from zipfile import ZipFile
from PIL import Image
import tempfile
import shutil

def download_yandex_disk_folder(yandex_disk_link, temp_folder, oauth_token):
    response = requests.get(
        yandex_disk_link,
        headers={"Authorization": f"OAuth {oauth_token}"}
    )
    download_link = response.json()["href"]

    response = requests.get(download_link)
    zip_file_path = os.path.join(temp_folder, "yandex_disk_folder.zip")

    with open(zip_file_path, 'wb') as zip_file:
        zip_file.write(response.content)

    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)


    os.remove(zip_file_path)

def load_images_from_folder(folder_path):
    images = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(root, filename)
                print(f"Loading image from: {img_path}")
                img = Image.open(img_path)
                images.append(img)
    return images


def choose_subfolder(temp_folder):
    base_folder = os.path.join(temp_folder, "Для тестового")

    subfolders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    if not subfolders:
        print("В папке пусто.")
        return None

    print("Доступные папки:")
    for i, subfolder in enumerate(subfolders, 1):
        print(f"{i}. {subfolder}")

    choice = input("Введите номер папки: ")

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(subfolders):
            return os.path.join(base_folder, subfolders[choice_index])
        else:
            print("Введите корректный номер папки")
    except ValueError:
        print("Пожалуйста введите число")

    return None


def merge_images(images, output_path, images_per_row=4, padding=50, margin=50):
    if not images:
        print("В папке нет изображений.")
        return

    widths, heights = zip(*(i.size for i in images))

    max_height = max(heights)


    rows = len(images) // images_per_row + (len(images) % images_per_row > 0)
    total_width = images_per_row * max(widths) + (images_per_row - 1) * padding + 2 * margin
    total_height = rows * max_height + (rows - 1) * padding + 2 * margin

    new_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

    x_offset, y_offset = margin, margin
    for img in images:
        new_image.paste(img, (x_offset, y_offset))
        x_offset += max(widths) + padding


        if x_offset > total_width - max(widths) - margin:
            x_offset = margin
            y_offset += max_height + padding

    new_image.save(output_path)

def main():
    yandex_disk_link = "https://cloud-api.yandex.net/v1/disk/public/resources/download/?public_key=https://disk.yandex.ru/d/739ZUqb_3G93qQ"
    temp_folder = tempfile.mkdtemp()
    oauth_token = "y0_AgAAAAASIiwOAAtd1wAAAAD8gH99AACVbkW5ivNAP5yd-gqMURYuuLsfng"
    download_yandex_disk_folder(yandex_disk_link, temp_folder, oauth_token)


    subfolder = choose_subfolder(temp_folder)

    if subfolder:
        output_path = r"C:\Users\Mike\PycharmProjects\test\Result.tif"
        images = load_images_from_folder(subfolder)
        merge_images(images, output_path)

    shutil.rmtree(temp_folder)

if __name__ == "__main__":
    main()