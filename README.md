# API Управления камерой

Для установки приложения воспользуйтесь инструкцией https://bit.ly/2KnRY4f

API работает при помощи https://github.com/quatanium/python-onvif

## Конфигурация подключения к камере

Для настройки необходимо в файле app.py в конструкторе PtzCam заменить на нужные ip-адрес, порт, логин, пароль и путь до файлов wsdl в методе __get_camera()

```
def _get_camera():
    try:
        cam = getattr(g, '_cam', None)
        if cam is None:
            cam = g._cam = PtzCam('192.168.1.110', 8999, 'admin', '', '/home/pi/camApi/venv/wsdl/')
            # cam = g._cam = PtzCam('85.12.222.142', 8999, 'admin', '', '/Users/vagano/PycharmProjects/camApi/venv/wsdl/')
        return cam
    except Exception as e:
        app.logger.error(str(e))
```

## Конфигурация словаря точек

Для отображения в пользовательском интерфейсе точек, настроенных на камере, в корректной форме необходимо заполнить  json-словарь в файле presets_dict.json в формате:

```
"CameraToken":{
    "ru":"Название на русском",
    "en":"Name in English"
  }
```

## Методы API

### GET /cam/api/get_presets_list/

Инициализирует подключение к камере и опрашивает ее на предмет наличия настроенных точек, настроенные точки сопоставляет со словарем и возвращает пересечение в формате:

```
IntegerToken:{
                    "token_name": token_name,
                    "name_ru": "Название на русском",
                    "name_en": "Name in English"
                }
```

### GET /cam/api/move_to_preset/<int:token>

Отправляет камере команду повернуться к пресету №token.
