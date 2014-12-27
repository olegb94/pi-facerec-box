"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Class
Copyright 2013 Tony DiCola 
"""
import time

import cv2
import RPIO
from RPIO import PWM

import picam
import config
import face


class Box(object):
	"""Class to represent the state and encapsulate access to the hardware of 
	the treasure box."""
	def __init__(self):
		# Initialize lock servo and button.
		self.servo = PWM.Servo()
		RPIO.setup(config.BUTTON_PIN, RPIO.IN)
		# Set initial box state.
		self.button_state = RPIO.input(config.BUTTON_PIN)
		self.is_locked = None
		RPIO.setup(2, RPIO.OUT)
		RPIO.setup(3, RPIO.OUT)
		RPIO.setup(4, RPIO.OUT)
		RPIO.setup(7, RPIO.OUT)
		RPIO.setup(17, RPIO.OUT)
		RPIO.setup(11, RPIO.OUT)
		RPIO.setup(22, RPIO.OUT)
		RPIO.setup(27, RPIO.OUT)

	def lock(self):
		"""Lock the box."""
		self.servo.set_servo(config.LOCK_SERVO_PIN, config.LOCK_SERVO_LOCKED)
		self.is_locked = True

	def unlock(self):
		"""Unlock the box."""
		self.servo.set_servo(config.LOCK_SERVO_PIN, config.LOCK_SERVO_UNLOCKED)
		self.is_locked = False

	def is_button_up(self):
		"""Return True when the box button has transitioned from down to up (i.e.
		the button was pressed)."""
		old_state = self.button_state
		self.button_state = RPIO.input(config.BUTTON_PIN)
		# Check if transition from down to up
		if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
			# Wait 20 milliseconds and measure again to debounce switch.
			time.sleep(20.0/1000.0)
			self.button_state = RPIO.input(config.BUTTON_PIN)
			if self.button_state == config.BUTTON_UP:
				return True
		return False

	def out_pins(self, n1, n2, n3, n4, n5, n6, n7, n8):
		RPIO.output(2, n1)
		RPIO.output(3, n2)
		RPIO.output(4, n3)
		RPIO.output(7, n4)
		RPIO.output(17, n5)
		RPIO.output(11, n6)
		RPIO.output(22, n7)
		RPIO.output(27, n8)

	def print_number(self, number):
		if (number==-1):
			self.out_pins(0,1,1,0,1,1,1,0)
		elif (number==-2):
			self.out_pins(0,0,0,0,0,0,0,1)
		elif (number==0):
			self.out_pins(1,1,1,1,1,1,0,0)
		elif (number==1):
			self.out_pins(0,1,1,0,0,0,0,0)
		elif (number==2):
			self.out_pins(1,1,0,1,1,0,1,0)


