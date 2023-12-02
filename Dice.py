"""
Project: Yahtzee
Module Name: Dice.py
Creation Date: Nov 25 2023
Author: Casey Foster
CSC 221
"""

# TODO: header

import random

class Die:

	def __init__(self, pSides=6):
		self.__NUMBER_OF_SIDES = pSides
		self.__currentFace = 1
	def roll(self):
		self.__currentFace = random.randint(1, self.__NUMBER_OF_SIDES)
	def lookAtDie(self):
		return self.__currentFace


