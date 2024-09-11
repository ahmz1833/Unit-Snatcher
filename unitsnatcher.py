import sys
import time
import random
from ansi import ANSI
from edu_session import EduSession
from threading import Thread, Lock

class UnitSnatcher:
	def __init__(self, username, password, number_of_sessions=1, start=0):
		self.__number_of_sessions = number_of_sessions
		self.__edu_sessions = [None] * number_of_sessions
		self.last_user_state = {}
		for i in range(0, number_of_sessions):
			self.__edu_sessions[i] = EduSession(self, i, username, password, f'eth{i+start}' if number_of_sessions > 1 else None)
			print(f'{ANSI.CYAN}Session {i} (on eth{i+start}) Successfully Initialized.{ANSI.RST}')
	#----------------------
	def get_capacity(self, course):
		info = self.__random_session().get_course_info(course)
		return info['capacity'] - info['count']
	#----------------------
	def has_reserve_cap(self, course):
		info = self.__random_session().get_course_info(course)
		return info['reserve']
	#----------------------
	def checkreg(self, course):
		courses = self.last_user_state['courses']
		for registered_course in courses:
			if(registered_course['id'] == course.split('.')[0]):
				return True
		return False
	#----------------------
	def get_favorite_courses(self):
		favorites = self.last_user_state['favorites']
		result = []
		for favorite in favorites:
			info = self.__random_session().get_course_info(favorite)
			result.append(f"{favorite}.{info['units']}")
		return result
	#----------------------
	def reg(self, courses):
		course_groups = []
		for i in range(len(courses) // len(self.__edu_sessions) + (len(courses) % len(self.__edu_sessions) > 0)):
			course_groups.append([])
		for i in range(len(courses)):
			index = i // len(self.__edu_sessions)
			course_groups[index].append(courses[i])

		for group in course_groups:
			if group:
				threads = []
				for i, course in enumerate(group):
					t = Thread(target=self.__edu_sessions[i].course_action, args=(course, "add"))
					threads.append(t)
					t.start()
				for t in threads:
					t.join()  # Wait for all threads to finish
		
		return
	#----------------------
	def move(self, course):
		return self.course_action(course, "move")
	#----------------------
	def remove(self, course):
		return self.course_action(course, "remove")
	#----------------------
	def check_login(self):
		for i in range(0, number_of_sessions):
			self.__edu_sessions[i].check_login()
			print(f'{ANSI.CYAN}Session {i} (on eth{i+start}) is logged in.{ANSI.RST}')
	#----------------------
	def countdown(self):
		print("\n\n")
		regTime = self.__random_session().get_user_state()['registrationTime']

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