import telebot
import requests
import psutil

OWM_API_KEY = "000be634412f078ad203b00957e74c50"
bot = telebot.TeleBot('6520477154:AAGFZiNMydPhX1KQIrUc7XDmR1fYvPKfTa0')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, я бот показываюший информация о погоде в городах,просто напиши свой после команды /search  ")

@bot.message_handler(commands=['search'])
def get_weather(message):
    try:
        city_name = message.text.split("/search ", 1)[1].capitalize()
        server = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&appid={OWM_API_KEY}&units=metric"
        response = requests.get(server)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            
            answer = f"Погода в городе {city_name}:\n"
            answer += f"Температура: {temperature}°C\n"
            answer += f"Давление: {pressure} гПа\n"
            answer += f"Влажность: {humidity}%\n"
            answer += f"Осадки: {description}\n"
            answer += f"Скорость ветра: {wind_speed} м/c"
        else:
            answer = "Данный город не найден"
    except IndexError:
        answer = "Пожалуйста, укажите название города после команды /search."
    except requests.exceptions.ReadTimeout:
        print("Извините, не удалось получить данные о погоде. Пожалуйста, попробуйте еще раз позже.")
    except Exception as e:
        answer = f"Произошла ошибка: {str(e)}"
    
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['bat'])
def send_battery_status(message):
    battery = psutil.sensors_battery()
    if battery:
        bot.send_message(message.chat.id, f"Процент заряда батареи: {battery.percent}%")
    else:
        bot.send_message(message.chat.id, "Информация о батарее недоступна")

bot.polling()