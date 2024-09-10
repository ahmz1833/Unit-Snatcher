class ANSI:
	# Define common ANSI codes as static instances
	RST = None  # Will be initialized later
	BOLD = None
	DIM = None
	NORMAL = None
	UNDERLINE = None
	NO_UNDERLINE = None
	STRIKE = None
	NO_STRIKE = None
	BLINK = None
	NO_BLINK = None
	INVERT = None
	DEF_FG = None
	WHITE = None
	BLACK = None
	RED = None
	GREEN = None
	BLUE = None
	YELLOW = None
	CYAN = None
	MAGENTA = None
	LRED = None
	LGREEN = None
	LBLUE = None
	LYELLOW = None
	LCYAN = None
	LMAGENTA = None

	def __init__(self, ansi_code: str):
		"""Constructor for ANSI class to store ANSI escape codes."""
		self.ansi = ansi_code

	@staticmethod
	def fg(red: int, green: int, blue: int):
		"""Return ANSI code for setting foreground color using RGB values."""
		return ANSI(f"\033[38;2;{red};{green};{blue}m")

	@staticmethod
	def bg(red: int, green: int, blue: int):
		"""Return ANSI code for setting background color using RGB values."""
		return ANSI(f"\033[48;2;{red};{green};{blue}m")

	def bd(self):
		"""Bold the text by appending BOLD ANSI code."""
		return self.append(ANSI.BOLD)

	def set_bg(self, red: int, green: int, blue: int):
		"""Set background color for the text."""
		return self.append(ANSI.bg(red, green, blue))

	def append(self, to_be_appended):
		"""Append another ANSI code to this one."""
		return ANSI(self.ansi + to_be_appended.ansi)

	def __str__(self):
		"""Return the ANSI code as a string."""
		return self.ansi

# Initialize the static constants
ANSI.RST = ANSI("\033[0m")
ANSI.BOLD = ANSI("\033[1m")
ANSI.DIM = ANSI("\033[2m")
ANSI.NORMAL = ANSI("\033[22m")
ANSI.UNDERLINE = ANSI("\033[4m")
ANSI.NO_UNDERLINE = ANSI("\033[24m")
ANSI.STRIKE = ANSI("\033[9m")
ANSI.NO_STRIKE = ANSI("\033[29m")
ANSI.BLINK = ANSI("\033[5m")
ANSI.NO_BLINK = ANSI("\033[25m")
ANSI.INVERT = ANSI("\033[7m")
ANSI.DEF_FG = ANSI("\033[39m")
ANSI.WHITE = ANSI("\033[37m")
ANSI.BLACK = ANSI("\033[30m")
ANSI.RED = ANSI("\033[31m")
ANSI.GREEN = ANSI("\033[32m")
ANSI.BLUE = ANSI("\033[34m")
ANSI.YELLOW = ANSI("\033[33m")
ANSI.CYAN = ANSI("\033[36m")
ANSI.MAGENTA = ANSI("\033[35m")
ANSI.LRED = ANSI("\033[91m")
ANSI.LGREEN = ANSI("\033[92m")
ANSI.LBLUE = ANSI("\033[94m")
ANSI.LYELLOW = ANSI("\033[93m")
ANSI.LCYAN = ANSI("\033[96m")
ANSI.LMAGENTA = ANSI("\033[95m")