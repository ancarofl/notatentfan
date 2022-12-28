# Not A Tent Fan
This is a super simple script to check housing availability from a specific URL.

## Prerequisites
| Package | Version  |
|---|---|
| Python  | 3.10.9  |
| seleneium  |  4.7.2  |
| python-dotenv  | 0.21.0 (or just harcode everything retrieved via `os.getenv`)  |
 
I have not tested using other versions. `python -V` to find your Python version. `pip list -v` to see a list of packages and their versions.
 

## Getting Started
1. Download then navigate to project folder in a terminal
2. Create `.env` / copy `.env.example` and remove `example`. Add your URL
3. `pip install selenium`
4. `pip install python-dotenv`
5. `python main.py`
