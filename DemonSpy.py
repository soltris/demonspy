import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from ReadWriteMemory import ReadWriteMemory

GAME_OFFSET = 0x193e370
HEALTH_OFFSET = 0x284a8
SCORE_OFFSET = 0x284aa
STR_OFFSET = 0x2849e
DEF_OFFSET = 0x284a0
MAG_OFFSET = 0x284a2
P1_SPEED_TIMER_OFFSET = 0x284ad
P1_INVIS_TIMER_OFFSET = 0x284ae
P1_WALLWALK_TIMER_OFFSET = 0x284af
P1_PARALYSIS_TIMER_OFFSET = 0x284b0
MON1_DMG_OFFSET = 0x28c42
MON1_HP_OFFSET = 0x28c43
MON2_DMG_OFFSET = 0x28c46
MON2_HP_OFFSET = 0x28c47
SCROLL_REQ_OFFSET = 0x28daa
CALVRAK_HP_OFFSET = 0x28e1e
AMULET_REQ_OFFSET = 0x29278
ARTIFACT_REQ_OFFSET = 0x29288
RELIC_REQ_OFFSET = 0x297d2
CHEST_REQ_OFFSET = 0x29bc0
VORTEX_REQ_OFFSET = 0x29bc4

def main():
	app = Application()
	app.mainloop()

def readValue(gameProcess, inputPointer, size: int) -> int:
	value = []
	for i in range(size):
		value += gameProcess.readByte(inputPointer+i)
	valueConverted = joinBytes(size, value)
	return valueConverted

def joinBytes(size: int, j: list[hex]) -> int:
	total = 0
	for i in range(size):
		value = int(j[i], 0)
		total += value * 256 ** i
	return total

# This class makes a row of labels
# Inputs are the parent to the frame and a list of labels to make a row out of
class LabelRow(ttk.Frame):
	def __init__(self, parent, labels, row, column, sticky):
		super().__init__(parent)
		self.labels=[]
		for i in range(len(labels)):
			if isinstance(labels[i], str):
				self.labels.append(tk.Label(self, text=labels[i]))
			else:
				self.labels.append(tk.Label(self, textvariable=labels[i]))
			self.labels[i].grid(row=0, column=i, sticky=sticky)
			self.labels[i].configure(font = ("Helvetica", 16, "bold"))
			self.columnconfigure(i, weight=1)

		self.grid(row=row, column=column, sticky=sticky, padx=5)

class Application(ThemedTk):

	def __init__(self):
		super().__init__(theme="Adapta")
		self.title("Demon Spy")
		self.columnconfigure(0, weight=1)
		for i in range(13):
			self.rowconfigure(i, weight=1)

		# Player stat variables
		playerHealth = tk.IntVar()
		playerScore = tk.IntVar()
		playerMagic = tk.IntVar()
		playerStrength = tk.IntVar()
		playerDefense = tk.IntVar()

		# Variables for required items - All must be 0 to exit level
		scrollsLeft = tk.IntVar()
		amuletsLeft = tk.IntVar()
		artifactsLeft = tk.IntVar()
		relicsLeft = tk.IntVar()
		chestsLeft = tk.IntVar()

		# Amulet timers, expressed in seconds
		speedTimer = tk.IntVar()
		invisTimer = tk.IntVar()
		wallwalkTimer = tk.IntVar()
		paralysisTimer = tk.IntVar()

		# Monster variables
		monsterOneHP = tk.IntVar()
		monsterOneDamage = tk.IntVar()
		monsterTwoHP = tk.IntVar()
		monsterTwoDamage = tk.IntVar()

		rwm = ReadWriteMemory()

		# Find base DOSBox process location in RAM
		self.process = rwm.get_process_by_name('DOSBox.exe')
		self.process.open()
		base_address = self.process.get_base_address()

		# Because Demon Stalkers always loads in the same spot in memory relative to DOSBox on a clean boot, it too has an offset
		# We calculate all memory pointers from these static offsets after finding DOSBox
		healthPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[HEALTH_OFFSET])
		scorePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[SCORE_OFFSET])
		magicPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MAG_OFFSET])
		strengthPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[STR_OFFSET])
		defensePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[DEF_OFFSET])
		scrollsLeftPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[SCROLL_REQ_OFFSET])
		amuletsLeftPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[AMULET_REQ_OFFSET])
		artifactsLeftPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[ARTIFACT_REQ_OFFSET])
		relicsLeftPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[RELIC_REQ_OFFSET])
		chestsLeftPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[CHEST_REQ_OFFSET])
		speedTimerPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[P1_SPEED_TIMER_OFFSET])
		invisTimerPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[P1_INVIS_TIMER_OFFSET])
		wallwalkTimerPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[P1_WALLWALK_TIMER_OFFSET])
		paralysisTimerPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[P1_PARALYSIS_TIMER_OFFSET])
		monsterOneHPPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON1_HP_OFFSET])
		monsterOneDamagePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON1_DMG_OFFSET])
		monsterTwoHPPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON2_HP_OFFSET])
		monsterTwoDamagePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON2_DMG_OFFSET])

		# Set up lists of variables to iterate through
		self.dataOffsets = [MAG_OFFSET, STR_OFFSET, DEF_OFFSET, SCROLL_REQ_OFFSET, AMULET_REQ_OFFSET, ARTIFACT_REQ_OFFSET, RELIC_REQ_OFFSET, CHEST_REQ_OFFSET, P1_SPEED_TIMER_OFFSET, P1_INVIS_TIMER_OFFSET, P1_WALLWALK_TIMER_OFFSET, P1_PARALYSIS_TIMER_OFFSET, MON1_HP_OFFSET, MON1_DMG_OFFSET, MON2_HP_OFFSET, MON2_DMG_OFFSET]
		self.dataPointers = [magicPointer, strengthPointer, defensePointer, scrollsLeftPointer, amuletsLeftPointer, artifactsLeftPointer, relicsLeftPointer, chestsLeftPointer, speedTimerPointer, invisTimerPointer, wallwalkTimerPointer, paralysisTimerPointer, monsterOneHPPointer, monsterOneDamagePointer, monsterTwoHPPointer, monsterTwoDamagePointer]
		self.dataVariables = [playerMagic, playerStrength, playerDefense, scrollsLeft, amuletsLeft, artifactsLeft, relicsLeft, chestsLeft, speedTimer, invisTimer, wallwalkTimer, paralysisTimer, monsterOneHP, monsterOneDamage, monsterTwoHP, monsterTwoDamage]

		self.after(250, self.updateLabel)

		# Initialize lists of label titles and variables, iterated through for FrameRows
		self.playerStatLabelList = ["Magic", "Strength", "Defense"]
		self.playerStatVariableList = [playerMagic, playerStrength, playerDefense]
		self.requirementCategoryList = ["Required Items"]
		self.requirementLabelList = ["Scrolls", "Amulets", "Artifacts", "Relics", "Chests"]
		self.requirementVariableList = [scrollsLeft, amuletsLeft, artifactsLeft, relicsLeft, chestsLeft]
		self.amuletCategoryList = ["Amulet Timers"]
		self.amuletLabelList = ["Speed", "Invisibility", "Wallwalk", "Paralysis"]
		self.amuletVariableList = [speedTimer, invisTimer, wallwalkTimer, paralysisTimer]
		self.monsterLabelList = ["Monster 1", "Monster 2"]
		self.monsterHPList = ["HP", monsterOneHP, "HP", monsterTwoHP]
		self.monsterDamageList = ["Damage", monsterOneDamage, "Damage", monsterTwoDamage]

		# Set layout and make rows of labels
		# Arguments: Parent window, list of labels, row, column, sticky)
		self.playerStatLabelRow = LabelRow(self, self.playerStatLabelList, 0, 0, "SEW")
		self.playerStatVariableRow = LabelRow(self, self.playerStatVariableList, 1, 0, "NEW")
		self.playerStatSeparator = ttk.Separator(self, orient="horizontal")
		self.playerStatSeparator.grid(row=2, column=0, sticky="EW")
		self.requirementCategoryRow = LabelRow(self, self.requirementCategoryList, 3, 0, "EW")		
		self.requirementLabelRow = LabelRow(self, self.requirementLabelList, 4, 0, "SEW")
		self.requirementVariableRow = LabelRow(self, self.requirementVariableList, 5, 0, "NEW")
		self.requirementSeparator = ttk.Separator(self, orient="horizontal")
		self.requirementSeparator.grid(row=6, column=0, sticky="EW")
		self.amuletCategoryRow = LabelRow(self, self.amuletCategoryList, 7, 0, "EW")
		self.amuletLabelRow = LabelRow(self, self.amuletLabelList, 8, 0, "SEW")
		self.amuletVariableRow = LabelRow(self, self.amuletVariableList, 9, 0, "NEW")
		self.amuletSeparator = ttk.Separator(self, orient="horizontal")
		self.amuletSeparator.grid(row=10, column=0, sticky="EW")
		self.monsterLabelRow = LabelRow(self, self.monsterLabelList, 11, 0, "SEW")
		self.monsterHPRow = LabelRow(self, self.monsterHPList, 12, 0, "EW")
		self.monsterDamageRow = LabelRow(self, self.monsterDamageList, 13, 0, "NEW")


	def updateLabel(self):
		if len(self.dataVariables) == len(self.dataPointers):
			for i in range(len(self.dataPointers)):
				self.dataVariables[i].set(readValue(self.process, self.dataPointers[i], 1))
		self.after(250, self.updateLabel)

if __name__ == "__main__":
	main()