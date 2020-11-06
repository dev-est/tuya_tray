# Tuya Tray

Tuya Tray is an application utilising the Tuya API to automatically create a taskbar application to control SmartLife/Tuya lights.


### Installation

Tuya Tray requires [Python 3](https://www.python.org/downloads/) to run.

Install the requirements and run the script.

```sh
$ pip install -r requirements.txt
$ python tuya-tray.py
```

You will also need to alter the config.json file with the following:
 1. Your Tuya/SmartLife login and password so it looks like this {"username":"example@domain.com","password":"YOURPASS"...}
 2. Your country code ("44" for UK users, "1" for US/Canadian users, etc)
 3. The application you're using ('tuya' for tuya users and 'smart_life' for smart life users)

```
{"username":"example@domain.com","password":"YOURPASS","country_code":"44","application":"tuya"}
```
### In Action!

![Gif](https://i.imgur.com/YdeAgh4.gif)





### Todos

 - Implement colour wheel to lights
 - Light percentages (25,50,75)
