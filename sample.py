#!./env/bin/python
from unitsnatcher import UnitSnatcher

# Username, Password, Number_Of_Sessions (number of eth(x) interfaces), eth(x) starting number
snacther = UnitSnatcher("402222222", "password", 1, 0)

# wait for registeration time
snatcher.countdown()

snacther.add(["40210-1.3", "40211-2.3", "40221-2.3"])

if snacther.checkreg("40210-1.3") and not snacther.checkreg("40211-2.3"):
	snacther.add(["40211-1.3"])

while snacther.get_capacity("22141-1") == 0:
	continue

snacther.add(["22141-1.3"])

input("\n\nPress Enter to Exit....")