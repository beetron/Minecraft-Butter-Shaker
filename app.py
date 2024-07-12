import sys
import threading
import time
import pyautogui
import keyboard  # type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.actionThread = None
        self.keepRunning = False
        self.startGlobalHotKeysListener()
        
    def initUI(self):
        self.setWindowTitle("牛乳ふりまん v1.0")
        self.setWindowIcon(QIcon("./files/images/mc-logo.jpg"))
        self.setFixedSize(300,75)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Instruction text
        instructionsLabel = QLabel("マイクラ画面を選択, F7開始、F8停止", centralWidget)
        instructionsLabel.setAlignment(Qt.AlignCenter)
        
        # Define layout
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(instructionsLabel)
        
    def startGlobalHotKeysListener(self):
        threading.Thread(target=self.listenForHotKeys, daemon=True).start()
        
    def listenForHotKeys(self):
        keyboard.add_hotkey("f7", lambda: self.startAction())
        keyboard.add_hotkey("f8", lambda: self.stopAction())
    
    def startAction(self):
        if self.actionThread is None or not self.actionThread.is_alive():
            self.keepRunning = True
            self.actionThread = threading.Thread(target=self.runAction)
            self.actionThread.start()
            
    def runAction(self):
        for key in map(str, range(1, 10)):
            if not self.keepRunning:
                break
            pyautogui.press(key)
            time.sleep(0.2)
            endTime = time.time() + 13 # Keep long for latency
            while time.time() < endTime and self.keepRunning:
                pyautogui.click()
                time.sleep(0.1)  
            if not self.keepRunning:
                break
            time.sleep(0.2)
            
    def stopAction(self):
        self.keepRunning = False
        if self.actionThread is not None:
            self.actionThread.join()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()