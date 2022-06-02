# TwitchClouds

<div align="center">
    <img src="https://img.shields.io/github/downloads/Roqvie/TwitchClouds/total" />
    <img src="https://img.shields.io/github/commit-activity/m/Roqvie/TwitchClouds" />
    <img src="https://img.shields.io/github/issues/Roqvie/TwitchClouds" />
</div>

Instrument for creating Twitch word clouds:
- Active chatters
- Most used messages

### Features

- Working with Helix API with twitch python library
- BTTV, FFZ, Twitch emoji support for exculding from wordclouds
- Working with images with PIL

### Installing　(Python 3.8+ on Ubuntu/Windows)
Download package and install requirements
```bash
git clone https://github.com/Roqvie/TwitchClouds.git
cd TwitchClouds
python -m venv venv
venv/bin/activate   # or venv/Scripts/activate for Windows
pip install -r requirements.txt
```

### Testing
1. Set major `.env` variables for testing
2. Test:
```bash
venv/bin/activate   # or venv/Scripts/activate for Windows
python -m pytest
```
![Example](https://raw.githubusercontent.com/Roqvie/TwitchClouds/dev/examples/test_preview.png)
### Example with `main.py`

1. Retrieve Client-Id and Client-Secret from [Twitch Apps](https://dev.twitch.tv/console/apps)
   1. Write Client-Id in `.env` file as APP_CLIENT_ID 
   2. Write Client-Secret in `.env` file as APP_CLIENT_SECRET 
2. Retrieve user Access-Token from [Twitchtokengenerator](https://twitchtokengenerator.com/)
   1. Write ACCESS TOKEN in `.env` file as USER_ACCESS_TOKEN 
   2. Write CLIENT ID in `.env` file as USER_CLIENT_ID
3. Select your broadcaster 
   1. Write his username in `.env` file as BROADCASTER
4. Write your filenames in `.env` file as BASE_FILE (with .extension) and OUTPUT_FILE (without .extension)
5. Run script:
```bash
python main.py
```
Output:
![Example](https://raw.githubusercontent.com/Roqvie/TwitchClouds/dev/examples/main_preview.png)


### Generated with `main.py`
![JesusAVGN](https://raw.githubusercontent.com/Roqvie/TwitchClouds/master/generated/hesus-users1.png)
