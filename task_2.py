import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO


def get_cat():
    url = "https://api.thecatapi.com/v1/images/search"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        img_url = data[0]['url']
        show_image_from_url(img_url)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить фото кота.\n{e}")


def get_dog():
    url = "https://dog.ceo/api/breeds/image/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        img_url = data['message']
        show_image_from_url(img_url)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить фото собаки.\n{e}")


def show_image_from_url(img_url):
    try:
        img_response = requests.get(img_url)
        img_response.raise_for_status()

        img_data = img_response.content
        img = Image.open(BytesIO(img_data))

        max_size = (400, 400)
        img.thumbnail(max_size)

        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось отобразить изображение.\n{e}")


root = tk.Tk()
root.title("Коты и Собаки")

btn_cat = tk.Button(root, text="Получить кота", command=get_cat, width=20, font=("Arial", 14))
btn_cat.pack(pady=10)

btn_dog = tk.Button(root, text="Получить собаку", command=get_dog, width=20, font=("Arial", 14))
btn_dog.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()