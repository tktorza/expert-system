import re

class Parseur:
	def parse(self, string):
		return re.match(r"((\s*+(\!)?[a-zA-Z]*+\s*(\+|\||\ˆ|\<\=\>|\=\>|(\!)?[a-zA-Z]*))*|\#(.)*?|\s*)", string)

