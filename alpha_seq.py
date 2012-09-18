import sys
import alpha_luhn

def base10toN(num,n):
	"""Change a to a base-n number.
	Up to base-36 is supported without special notation."""
	num_rep={10:'a',
				11:'b',
				12:'c',
				13:'d',
				14:'e',
				15:'f',
				16:'g',
				17:'h',
				18:'i',
				19:'j',
				20:'k',
				21:'l',
				22:'m',
				23:'n',
				24:'o',
				25:'p',
				26:'q',
				27:'r',
				28:'s',
				29:'t',
				30:'u',
				31:'v',
				32:'w',
				33:'x',
				34:'y',
				35:'z'}
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
	i = int(start)
	end = i + int(iterations)
	while i <= end:
		ib = base10toN(i, 36)
		print(string.replace(symbol,  ib + str(alpha_luhn.return_checkdigit(ib))))
		i += 1

argv = sys.argv
if len(argv) != 5:
	print('Usage: generate.py start_number num_iterations string symbol_replace')
	print('\tstring: String where each of the generated numbers will be included.')
	print('\tsymbol_replace: character(s) which will be replaced, in the string, for the generated numbers')
else:
	generate_alphaseq(argv[1], argv[2], argv[3], argv[4])
