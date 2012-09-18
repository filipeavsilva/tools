import sys
import alpha_luhn

def base10toN(num,n):
	"""Change a to a base-n number.
	Up to base-36 is supported without special notation."""
	num_rep={10:'A',
				11:'B',
				12:'C',
				13:'D',
				14:'E',
				15:'F',
				16:'G',
				17:'H',
				18:'I',
				19:'J',
				20:'K',
				21:'L',
				22:'M',
				23:'N',
				24:'O',
				25:'P',
				26:'Q',
				27:'R',
				28:'S',
				29:'T',
				30:'U',
				31:'V',
				32:'W',
				33:'X',
				34:'Y',
				35:'Z'}
	new_num_string=''
	current=num
	while current!=0:
		remainder = current % n
		if 36>remainder>9:
			remainder_string=num_rep[remainder]
		elif remainder>=36:
			remainder_string='('+str(remainder)+')'
		else:
			remainder_string=str(remainder)
		new_num_string=remainder_string+new_num_string
		current=current/n
	return new_num_string

def generate_alphaseq(start, iterations, string, symbol):
	#Handle the case where the string is empty
	if len(string) == 0:
		if len(symbol) == 0:
			symbol = '%'
		string = symbol

	i = int(start)
	end = i + int(iterations)
	while i <= end:
		ib = base10toN(i, 36)
		print(string.replace(symbol,  ib + str(alpha_luhn.return_checkdigit(ib))))
		i += 1

argv = sys.argv
if len(argv) < 3:
	print('Usage: generate.py start_number num_iterations string symbol_replace')
	print('\tstring: String where each of the generated numbers will be included.')
	print('\tsymbol_replace: character(s) which will be replaced, in the string, for the generated numbers')
else:
	if len(argv) < 5:
		symbol = ''
		if len(argv) < 4:
			string = ''
		else:
			string = argv[3]
	else:
		string = argv[3]
		symbol = argv[4]

	generate_alphaseq(argv[1], argv[2], string, symbol)
