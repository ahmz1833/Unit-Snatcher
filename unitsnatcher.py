import time
import argparse
from ansi import ANSI
from edu_session import EduSession
from threading import Thread, Lock

class UnitSnatcher:
	def __init__(self, username, password, number_of_sessions=1, start=0):
		self.__number_of_sessions = number_of_sessions
		self.__edu_sessions = [None] * number_of_sessions
		for i in range(0, number_of_sessions):
			self.__edu_sessions[i] = EduSession(i, username, password, f'eth{i+start}' if number_of_sessions > 1 else None)
			print(f'{ANSI.CYAN}Session {i} (on eth{i+start}) Successfully Initialized.{ANSI.RST}')
	#----------------------
	def get_capacity(self, course):
		info = self.__edu_sessions[0].get_course_info(course)
		return info['capacity'] - info['count']
	#----------------------
	def has_reserve(self, course):
		info = self.__edu_sessions[0].get_course_info(course)
		
	# def ??

