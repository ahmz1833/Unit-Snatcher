import os
import io
import cv2
import time
import json
import asyncio
import requests
import cairosvg
import websockets
import pytesseract
import numpy as np
from ansi import ANSI
from PIL import Image
import requests_toolbelt
import xml.etree.ElementTree as ET

class EduSession:
	__user_agents = [
		# Chrome on Windows
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
		# Safari on macOS
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
		# Firefox on Windows
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
		# Chrome on Android
		"Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Mobile Safari/537.36",
		# Edge on Windows
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
		# Opera on macOS
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 OPR/75.0.3969.243",
		# Safari on iPhone
		"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
		# Firefox on Android
		"Mozilla/5.0 (Android 11; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0",
		# Chrome on Linux
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
		# Edge on macOS
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78",
	]
	#-------------------------------------------------------------
	def __init__(self, unitsnatcher, session_number, username, password, interface=None):
		self.__unitsnacther = unitsnatcher
		self.__username = username
		self.__password = password
		self.__header = {
			'accept': 'application/json',
			'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
			'content-type': 'application/json',
			'origin': 'https://my.edu.sharif.edu',
			'user-agent': EduSession.__user_agents[session_number % 10],
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
		}
		self.__session = EduSession.__create_session_with_interface(interface)
		self.__token = None
	#-------------------------------------------------------------
	def check_login(self):
		# Check if we are already logged in
		if self.__token:
			result = self.test().json()
			if not result.get('error'):
				self.__unitsnacther.set_user_state(result)
				return # return, No error and we are logged in
		
		challenge, captcha = EduSession.__get_captcha()
		data = {
			"username": self.__username,
			"password": self.__password,
			"challenge": challenge,
			"captcha": captcha
		}
		login_res = self.__request('https://my.edu.sharif.edu/api/auth/login', data)
		
		if login_res.status_code == 200 and not login_res.json().get('error'):
			self.__token = login_res.json()['token']
			self.__header['authorization'] = self.__token
		elif login_res.json().get('error'):
			print(f'{ANSI.RED.bd()}Error in Login: {login_res.json().get("error")}, Trying Again...{ANSI.RST}')
			time.sleep(0.5)
		else:
			print(f'{ANSI.RED.bd()}Error in Login: {login_res.status_code}, Trying Again...{ANSI.RST}')
			time.sleep(0.5)
		self.check_login()
	#-------------------------------------------------------------
	def get_courses_info(self):
		_, list_update = self.__read_ws()
		courses = {}
		for item in json.loads(list_update)['message']:
			courses[str(item['id'])] = item
		return courses
	#-------------------------------------------------------------
	def course_action(self, course, action):
		data = {
			"action" : action,
			"course" : course.split('.')[0],
			"units" : int(course.split('.')[1])
		}
		self.__unitsnacther.set_user_state(self.__request("https://my.edu.sharif.edu/api/reg", data).json())
		time.sleep(1.5)
		try:
			result = self.get_last_job_result(course)
			if result == "OK":
				print(f'{ANSI.GREEN.bd()}Successfull action {action}: {course}.{ANSI.RST}')
			elif result == "COURSE_DUPLICATE":
				print(f'{ANSI.CYAN.bd()}Already have {course}.{ANSI.RST}')
			else:
				print(f'{ANSI.RED}Error in {action} {course}: {ANSI.BOLD}{result}{ANSI.RST}')
			return (result == "OK" or result == "COURSE_DUPLICATE")
		except:
			print(f'{ANSI.RED}ERROR! STATE={self.__unitsnacther.get_user_state()}')
		return False
	#-------------------------------------------------------------
	def test(self):
		return self.__request('https://my.edu.sharif.edu/api/user/favorite', {"course": "40102-1", "marked": False})
	#-------------------------------------------------------------
	def get_last_job_result(self, course_filter=None):
		if not course_filter:
			return self.__unitsnacther.get_user_state()['jobs'][0]['result']
		else: 
			for job in self.__unitsnacther.get_user_state()['jobs']:
				if job['courseId'] == course_filter.split('.')[0]:
					return job['result']

############################### Private Functions ######################################

	@staticmethod
	def __captcha_svg_to_text(svg_data):
		root = ET.fromstring(svg_data)
		paths = root.findall('.//{http://www.w3.org/2000/svg}path')
		for path in paths:
			if(path.get('fill') == 'none'): root.remove(path) # remove line
			else: path.set('fill', '#000000') # black all numbers
		new_svg_data = ET.tostring(root, encoding='unicode')

		# convert to image by scale cofactor 2
		png_data = cairosvg.svg2png(bytestring=new_svg_data.encode('utf-8'), scale=2)
		image = Image.open(io.BytesIO(png_data))
		
		# remove transparency
		if image.mode == 'RGBA':
			image = Image.alpha_composite(Image.new('RGBA', image.size, (255, 255, 255, 255)), image)
			image = image.convert('RGB')

		# convert to grayscale and apply filters to prepare for OCR
		array_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
		_, tresh = cv2.threshold(array_image, 254, 255, cv2.THRESH_BINARY_INV)
		kernel = np.ones((1, 1), np.uint8)
		dilated = cv2.dilate(tresh, kernel, iterations=2)
		h, w = dilated.shape[:2]
		mask = np.zeros((h+2, w+2), np.uint8)
		cv2.floodFill(dilated, mask, (0,0), 255)
		captcha_image = Image.fromarray(dilated)

		# apply OCR and return captcha code
		return pytesseract.image_to_string(captcha_image, lang='eng', config='--psm 10 --oem 3 digits')
	
	@staticmethod
	def __get_captcha():
		url = "https://my.edu.sharif.edu/api/auth/captcha"
		response = requests.get(url)
		captcha_json = response.json()
		captcha = EduSession.__captcha_svg_to_text(captcha_json["data"]).strip()
		return captcha_json["challenge"], captcha

	@staticmethod
	def __create_session_with_interface(interface=None):
		session = requests.Session()
		if interface:
			ipv4 = os.popen(f'ip addr show {interface}').read().split("inet ")[1].split("/")[0]
			iface = requests_toolbelt.adapters.source.SourceAddressAdapter(ipv4)
			session.mount('http://', iface)
			session.mount('https://', iface)
		return session

	def __request(self, url, payload, attempt=1):
		response = self.__session.post(url, headers=self.__header, json=payload)
		if response.status_code == 429:
			wait_time = min(2 ** attempt, 60)  # Exponential backoff, max 60 seconds
			print(f'{ANSI.RED.bd()}Too many Requests!!! Waiting for {wait_time} seconds{ANSI.RST}')
			time.sleep(wait_time)
			return self.__request(url, payload, attempt + 1)
		return response

	async def __ws_read(self):
		uri = f"wss://my.edu.sharif.edu/api/ws?token={self.__token}"
		async with websockets.connect(uri=uri) as websocket:
			user_state = await websocket.recv()
			list_update = await websocket.recv()
		return user_state, list_update

	def __read_ws(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		return loop.run_until_complete(self.__ws_read())
	
# added by me