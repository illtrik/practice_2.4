import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = '4bb1db1ec6f0d30295bfb3fd59ed6aa1'

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        icon_code = data['weather'][0]['icon']
        description = data['weather'][0]['description']
        return temp, icon_code, description
    except requests.RequestException:
        messagebox.showerror("Ошибка", "Проблемы с интернет-соединением или API.")
    except KeyError:
        messagebox.showerror("Ошибка", "Город не найден или ошибка данных от API.")
    return None, None, None


def show_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Внимание", "Пожалуйста, введите название города.")
        return

    temp, icon_code, description = get_weather(city)
    if temp is not None:
        temp_label.config(text=f"Температура в городе {city}: {temp}°C\n{description.capitalize()}")

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            icon_response.raise_for_status()
            icon_img_data = icon_response.content
            image = Image.open(BytesIO(icon_img_data))
            photo = ImageTk.PhotoImage(image)
            icon_label.config(image=photo)
            icon_label.image = photo
        except:
            icon_label.config(image='')
            icon_label.image = None
    else:
        temp_label.config(text="")
        icon_label.config(image='')
        icon_label.image = None


root = tk.Tk()
root.title("Погода в городе")

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

get_weather_button = tk.Button(root, text="Узнать погоду", command=show_weather)
get_weather_button.pack(pady=5)

temp_label = tk.Label(root, font=("Arial", 16))
temp_label.pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack()

root.mainloop()