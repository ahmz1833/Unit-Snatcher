import sys
import time
import random
import datetime
import asyncio
from ansi import ANSI
from edu_session import EduSession
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

class UnitSnatcher:
	def __init__(self, username, password, number_of_sessions=1, start=0):
		self.__number_of_sessions = number_of_sessions
		self.__edu_sessions = [None] * number_of_sessions
		self.__last_user_state = {}
		self.lock = Lock()  # Add a lock
		for i in range(0, number_of_sessions):
			self.__edu_sessions[i] = EduSession(self, i, username, password, f'eth{i+start}' if number_of_sessions > 1 else None)
		self.check_login()
	#---------------------
	def set_user_state(self, user_state):
		with self.lock:
			self.__last_user_state = user_state
	#---------------------
	def get_user_state(self):
		with self.lock:
			return self.__last_user_state
	#----------------------
	def get_capacity(self, course):
		info = self.__random_session().get_courses_info()[course.split(".")[0]]
		return info['capacity'] - info['count']
	#----------------------
	def has_reserve_cap(self, course):
		info = self.__random_session().get_courses_info()[course.split(".")[0]]
		return info['reserve']
	#----------------------
	def checkreg(self, course):
		courses = self.get_user_state()['courses']
		for registered_course in courses:
			if(registered_course['id'] == course.split('.')[0]):
				return True
		return False
	#----------------------
	def get_favorite_courses(self):
		favorites = self.get_user_state()['favorites']
		result = []
		courses = self.__random_session().get_courses_info()
		for favorite in favorites:
			result.append(f"{favorite}.{courses[favorite]['units']}")
		return result
	#----------------------
	def reg(self, courses):
		with ThreadPoolExecutor(max_workers=len(self.__edu_sessions)) as executor:
			for i, course in enumerate(courses):
				session = self.__edu_sessions[i % len(self.__edu_sessions)]
				executor.submit(session.course_action, course, "add")
		return
	#----------------------
	def move(self, course):
		return self.__random_session().course_action(course, "move")
	#----------------------
	def remove(self, course):
		return self.__random_session().course_action(course, "remove")
	#----------------------
	def __wait_for_capacity(self, course, action):
		while self.get_capacity(course) <= 0 and not self.has_reserve_cap(course):
			time.sleep(1)
		time.sleep(1)
		if not self.__random_session().course_action(course, action):
			self.__wait_for_capacity(course, action)
	#----------------------
	def wait_for_capacity(self, course):   # has bug
		action = "add"
		courses = self.get_user_state()['courses']
		for registered_course in courses:
			if(registered_course['number'] == course.split('-')[0]):
				action = "move"
		print(f"{ANSI.LBLUE}A listener successfully tuned for {ANSI.BOLD}{course} (action: {action}).{ANSI.RST}")
		self.__wait_for_capacity(course, action)
	#----------------------
	def check_login(self):
		for i in range(0, self.__number_of_sessions):
			self.__edu_sessions[i].check_login()
			print(f'{ANSI.CYAN}Session {i} is logged in.{ANSI.RST}')
		time.sleep(2)
	#----------------------
	def countdown(self, rtime=None):
		print("\n\n")
		regTime = self.get_user_state()['registrationTime'] if not rtime else rtime * 1000
		print(f"Start time of registeration: {ANSI.CYAN.bd()}{datetime.datetime.fromtimestamp((regTime / 1000)+3.5*3600).strftime('%02H:%02M:%02S')}{ANSI.RST}")
		time.sleep(1.5)

		while time.time() < regTime // 1000:
			difference = int(regTime // 1000 - time.time())
			minutes = difference // 60
			seconds = difference % 60
			sys.stdout.write("\r" + " " * 50)
			sys.stdout.flush()

			if(minutes == 2 and seconds == 0):
				self.check_login()
			
			if difference % 2 == 0:
				color = ANSI.RED.bd()
			elif difference % 3 == 0:
				color = ANSI.YELLOW.bd()
			else:
				color = ANSI.GREEN.bd()
			sys.stdout.write(f"\r{color}{ANSI.BLINK}{minutes:02}:{seconds:02} minutes left!{ANSI.RST}")
			sys.stdout.flush()
			time.sleep(1)

		sys.stdout.write(f"\n{ANSI.GREEN.bd()}Registration time has arrived!{ANSI.RST}\n\n")
	#----------------------
	def __random_session(self):
		return self.__edu_sessions[random.randint(0, self.__number_of_sessions - 1)]