# 🚀  Virtual Assistant

![Versi](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Lisensi](https://img.shields.io/badge/license-MIT-green.svg)
![Status Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

> Initially, I created a program that I can talk to and that can execute my commands. I added some programs to remind me when the battery is at a certain percentage and remind me to rest when I've been in front of the screen for too long

## ⚠️The program is still in a development state, there may still be bugs that need to be fixed⚠️

## 📖 Overview

I created a program that I wanted to make as similar as possible to one of the AI characters in the Zenless Zone Zero game called "Fairy". I want to make the program as similar as possible, yes for now I'm still working on it

This program uses localhost for its model.
```` bash
    def get_ai_response(self, prompt):
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "openchat:latest",
            "prompt": f"Your name is Fairy. You **must** always call the user is Master. User: {prompt}\nAI:",
            "stream": False
        }
````
So besides being safe, you can also change the model, or fine tuning the model

## 🎯 Feature

- 🤖 Chatbot
- 🔊 Interactive sound
- 💻 Can open aplication with `-op` or `open`
- 📄 Can search all file and open that by name with `-s` or `search`
- 📁 Can search folder by name with `-of`
- 🔎 You can type `/` first and then`[object]` to search in default browser
- 🗝️ You can type shutdown, sleep, hibernate and restart
- 🔜 **Upcoming Features**: Voice Recognition


## How to use ⁉️
1. If you just want to talk or ask the AI model, you just need to type as usual when talking to your friends.
2. If you want to search for a file, but you are too lazy to do it, you can type `search file.img` or `-s file.img` to search and open the file
3. Have you forgotten the format of your files? Don't worry, I've dealt with it, now you can search for some unformatted files, because if you don't type the format, the program will have some default extensions that I have already given, but you can also add extensions, but be careful because it will make the search longer. So you just have to type `search file` or `-s file`
4. Don't worry, not only files that you can search, but also folders, although I know you will rarely use this feature
5. If you are lazy to use your eyes to search for an application, you just need to type `open application name` or `-op application name` and the application will open immediately, you can also add or remove what you don't need in Open_APP.py
6. You can also type shutdown to shut down your PC, sleep to sleep, hibernate, and restart as well
7. I have also set this program if you open it for 25 minutes then you will be warned to rest, if in 30 minutes you have not rested then your PC will be automatically put to sleep
8. Do you often forget to recharge? Do you often forget to remove the charger? Calm down, I've added a reminder when the battery status reaches a certain percentage
9. Are you lazy to open the browser? But want to find something? Just type `/` then followed by your search: `/Artificial Intelligence`
10. You can click `enter` to send message and `shift + enter` for new line

## 🔧 Tools

This programs built with:

- [Python](https://python.org/) - Proccess and GUI
- [Ollama](https://ollama.com/) - Model NLP

yes, for now, I'm only using Python and Ollama for this program. I don't know what I'm going to use next.
if you dont have ollama, you must install ollama firts [Ollama](https://ollama.com/)

**Before installing this program, you must be have:** 

- [Python](https://python.org/)
- [Ollama](https://ollama.com/)
- llama3 (I recommend you to use it because this model is good in low parameters) i use this model too for this program. Type `ollama pull llama3` in cmd

**For this program, I am using the Python Library:**
- PyQt6 `6.9.0`
- comtypes `1.4.10`
- gTTS `2.5.4`
- playsound `1.2.2`
- pycaw `20240210`
- requests `2.23.3`

**or for fast you can:**
`pip install -r requirements.txt`

## 🗂️ Project Structure

```
Fairy/
│
├── Fairy.py            # Main file
├── Command.py          # Modules for processing commands
├── file_searcher.py    # searching file and folder Modules
├── web_searcher.py     # Web search module
├── Open_APP.py         # App opening module
├── AutoRestTimer.py    # Break reminder module
├── Status_Battery.py   # battery monitoring modules
├── public/
│   │
│   ├── Alarm95_.mp3    # File audio for alarm
│   ├── Intro_Fairy.mp3 # File audio intro
│   └── Fairy_Icons.ico # program icon
│       
├── .gitignore              # File to ignore a specific file in Git
├── README.md               # Project documentation
└── requirements.txt        # List of Python dependencies
```

## ❓ FAQ

### Does the program run in the background automatically at startup?

Yes, The program can be configured to run automatically at startup. because I did it too. You can do this through the Start up folder file batch(.bat) or through the task scheduler

### How many system resources does the program use?

I want to make this program as efficient as possible in resource usage. CPU usage is typically below 5% at idle and memory is around 150-300MB depending on the LLM model used. Usage can increase when performing intensive tasks such as searching files or running chatbots.

### Does this program collect or send my data?

not. The program runs entirely locally and does not send your data to external servers except when you use the web search feature, which will send your search query to search engines.

## 🔍 Troubleshooting

### LLM model is slow to respond
1. Try using smaller models by looking for models with smaller parameters in [Ollama](https://ollama.com/search)
2. Close other heavy applications running at the same time
3. Make sure you're using the latest version of Ollama
4. Sometimes, the model becomes heavier because Energy Saver is turned on


## 📃 License

The project is licensed under the MIT License

## 📞 Contact

Finsa Kusuma Putra - [https://www.linkedin.com/in/finsa-kusuma-putra-72bab4360/) - finsakusumaputra@gmail.com

Project Link: [https://github.com/Finsa-SC/Virtual-Assistans.git](https://github.com/Finsa-SC/Virtual-Assistans.git)

---

<p align="center">Made with ❤️ by <a href="https://github.com/Finsa-SC">Finsa Kusuma Putra</a></p>