# O Objetivo é construir um compilador simples, capaz de fazer a análise semântica de
# uma linguágem de exemplo

# @author Felipe Molinari
# 2/01/2021

import re
from Interpretador import Interp

END_WITH_SEMICOLON = ";$"
START_WITH_CHARACTER = "^[a-zA-Z]"
HAS_ASSIGNMENT_SIGNAL = "^[a-zA-Z]=.+;$"

ASSIGNMENT_CORRECT = "^[a-zA-Z][=]([a-zA-Z]|[0-9]+[+,*][a-zA-Z]|[0-9]+)([+,*]([a-zA-Z]|[0-9]+))*;"
CONSOLE_REGEX = "^[a-zA-Z];"


class Foo:
	def __init__(self, fileName):
		self.file = open(fileName, 'r')
		self.code = []
		self.current_line = 0
		self.current_pos = 0
		self.formatter()


	# Remove espaços em branco e linhas vazias
	def formatter(self):
		linesArry = self.file.readlines()
		for line in linesArry:
			formattedLine = re.sub("\s", "", line)
			if formattedLine != '':
				self.code.append(formattedLine)


	# def isOperator(self, character):
	# 	if character == '+' or character == '-':
	# 		self.current_pos += 1
	# 		return True
	# 	return False

	def isOperand(self):
		current_character = self.code[self.current_line][self.current_pos]
		if re.findall("[a-zA-Z]", current_character):
			self.current_pos += 1
			return True
		if not re.findall("[0-9]", current_character):
			return False
		
		while self.current_pos < len(current_character) and re.findall("[0-9]", current_character):
			self.current_pos += 1
		return True


	def isValid(self):
		while self.current_line < len(self.code) and self.code[self.current_line]:
			line = self.code[self.current_line]

			# Verifica se começa com um character
			if not re.findall(START_WITH_CHARACTER, line):
				errorMessage = "Should start with a character at {}:{}"
				print(errorMessage.format(self.current_line, 0))
				return False
			
			if not re.findall(END_WITH_SEMICOLON, line):
				errorMessage = "Missing ; at line {}"
				print(errorMessage.format(self.current_line))
				return False
			# Verifica se é uma operação de atribuição
			if re.findall(HAS_ASSIGNMENT_SIGNAL, line):
				self.current_pos = 2
				if self.current_pos > len(line):
					break

				if not self.isOperand():
					errorMessage = "Operand is missning at {}:{}"
					print(errorMessage.format(self.current_line, self.current_pos))
					return False
				if not re.findall(ASSIGNMENT_CORRECT, line):
					errorMessage = "Invalid syntax at {}:{}"
					print(errorMessage.format(self.current_line, self.current_pos))
					return False	

			else:
				if not re.findall(CONSOLE_REGEX, line): 
					errorMessage = "You can't print a non variable value at {}"
					print(errorMessage.format(self.current_line))
					return False
			
			self.current_line +=1
		return True
	 	




def main():
	try:
		test = Foo('teste.txt')
		i = Interp()
		if test.isValid():
			print('Parser OK. Interpreting...')
			i.interp(test.code)
		else: 
			print("Parser failed...")
	except Exception as ex:
		print("Exception: {}".format(ex))
	


if __name__ == "__main__":
    main()

