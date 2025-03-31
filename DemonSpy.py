import tkinter as tk
from tkinter import ttk

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
MON1_DMG_OFFSET = 0x28cf2
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

def updateLabel(label, gameProcess, inputPointer, size: int):
	print(gameProcess)
	print(inputPointer)
	print(size)
	print('readValue:',readValue(gameProcess,inputPointer, size))
	label.set(readValue(gameProcess, inputPointer, size))

class Application(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Demon Spy")
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)

		playerStatLabelList = ["Magic", "Strength", "Defense"]
		playerStatVariableList = ["Magic", "Strength", "Defense"]
		requirementCategoryList = ["Required Items"]
		requirementLabelList = ["Scrolls", "Amulets", "Artifacts", "Relics", "Chests"]
		requirementVariableList = ["Scrolls", "Amulets", "Artifacts", "Relics", "Chests"]

		# Set up frame containers
		playerStatLabelFrame = ttk.Frame(self)
		playerStatLabelFrame.grid(row=0, column=0, sticky="SEW", padx=5)
		playerStatLabelFrame.columnconfigure(0, weight=1)
		playerStatLabelFrame.columnconfigure(1, weight=1)
		playerStatLabelFrame.columnconfigure(2, weight=1)
		playerStatFrame = ttk.Frame(self)
		playerStatFrame.grid(row=1, column=0, sticky="NEW", padx=5)
		playerStatFrame.columnconfigure(0, weight=1)
		playerStatFrame.columnconfigure(1, weight=1)
		playerStatFrame.columnconfigure(2, weight=1)
		requirementCategoryFrame = ttk.Frame(self)
		requirementCategoryFrame.grid(row=2, column=0, sticky="EW", padx=5, pady=5)
		requirementCategoryFrame.columnconfigure(0, weight=1)
		requirementLabelFrame = ttk.Frame(self)
		requirementLabelFrame.grid(row=3, column=0, sticky="SEW", padx=5)
		requirementLabelFrame.columnconfigure(0, weight=1)
		requirementLabelFrame.columnconfigure(1, weight=1)
		requirementLabelFrame.columnconfigure(2, weight=1)
		requirementLabelFrame.columnconfigure(3, weight=1)
		requirementLabelFrame.columnconfigure(4, weight=1)
		requirementFrame = ttk.Frame(self)
		requirementFrame.grid(row=4, column=0, sticky="NEW", padx=5)
		requirementFrame.columnconfigure(0, weight=1)
		requirementFrame.columnconfigure(1, weight=1)
		requirementFrame.columnconfigure(2, weight=1)
		requirementFrame.columnconfigure(3, weight=1)
		requirementFrame.columnconfigure(4, weight=1)

		playerHealth = tk.IntVar()
		playerScore = tk.IntVar()
		playerMagic = tk.IntVar()
		playerStrength = tk.IntVar()
		playerDefense = tk.IntVar()
		scrollsLeft = tk.IntVar()
		amuletsLeft = tk.IntVar()
		artifactsLeft = tk.IntVar()
		relicsLeft = tk.IntVar()
		chestsLeft = tk.IntVar()

		rwm = ReadWriteMemory()

		process = rwm.get_process_by_name('DOSBox.exe')
		process.open()
		base_address = process.get_base_address()

		# Get pointers for basic player values after finding game's base memory address
		healthPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[HEALTH_OFFSET])
		scorePointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[SCORE_OFFSET])
		magicPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[MAG_OFFSET])
		strengthPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[STR_OFFSET])
		defensePointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[DEF_OFFSET])
		scrollsLeftPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[SCROLL_REQ_OFFSET])
		amuletsLeftPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[AMULET_REQ_OFFSET])
		artifactsLeftPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[ARTIFACT_REQ_OFFSET])
		relicsLeftPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[RELIC_REQ_OFFSET])
		chestsLeftPointer = process.get_pointer(base_address+GAME_OFFSET, offsets=[CHEST_REQ_OFFSET])

		# Update labels with all sought-for values
		playerHealth.set(readValue(process, healthPointer, 2))
		playerScore.set(readValue(process, scorePointer, 2))
		playerMagic.set(readValue(process, magicPointer, 1))
		playerStrength.set(readValue(process, strengthPointer, 1))
		playerDefense.set(readValue(process, defensePointer, 1))
		scrollsLeft.set(readValue(process, scrollsLeftPointer, 1))
		amuletsLeft.set(readValue(process, amuletsLeftPointer, 1))
		artifactsLeft.set(readValue(process, artifactsLeftPointer, 1))
		relicsLeft.set(readValue(process, relicsLeftPointer, 1))
		chestsLeft.set(readValue(process, chestsLeftPointer, 1))

		# Create all the Labels for the main layout
		magicStatLabel = tk.Label(playerStatLabelFrame, text='  Magic')
		strengthStatLabel = tk.Label(playerStatLabelFrame, text='  Strength')
		defenseStatLabel = tk.Label(playerStatLabelFrame, text=' Defense')
		magicStat = tk.Label(playerStatFrame, textvariable=playerMagic)
		strengthStat = tk.Label(playerStatFrame, textvariable=playerStrength)
		defenseStat = tk.Label(playerStatFrame, textvariable=playerDefense)
		requirementLabel = tk.Label(requirementCategoryFrame,text='Required Items')
		scrollReqLabel = tk.Label(requirementLabelFrame,text='Scrolls')
		scrollReq = tk.Label(requirementFrame, text=scrollsLeft.get())
		amuletReqLabel = tk.Label(requirementLabelFrame,text='Amulets')
		amuletReq = tk.Label(requirementFrame, text=amuletsLeft.get())
		artifactReqLabel = tk.Label(requirementLabelFrame,text='Artifacts')
		artifactReq = tk.Label(requirementFrame, text=artifactsLeft.get())
		relicReqLabel = tk.Label(requirementLabelFrame,text='Relics')
		relicReq = tk.Label(requirementFrame,text=relicsLeft.get())
		chestReqLabel = tk.Label(requirementLabelFrame,text='Chests')
		chestReq = tk.Label(requirementFrame,text=chestsLeft.get())

		## Layout of main window
	
		# Row 1: Player stat labels
		magicStatLabel.grid(row=0, column=0)
		strengthStatLabel.grid(row=0, column=1)
		defenseStatLabel.grid(row=0, column=2)
		
		# Row 2: Player stats
		magicStat.grid(row=0, column=0)
		strengthStat.grid(row=0, column=1)
		defenseStat.grid(row=0, column=2)
	
		# Row 3: Top Required Items Label
		requirementLabel.grid(row=0, column=0)
		
		# Row 4: Required Items Category Labels
		scrollReqLabel.grid(row=0, column=0)
		amuletReqLabel.grid(row=0, column=1)
		artifactReqLabel.grid(row=0, column=2)
		relicReqLabel.grid(row=0, column=3)
		chestReqLabel.grid(row=0, column=4)
	
		# Row 4: Requirements
		scrollReq.grid(row=0, column=0)
		amuletReq.grid(row=0, column=1)
		artifactReq.grid(row=0, column=2)
		relicReq.grid(row=0, column=3)	
		chestReq.grid(row=0, column=4)

class LabelRow(ttk.Frame):
	def __init__(self, parent, labelList):
		super().__init__(parent)
		for i in range(labelList):
			self.columnconfigure(i, weight=1)

#statList = ['magic','strength','defense','scrollsLeft','amuletsLeft','artifactsLeft','relicsLeft','chestsLeft']

if __name__ == "__main__":
	main()