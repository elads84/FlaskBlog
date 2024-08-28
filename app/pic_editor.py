from PIL import Image
from random import choice
import string
import os


def resize_image(image_path: str, width: int):
    # Open an image file
    with Image.open(image_path) as img:
        # Calculate the height using the aspect ratio
        ratio = width / img.width
        height = int(img.height * ratio)

        # Resize the image
        resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Save the resized image
        resized_img.save(image_path)


def create_image_name(ext, length):
    options = string.ascii_letters + string.digits
    result = ""
    for i in range(length):
        result += choice(options)
    return f"{result}.{ext}"


def create_unique_image_name(ext, length, destination: str):
    file_name = create_image_name(ext, length)
    while os.path.exists(os.path.join('static', destination, file_name)):
        file_name = create_image_name(ext, length)
    return file_name


def set_photo(file, app, size: str, destination: str, unique=True):
    extension = file.filename.split(".")[-1]
    file_name = create_unique_image_name(extension, 12, destination)

    # Ensure the upload folder exists
    upload_folder = os.path.join(app.root_path, 'static', destination)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file_name)
    file.save(file_path)

    resize_image(file_path, app.config[size])

    return f'/static/{destination}/' + file_name


def delete_file(file_name):
    try:
        file_name = file_name[1:] if file_name.startswith('/') or file_name.startswith('\\') else file_name
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name))
    except Exception as e:
        print(e)
        return False
    else:
        return True
# TODO: add logging!
