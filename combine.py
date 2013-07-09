#!/usr/bin/python

import argparse
import random
import operator
from datetime import datetime


#Constants for the history file:
_history_separator_start = "====="

#Usage / Documentation
parser = argparse.ArgumentParser(description="""Randomly combines items from 
multiple lists, optionally following a set of rules, keeping a history of 
combinations, and only accepting new (not in history) results.""",
epilog="""The rules syntax is as follows:
	<IN CONSTRUCTION>""")


parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

parser.add_argument('-u', '--unique', action='store_true', help="""If specified, requires --history_file.
		With this option, the generated combination will be guaranteed to be new (not present in the history file).""")

parser.add_argument('-hf', '--history_file', help='The file where to write (and, if --unique is specified, read) the previous combination history.')

parser.add_argument('-r', '--rules', help='One or more rules, separated by semicolon, to apply to the combination.')
parser.add_argument('-rf', '--rules_file', action='append', nargs='*',
                    help='One or more files from where to load the rules to apply to the combination.')

parser.add_argument('-s', '--separator', help='Character(s) to use to separate the combined items. Defaults to ", ".')

parser.add_argument('-n', '--number', type=int, default=1, help='Generate the specified number of combinations. Defaults to 1.')

parser.add_argument('files', nargs='+', help="""The files from where to load the items to combine.
		Each file will contribute with one item for the combination, and must have one item per line.""")

args = parser.parse_args()

###############

history_file = None
history = {}
rules = []
items = []
result = []
separator = ", "



if args.files is None:
	raise ValueError('Item files not specified. You must specify at least one item file from where to choose an item.')

if args.history_file is not None:
	if args.unique:
		history_file = open(args.history_file, 'r+')
	else:
		history_file = open(args.history_file, 'a')

if args.separator is not None:
	separator = args.separator

if args.unique and history_file is None:
		raise ValueError('For --unique to be specified, --history_file must be present.')


#Load the items
file_idx = 0

for f in args.files:
	_file = open(f, 'r')
	items.append([])

	for line in _file:
		_line = line.strip()

		if _line not in items[file_idx]:
			items[file_idx].append(_line)

	file_idx += 1



#Get the combination history
if args.unique:
	current_history = None
	numCombinations = 0 #How many combinations are in history

	for _line in history_file:

		line = _line.strip()
		if len(line) > 0:
			if line.startswith(_history_separator_start): #Start of a new history record
				if current_history is not None:
					current_history[True] = True #True marks that a record ended here
					numCombinations += 1

				current_history = None

			else:
				if current_history is None: #First item of a history record
					if line not in history:
						history[line] = {} 
					current_history = history[line]

				else:
					if line not in current_history:
						current_history[line] = {}

					current_history = current_history[line]

	if current_history is not None:
		current_history[True] = True #Last record ended here
		numCombinations += 1
	
	#Check if the combinations in history cover all the possible combinations
	allCombinations = reduce(operator.mul, [len(lst) for lst in items], 1)
	if numCombinations >= allCombinations:
		raise Exception("All possible combinations are in the history file. No more unique combinations are possible.")



#Combine!!!
random.seed()
number = args.number
while number > 0:
	loop_result = []
	while len(loop_result) == 0:

		for slot in items:
			idx = random.randint(0, len(slot) - 1)

			loop_result.append(slot[idx])
			#TODO: Rules

		if args.unique:
			current_history = history
			for res in loop_result:
				if res in current_history:
					current_history = current_history[res]

			if True in current_history: #Ended here
				loop_result = []
			#TODO: Make this more efficient

	result.append(loop_result)
	number -= 1



#Save history
if history_file is not None:
	history_str = ""

	for res in result:
		history_str += _history_separator_start + ' ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
		history_str += '\n'.join(res)
		history_str += '\n\n'

	history_file.write(history_str)
	history_file.close()

#print the final result
print('\n'.join([separator.join(res) for res in result]))
