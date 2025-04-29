#import ImageTk
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from ReadWriteMemory import ReadWriteMemory

# Constants for memory offsets
# All addresses use base DOSBox address + GAME_OFFSET + variable offset
GAME_OFFSET = 0x193e370
GAMEPLAY_BYTE_OFFSET = 0x2848c
HEALTH_OFFSET = 0x284a8
SCORE_OFFSET = 0x284aa
STR_OFFSET = 0x2849e
DEF_OFFSET = 0x284a0
MAG_OFFSET = 0x284a2
P1_SPEED_TIMER_OFFSET = 0x284ad
P1_INVIS_TIMER_OFFSET = 0x284ae
P1_WALLWALK_TIMER_OFFSET = 0x284af
P1_PARALYSIS_TIMER_OFFSET = 0x284b0
MON1_SPD_OFFSET = 0x28c41
MON1_DMG_OFFSET = 0x28c42
MON1_HP_OFFSET = 0x28c43
MON2_SPD_OFFSET = 0x28c45
MON2_DMG_OFFSET = 0x28c46
MON2_HP_OFFSET = 0x28c47
MON1_TYPE_OFFSET = 0x28d58
MON2_TYPE_OFFSET = 0x28d80
SCROLL_REQ_OFFSET = 0x28daa
CALVRAK_HP_OFFSET = 0x28e1e
AMULET_REQ_OFFSET = 0x29278
ARTIFACT_REQ_OFFSET = 0x29288
RELIC_REQ_OFFSET = 0x297d2
LEVEL_OFFSET = 0x299a0
CHEST_REQ_OFFSET = 0x29bc0
VORTEX_REQ_OFFSET = 0x29bc4

monsterSpeedMap = {
	0: "Slow",
	1: "Med",
	2: "Fast"
}

monsterTypeMap = {
	0: "Rat",
	1: "Mage",
	2: "Ghost",
	3: "Snapper",
	4: "Dervish"
}

def main():
	app = Application()
	app.mainloop()

# Reads a value from a memory value of arbitrary size
# Inputs: Game process, pointer value, size of variable in bytes
def readValue(gameProcess, inputPointer, size: int) -> int:
	value = []
	for i in range(size):
		value += gameProcess.readByte(inputPointer+i)
	valueConverted = joinBytes(value)
	return valueConverted

# Receives a list of byte values from readValue() and converts it to a single integer
# Input: List of single byte hex values
def joinBytes(byteList) -> int:
	total = 0
	for i in range(len(byteList)):
		value = int(byteList[i], 0)
		total += value * 256 ** i
	return total

def convertMonsterSpeed(speedValue) -> str():
	if speedValue in monsterSpeedMap:
		return str(monsterSpeedMap[speedValue])
	else:
		return ''

def convertMonsterType(typeValue) -> str():
	if typeValue in monsterTypeMap:
		return str(monsterTypeMap[typeValue])
	else:
		return ''

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
			self.labels[i].configure(font = ("Helvetica", 12, "bold"))
			self.columnconfigure(i, weight=1)

		self.grid(row=row, column=column, sticky=sticky, padx=5)

class Application(ThemedTk):

	def __init__(self):
		super().__init__(theme="Adapta")
		self.title("Demon Spy")
		self.geometry("214x300")
		self.columnconfigure(0, weight=1)
		for i in range(14):
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
		monsterOneSpeed = tk.StringVar()
		monsterOneType = tk.StringVar()
		monsterOneHP = tk.IntVar()
		monsterOneDamage = tk.IntVar()
		monsterTwoSpeed = tk.StringVar()
		monsterTwoType = tk.StringVar()
		monsterTwoHP = tk.IntVar()
		monsterTwoDamage = tk.IntVar()
		calvrakHP = tk.IntVar()
		vortexesLeft = tk.IntVar()

		# Current level
		self.currentLevel = tk.IntVar()

		rwm = ReadWriteMemory()

		# Find base DOSBox process location in RAM
		self.process = rwm.get_process_by_name('DOSBox.exe')
		self.process.open()
		base_address = self.process.get_base_address()

		# Because Demon Stalkers always loads in the same spot in memory relative to DOSBox on a clean boot, it too has an offset
		# We calculate all memory pointers from these static offsets after finding DOSBox

		self.gameplayPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[GAMEPLAY_BYTE_OFFSET])
		levelPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[LEVEL_OFFSET])
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
		monsterOneSpeedPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON1_SPD_OFFSET])
		monsterOneTypePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON1_TYPE_OFFSET])
		monsterOneHPPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON1_HP_OFFSET])
		monsterOneDamagePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON1_DMG_OFFSET])
		monsterTwoSpeedPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON2_SPD_OFFSET])
		monsterTwoTypePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON2_TYPE_OFFSET])		
		monsterTwoHPPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON2_HP_OFFSET])
		monsterTwoDamagePointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[MON2_DMG_OFFSET])
		calvrakHealthPointer = self.process.get_pointer(base_address+GAME_OFFSET,offsets=[CALVRAK_HP_OFFSET])
		vortexesLeftPointer = self.process.get_pointer(base_address+GAME_OFFSET, offsets=[VORTEX_REQ_OFFSET])


		# Set up lists of variables to iterate through
		self.dataOffsets = [MAG_OFFSET, STR_OFFSET, DEF_OFFSET, SCROLL_REQ_OFFSET, AMULET_REQ_OFFSET, ARTIFACT_REQ_OFFSET, RELIC_REQ_OFFSET, CHEST_REQ_OFFSET, P1_SPEED_TIMER_OFFSET, P1_INVIS_TIMER_OFFSET, P1_WALLWALK_TIMER_OFFSET, P1_PARALYSIS_TIMER_OFFSET, MON1_HP_OFFSET, MON1_DMG_OFFSET, MON2_HP_OFFSET, MON2_DMG_OFFSET, LEVEL_OFFSET, VORTEX_REQ_OFFSET, CALVRAK_HP_OFFSET]
		self.dataPointers = [magicPointer, strengthPointer, defensePointer, scrollsLeftPointer, amuletsLeftPointer, artifactsLeftPointer, relicsLeftPointer, chestsLeftPointer, speedTimerPointer, invisTimerPointer, wallwalkTimerPointer, paralysisTimerPointer, monsterOneHPPointer, monsterOneDamagePointer, monsterTwoHPPointer, monsterTwoDamagePointer, levelPointer, vortexesLeftPointer, calvrakHealthPointer]
		self.dataVariables = [playerMagic, playerStrength, playerDefense, scrollsLeft, amuletsLeft, artifactsLeft, relicsLeft, chestsLeft, speedTimer, invisTimer, wallwalkTimer, paralysisTimer, monsterOneHP, monsterOneDamage, monsterTwoHP, monsterTwoDamage, self.currentLevel, vortexesLeft, calvrakHP]
		self.monsterStringOffsets = [MON1_SPD_OFFSET, MON1_TYPE_OFFSET, MON2_SPD_OFFSET, MON2_TYPE_OFFSET]
		self.monsterStringPointers = [monsterOneSpeedPointer, monsterOneTypePointer, monsterTwoSpeedPointer, monsterTwoTypePointer]
		self.monsterStringVariables = [monsterOneSpeed, monsterOneType, monsterTwoSpeed, monsterTwoType]

		self.after(250, self.updateLabel, False)

		# Initialize lists of label titles and variables, iterated through for FrameRows
		self.playerStatLabelList = ["MAG", "STR", "DEF"]
		self.playerStatVariableList = [playerMagic, playerStrength, playerDefense]
		self.requirementCategoryList = ["Required Items"]
		self.requirementLabelList = ["Scr", "Amu", "Art", "Rel", "Che"]
		self.requirementVariableList = [scrollsLeft, amuletsLeft, artifactsLeft, relicsLeft, chestsLeft]
		self.amuletCategoryList = ["Amulet Timers"]
		self.amuletLabelList = ["Spd", "Inv", "Wall", "Para"]
		self.amuletVariableList = [speedTimer, invisTimer, wallwalkTimer, paralysisTimer]
		self.monsterLabelList = ["Monster 1", "Monster 2"]
		self.monsterTypeList = [monsterOneSpeed, monsterOneType, ' ', monsterTwoSpeed, monsterTwoType]
		self.monsterHPList = ["HP", monsterOneHP, "HP", monsterTwoHP]
		self.monsterDamageList = ["DMG", monsterOneDamage, "DMG", monsterTwoDamage]

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
		self.monsterTypeRow = LabelRow(self, self.monsterTypeList, 12, 0, "EW")
		self.monsterHPRow = LabelRow(self, self.monsterHPList, 13, 0, "EW")
		self.monsterDamageRow = LabelRow(self, self.monsterDamageList, 14, 0, "NEW")

		self.transitionFlag = False

	def updateLabel(self, transitionFlag):
		if readValue(self.process, self.gameplayPointer, 1) == 1 and len(self.dataVariables) == len(self.dataPointers): 
			for i in range(len(self.dataPointers)):
				self.dataVariables[i].set(readValue(self.process, self.dataPointers[i], 1))
			for j in range(0, len(self.monsterStringPointers), 2):
				self.monsterStringVariables[j].set(convertMonsterSpeed(readValue(self.process, self.monsterStringPointers[j], 1)))
				self.monsterStringVariables[j+1].set(convertMonsterType(readValue(self.process, self.monsterStringPointers[j+1], 1)))
			if self.transitionFlag == False and self.currentLevel.get() == 100:
				self.transitionFlag = True
				self.transitionFrames()

		self.after(250, self.updateLabel, self.transitionFlag)

	# Switches between the view for levels 1-99 and the level 100 view with Calvrak's HP
	# TODO: Split discrete sections of HUD into individual frames and clean this up
	def transitionFrames(self):
		# Remove unnecessary frames for level 100
		self.amuletCategoryRow.grid_forget()
		self.amuletLabelRow.grid_forget()
		self.amuletVariableRow.grid_forget()
		self.amuletSeparator.grid_forget()
		self.monsterLabelRow.grid_forget()
		self.monsterTypeRow.grid_forget()
		self.monsterHPRow.grid_forget()
		self.monsterDamageRow.grid_forget()

		self.vortexCategoryRow = LabelRow(self, ["    ", "Remaining Vortexes", "    "], 7, 0, "S")
		self.vortexLeftRow = LabelRow(self, [self.dataVariables[-2], "/ 5"], 8, 0, "N")
		self.vortexSeparator = ttk.Separator(self, orient="horizontal")
		self.vortexSeparator.grid(row=9, column=0, sticky="EW")

		self.calvrakLabelRow = LabelRow(self, ["Calvrak's HP"], 10, 0, "S")
		self.calvrakHPRow = LabelRow(self, [self.dataVariables[-1], "/ 240"], 11, 0, "N")

if __name__ == "__main__":
	main()