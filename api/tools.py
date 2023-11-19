# Custom Functions

import string
import random

def GenerateToken():
	letters = string.ascii_uppercase
	token = ''.join(random.choice(letters) for i in range(16))
	
	return token