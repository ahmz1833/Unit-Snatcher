#!./env/bin/python
from unitsnatcher import UnitSnatcher

# Username, Password, Number_Of_Sessions (number of eth(x) interfaces), eth(x) starting number
snacther = UnitSnatcher("402222222", "password", 1, 0)

# print(snatcher.get_favorite_courses())
snatcher.countdown(1726057800)

# print("\n")

# snatcher.reg([
# 	"40126-1.3",   # Saakhtar Asadi
# 	"40181-1.3",   # Amar Najafi
# 	"30003-11.1",  # Tarbiat
# 	"37448-4.2"   # Ma'aref Faani
# 	])
# snatcher.wait_for_capacity("40126-1.3")
# print(snatcher.get_capacity("40102-2.1"))
# print("\n")

# snatcher.reg([
# 	"40124-1.3",    # Elec Bayaat
# 	"22034-3.3",   # Diff Fanaa'ei
# 	"40254-1.3"    # DS Abam
# 	])

# print("\n")

# if not snatcher.checkreg("37448-4.2"):
# snatcher.reg(["44002-1.3"])
# snatcher.move(["40282-1.3"])


while True:
	continue
# 	while snatcher.get_capacity("22034-3.3") == 0 and not snatcher.has_reserve_cap("22034-3.3"):
# 		time.sleep(0.5)
# 	time.sleep(1)
# 	snatcher.reg(["22034-3.3"])


input("\n\nPress Enter to Exit....")