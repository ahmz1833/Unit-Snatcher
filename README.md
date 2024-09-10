# Unit Snatcher

Unit Snatcher is a Python project designed to automate unit taking from [SUT my.edu for Unit Choosing](https://my.edu.sharif.edu). It bypasses CAPTCHA using image processing and mimics multiple devices logging in to avoid being detected as a bot.

## Features
- Automated CAPTCHA reading using image processing (OpenCV and Tesseract)
- Support for multiple User-Agent strings to simulate different devices
- Easy integration and token management

## Init for usage

First, You must clone the repository in your machine or server.

Then, Create a Python Virtual Environment for this project.

You must also install prerequisties :

- `requests`
- `requests_toolbelt`
- `pytesseract`
- `cairosvg`
- `opencv-python`
- `websockets`
- `Pillow`

```bash
git clone https://github.com/ahmz1833/Unit-Snatcher.git
cd Unit-Snatcher
sudo apt install python3-venv
python3 -m venv ./env
sudo apt update
sudo apt install libcairo tesseract-ocr python3-opencv  -y
./env/bin/pip install requests websockets requests_toolbelt pytesseract cairosvg opencv-python Pillow
```

## Personal Script

You must create a new python script named as pattern `personal-*.py` , for work with this library. some examples is found in `sample.py` for reference and example.

## Multiple IP Interfaces
If you have multiple network interfaces (on the server) and want to use them, you can use `iprule.sh` script to initialize IP rules for each IP of the device and make them usable.

## Run
You must use the python of the Virtual Environment for running your personal script that uses the unitsnatcher library. 
you can add this line to first of your personal python file (like `sample.py`):
```python
#!./env/bin/python
```
