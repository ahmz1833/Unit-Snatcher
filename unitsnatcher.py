import os
import time
import argparse
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
		info = self.__edu_sessions[0].get_course_info(course)
		return info['capacity'] - info['count']
	#----------------------
	def has_reserve_cap(self, course):
		info = self.__edu_sessions[0].get_course_info(course)
		return info['reserve']
	#----------------------
	def checkreg(self, course):
		print(self.__edu_sessions[0].get_user_state())
		# TODO: check 'courses'
	#----------------------
	def reg(self, courses):
		course_groups = []
		for i in range(len(courses) // len(self.__edu_sesstions) + (len(courses) % len(self.__edu_sesstions) > 0)):
			course_groups.append([])
		for i in range(len(courses)):
			index = i // len(self.__edu_sesstions)
			course_groups[index].append(courses[i])

		print(course_groups) # TODO ahmz use this groups and apply your magic
		return
	#----------------------
	def countdown(self):
		regTime = self.__edu_sessions[0].get_user_state()['registrationTime']
		print(time.time_ns, regTime)
	#----------------------
	# def ??