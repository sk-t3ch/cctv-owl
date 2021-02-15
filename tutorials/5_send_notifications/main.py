import requests 

payload = {
          "app_key": "APP_KEY",
          "app_secret": "APP_SECRET",
          "target_type": "app",
          "content": "Zombie approaching!"
          }

r = requests.post("https://api.pushed.co/1/push", data=payload)