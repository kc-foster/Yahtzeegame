"""
Project: Yahtzee
Module Name: Dice.py
Creation Date: Nov 25 2023
Author: Casey Foster
CSC 221
"""

from Dice import Die

def getIntegerValue(message):

	# get any input as a string
	string = input(message)

	if string == '':
		return -2, None

	for i in range(len(string)):
		# catches floats as well as strings with spaces in them
		if not string[i].isdigit() or int(string[i]) < 0:
			print(f"\'{string}\' is not a valid integer value!")
			return -1, None

	# return the string as an integer
	return 1, int(string)

def rollDice(roll_x_dice, list_of_dice, AB_options_count, dice_rolls_storage):

	# roll dice
	for dice in roll_x_dice:
		if dice == 0:
			continue
		list_of_dice[dice-1].roll()
	

	# auto store rolls at 3 rolls (0-2)
	if AB_options_count == 2:
		rollStore(dice_rolls_storage, list_of_dice, player_scores)
		for dice_object in list_of_dice:
			print(dice_object.lookAtDie(), end=' ')
		print("saved.")
		# return success
		return 2, list_of_dice

	# return success and the new list of dice rolls
	return 1, list_of_dice

def reroll(list_of_dice, AB_options_count, dice_rolls_storage):

	get_integer_return_value = None
	num_rerolls = test_input = 0
	input_rerolls = []

	# while the return value for getIntegerValue is success and the input is less than 6, append input numbers to a list
	# a maximum of 5 integers (to choose the dice)
	get_integer_return_value, test_input = getIntegerValue("Which dice to reroll? Enter one number at a time.\n")
	while True:
		if get_integer_return_value == -2:
			break
		elif get_integer_return_value > 0 and test_input < 6 and num_rerolls < 5:
			input_rerolls.append(test_input)
			get_integer_return_value, test_input = getIntegerValue("Which dice to reroll? Enter one number at a time.\n")
			num_rerolls += 1
		elif num_rerolls > 4:
			print("Too many rerolls")
			return -1, list_of_dice
		elif get_integer_return_value < 0 or test_input > 5:
			print("Invalid dice reroll")
			return -1, list_of_dice

	# otherwise, instantiate a list of 5 elements of value 0, and edit those list elements with the dice to reroll
	output_rerolls = [0 for _ in range(5)]
	for dice in input_rerolls:
		output_rerolls[dice-1] = dice

	# pass rollDice function the rerolls in output_rerolls along with the list of dice rolls list that will hold the new rolls
	# pass AB_options_count and dice_rolls_storage as well to update those
	return rollDice(output_rerolls, list_of_dice, AB_options_count, dice_rolls_storage)

def rollStore(dice_rolls_storage, list_of_dice, player_scores):

	storelist = []
	# look at each value of the dice and append to an empty list
	for dice_object in list_of_dice:
		storelist.append(dice_object.lookAtDie())

	# append that list to storage
	dice_rolls_storage.append(storelist)

	# call userChooseAction so the user can choose what to do with the stored roll
	userChooseAction(list_of_dice, player_scores)

	return

def rollDisplayCurrent(list_of_dice):

	print("\nCurrent rolls:", end=' ')
	# look at current rolls and print them
	for dice_object in list_of_dice:
		print(dice_object.lookAtDie(), end=' ')
	print("\n")

	return

def rollDisplayStored(dice_rolls_storage, player_scores):

	# print both the set of all previous saved rolls, as well as the score card so the user does not have to remember
	# his/her chosen Upper Section and Lower Section choices
	print(f"All rolls:\n{dice_rolls_storage}")
	print(f"Score Card:\n{player_scores}")

	return

# call restart function at the end of turn 13 or at turn 0
def rollRestart():

	# clear score card for the player
	player_scores = {"Aces": 0, "Twos": 0, "Threes": 0, "Fours": 0, "Fives": 0, "Sixes": 0, "Three_of_a_Kind": 0, "Four_of_a_Kind": 0, "Yahtzees": 0, "Full_House": 0, "Small_Straight": 0, "Large_Straight": 0, "Chance": 0}
	# clear storage
	dice_rolls_storage = []
	# clear list_of_dice that holds the current rolls
	list_of_dice = [None for _ in range(5)]

	# call Die() constructor function 5 times to instantiate dice into a list called list_of_dice
	for dice_index in range(5):
		list_of_dice[dice_index] = Die()

	# reset list of dice and storage every 13th turn if the user chooses to
	return list_of_dice, dice_rolls_storage, player_scores

def userChooseAction(list_of_dice, player_scores):

	scores = {"Aces": -1, "Twos": -1, "Threes": -1, "Fours": -1, "Fives": -1, "Sixes": -1, "Three_of_a_Kind": -2, "Four_of_a_Kind": -2, "Yahtzees": 50, "Full_House": 25, "Small_Straight": 30, "Large_Straight": 40, "Chance": -2}
	upper_section = {"Aces": 0,"Twos": 1, "Threes": 2, "Fours": 3, "Fives": 4, "Sixes": 5}

	# tally the dice values into a list
	tallies = [0 for _ in range(6)]
	for i in range(len(list_of_dice)):
		tallies[list_of_dice[i].lookAtDie() - 1] += 1

	# decide on the correct set of choices to provide to the user for the rolls given
	list_of_choices = []
	# flags keep track of two or three of same roll for three of a kind and full house rolls
	three_seen = two_seen = four_seen = five_seen = False
	for tally_index in range(len(tallies)):
		# if there is a tally present for a specific value, and the user has not chosen for that score on the score card
		# then append that choice to the list of choices the user can make
		if tallies[tally_index] >= 1 and not(player_scores[list(player_scores.keys())[tally_index]]):
			list_of_choices.append(list(player_scores.keys())[tally_index])

		if tallies[tally_index] == 2:
			two_seen = True
		if tallies[tally_index] == 3:
			three_seen = True
		if tallies[tally_index] == 4:
			four_seen = True
		if tallies[tally_index] == 5:
			five_seen = True

	# combos of the same kind
	if three_seen and not(player_scores[list(player_scores.keys())[6]]):
		list_of_choices.append("Three_of_a_Kind")
	elif four_seen and not(player_scores[list(player_scores.keys())[7]]):
		list_of_choices.append("Four_of_a_Kind")
	elif five_seen and not(player_scores[list(player_scores.keys())[8]]):
		list_of_choices.append("Yahtzees")

	# check for Full Houses
	if (three_seen and two_seen) and not(player_scores[list(player_scores.keys())[9]]):
		list_of_choices.append("Full_House")

	# check for sequences, small straight can be 1 of 3 possibilities, large straight 1 of 2
	if (all(tallies[:4]) or all(tallies[1:5]) or all(tallies[2:6])) and not(player_scores[list(player_scores.keys())[10]]):
		list_of_choices.append("Small_Straight")
	if (all(tallies[:5]) or all(tallies[1:6])) and not(player_scores[list(player_scores.keys())[11]]):
		list_of_choices.append("Large_Straight")

	# if the chance option has not been used, display that
	if not(player_scores[list(player_scores.keys())[12]]):
		list_of_choices.append("Chance")

	display_rolls = [0 for _ in range(5)]
	for index, roll in enumerate(list_of_dice):
		display_rolls[index] = roll.lookAtDie()

	# get user input for the choice to score on the score card
	while True:
		# choose any remaining upper section or lower section choices to disregard if no choices are present in the roll
		if not(list_of_choices):
			for potential_scoring_roll in player_scores.keys():
				if player_scores[potential_scoring_roll] == 0:
					list_of_choices.append(potential_scoring_roll)
			user_choice = input(f"Last roll: {display_rolls}\nChoices to score as zero: {list_of_choices}\nEnter Choice\n")
			if user_choice in list_of_choices:
				player_scores[user_choice] = -1
			break

		# if the entered choice is a correct choice, then score that on the score card accordingly
		user_choice = input(f"Last roll: {display_rolls}\nChoices: {list_of_choices}\nEnter Choice\n")
		if user_choice in list_of_choices:
			if scores[user_choice] == -1:
				player_scores[user_choice] = tallies[upper_section[user_choice]] * ((upper_section[user_choice]) + 1)
			elif scores[user_choice] == -2:
				player_scores[user_choice] = sum(display_rolls)
			else:
				player_scores[user_choice] += scores[user_choice] 
			print(f"{user_choice} Scored")
			break

	return


# AB_options_count counts the number of times either option A or B was selected during a turn
# turn_count iterates the current turn
# return_value is used by either option A or B in an if-elif-else structure to decide what to do on different return values of option A or B
AB_options_count = turn_count = return_value = 0
# AorB_selected is used to determine if either option A or B was selected last turn which allows options C or D to become available to the user
AorB_selected = False
# dice_rolls_storage stores all rolls
dice_rolls_storage = []

# Main loop
while True:

	return_value = 0
	# Initialize game
	if turn_count == 0 and AB_options_count == 0:
		list_of_dice, dice_rolls_storage, player_scores = rollRestart()

	# choose to restart game at last turn or exit
	elif turn_count == 13:
		print(f"score: {sum([score_value for score_value in player_scores.values() if score_value != -1])}")

		turn_13_input = input("Press F or f to restart or G or g to exit\n")
		if turn_13_input == 'g' or turn_13_input == 'G':
			break
		elif turn_13_input == 'f' or turn_13_input == 'F':
			turn_count = AB_options_count = 0
			continue
		else:
			continue

	# Menu
	option = input("======YAHTZEE======\nA) Roll all five dice\nB) Roll a few dice\nC) Store a roll\nD) Display current dice\nE) Display saved rolls\nF) Restart\nG) Quit\n")
	if option != 'A' and option != 'a' and option != 'B' and option != 'b' and option != 'C' and option != 'c' and option != 'D' and option != 'd' and option != 'E' and option != 'e' and option != 'F' and option != 'f' and option != 'G' and option != 'g':
		print(f"{option} is not a valid option")
		continue

	# Roll 5 dice
	if option == 'A' or option == 'a':
		return_value, list_of_dice = rollDice([1, 2, 3, 4, 5], list_of_dice, AB_options_count, dice_rolls_storage)
		if return_value == -1:
			continue
		# 3 rolls this turn, store
		elif return_value == 2:
			turn_count += 1
			AB_options_count = 0
			AorB_selected = False
		else:
			AB_options_count += 1
			AorB_selected = True

	# Roll 5 or less dice if A has been selected atleast once this turn
	elif AB_options_count > 0 and (option == 'B' or option == 'b'):
		return_value, list_of_dice = reroll(list_of_dice, AB_options_count, dice_rolls_storage)
		if return_value == -1:
			continue
		elif return_value == 2:
			turn_count += 1
			AB_options_count = 0
			AorB_selected = False
		else:
			AB_options_count += 1
			AorB_selected = True

	# print error and continue if B selected incorrently
	elif not(AB_options_count) and (option == 'B' or option == 'b'):
		print("Must roll 5 first to reroll")
		continue

	# Store a roll
	elif AorB_selected and (option == 'C' or option == 'c'):
		rollStore(dice_rolls_storage, list_of_dice, player_scores)
		AB_options_count = 0
		turn_count += 1
		AorB_selected = False

	# option C selected before A or B
	elif not(AorB_selected) and (option == 'C' or option == 'c'):
		print("Must roll first before saving rolls")
		continue

	# Display last roll
	elif AorB_selected and (option == 'D' or option == 'd'):
		rollDisplayCurrent(list_of_dice)
		continue

	# print error and continue if D selected incorrectly
	elif not(AorB_selected) and (option == 'D' or option == 'd'):
		print("Must roll first to display")
		continue
	
	# Display all rolls and score card for the player
	elif option == 'E' or option == 'e':
		rollDisplayStored(dice_rolls_storage, player_scores)
		continue

	# Restart
	elif option == 'F' or option == 'f':
		turn_count = AB_options_count = 0
		continue

	# Quit
	elif option == 'G' or option == 'g':
		break