#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import re
COMMENT_LINE = 0
RESULT_LINE = 1
QUESTION_LINE = 2
OPERATION_LINE = 3
CORRECT_LINE = 4

class ParseError(Exception):
    """
		Base class for exceptions in this module.
		renseign error in parameter when initialiaze object
	"""
    def __init__(self, param):
		print('Error when parsing: '+ param)


class Parseur:
	tab = {"true":[], "false":[], "question": [], "operation": []}
	lineType = ""
	commentLine = r"^(\s*\#+.*)"
	resultLine = r"\s*\=+[a-zA-Z]+\s*\#?.*"
	questionLine = r"^(\s*\?[a-zA-Z]*\s*(\#.*)?)$"
	operationLine = r"(^(\s*\!?[a-zA-Z]\s*((\+|\^|\|)\s*\!?\s*[a-zA-Z]\s*)*)\s*(\<?\=\>)\s*(\s*\!?[a-zA-Z]\s*((\+|\^|\|)\s*\!?\s*[a-zA-Z]\s*)*)\s*(\#.*)?\s*$)"
	def parse(self, string):
		if any( [self.isCommentLine(string), self.isResultLine(string), self.isQuestionLine(string), self.isOperationLine(string)] ):
			return self.lineType
		else:
			raise ParseError('This is a syntax error')
	
	def isCommentLine(self, string):
		var = re.match(self.commentLine, string) 
		if var is not None:
			self.lineType = 'comment'
		return var

	def isResultLine(self, string):
		var = re.match(self.resultLine, string)
		if var is not None:
			self.lineType = 'result'
			#pb du \n
			self.tab["true"].extend(list(re.sub(r"\s*(\#.*)[\n]*", '', string)[1:]))
		return var
	
	def isQuestionLine(self, string):
		var = re.match(self.questionLine, string)
		if var is not None:
			self.lineType = 'question'
			self.tab["question"].extend(list(re.sub(r"\s*(\#.*)[\n]*", '', string)[1:]))
		return var

	def isOperationLine(self, string):
		var = re.match(self.operationLine, string)
		if var is not None:
			self.lineType = 'operation'
			self.tab["operation"].append(re.sub(r"\s*(\#.*)[\n]*", '', string).split(' '))
		return var

	def isCorrectLine(self, string):
		var = re.match(self.lineCorrect, string)
		if var is not None:
			self.lineType = 'correct'
		return var


class Expert:
	parser = Parseur()
	asArgument = False
	operators = "\+|\||\^"
	def __init__(self):
		if len(sys.argv) > 1:
			self.asArgument = True
		
	def readLines(self):
		file = open(sys.argv[1]) 
		for line in file:
			res = self.parser.parse(line)
			if res is not None:
				print(res)
			else:
				print(False)
		return self
	
	def leftValue(self, tab):
		if re.match(r"("+"|".join(self.parser.tab["true"])+")") is not None:
			val = True
		else:
			val = 'dont'
		for o in tab:
			if re.match(r"("+"|".join(self.parser.tab["true"])+")") is not None:
				val = True

	def updateValues(self, tab):
		for count, item in enumerate(tab, start=1):
			print("ok  => " + item)
			if re.match(r"(\+|\||\^)", item) is not None:
				print("ok  => " + item)
			if re.match(r"(<?=>)", elem) is not None:
				if (count == 1):
					count = 1

	def fusionTrue(self, tab, divisor):
		#divide in two table depends from <?=>
		one = tab[:divisor-1]
		two = tab[divisor:]
		print('==============================>>>>>>>>>>>>>>>>', one, two)
		#fusion de True séparées par un signe dans une boucle 

	def addTrue(self):
		try:
			for operation in self.parser.tab["operation"]:
				actual = []
				separator = 0
				for key, elem in enumerate(operation):
					if re.match(r"("+"|".join(self.parser.tab["true"])+")", elem, re.IGNORECASE) is not None:
						actual.append(True)
					elif self.parser.tab["false"]:
						if re.match(r"("+"|".join(self.parser.tab["false"])+")", elem, re.IGNORECASE) is not None:
							actual.append(False)
					elif re.match(r"(\+|\||\^)", elem) is not None:
						actual.append(elem)
					else:
						if re.match(r"(<?=>)", elem) is not None:
							separator = key
							actual.append(elem)
						else:
							actual.append(elem)
				print(actual, key)
				self.fusionTrue(actual, key)
			print('Finish')
		except:
			pass
		
def main():
	expert  = Expert()
	try:
		print(expert.readLines()).addTrue()
		#step 1 = aller du debut jusqu'à <?=> et essayer d'en sortir une valeur
	except:
		pass
	
if __name__ == "__main__":
    main()