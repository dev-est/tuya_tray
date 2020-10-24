# Tuya Tray

Tuya Tiktok is an application utilising the Tuya API to automatically create a taskbar application to control SmartLife/Tuya lights.


### Installation

TuyaTikTok requires [Python 3](https://www.python.org/downloads/) to run.

Install the requirements and run the script.

```sh
$ pip install -r requirements.txt
$ python tuya-tray.py
```
You will also need to alter the code in regards to the country code as well as the application you're using ('tuya' for tuya users and 'smart_life' for smart life users)

```sh
api.init(os.getenv('TUYA_LOGIN'),os.getenv('TUYA_PASSWORD'),"44","tuya")
```
### In Action!

![Gif](https://i.imgur.com/jM0mK28.gif)





### Todos

 - Implement colour wheel to lights
 - Light percentages (25,50,75)
