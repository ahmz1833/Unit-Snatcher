#!./env/bin/python
from unitsnatcher import UnitSnatcher

# Username, Password, Number_Of_Sessions (number of eth(x) interfaces), eth(x) starting number
snacther = UnitSnatcher("402222222", "password", 1, 0)

print(snacther.get_capacity("22141-1"))

while True:
	continue