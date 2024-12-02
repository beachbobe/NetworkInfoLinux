#!/usr/bin/env python3
#Project added to Git with VSCODE.

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


import gi, os, socket, requests, speedtest
import sys
import time

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        uic.loadUi("ui/dialog.ui", self)  # Load the dialog UI dynamically
        
        # Set up worker thread
        self.worker = WorkerThread()
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.task_completed)

        # Start the task when dialog is shown
        QTimer.singleShot(0, self.start_task)

    def start_task(self):
        print("Starting task...")
        self.label.setText("Starting Task")
        self.worker.start()  # Start the worker thread

    def update_progress(self, step):
        self.label.setText("Running Test...")
        print(f"Processing step {step}/5...")

    def task_completed(self):
        self.label.setText("Test Completed")
        print("Task Completed!")
           
                
    
class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)  # Signal to update progress
    finished_signal = pyqtSignal()    # Signal to indicate task completion

    def run(self):
        st = speedtest.Speedtest(secure=True)
        self.progress_signal.emit(1)  # Emit progress
        print("Speed Test")
 
 
        # Measure speeds
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        self.progress_signal.emit(2)  # Emit progress
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps

        print(f"Download Speed: {download_speed:.2f} Mbps")
        self.progress_signal.emit(3)  # Emit progress
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
   
        self.finished_signal.emit()  # Emit completion signal



class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        uic.loadUi('ui/mainwindow.ui', self)  # Load the .ui file
        
        # Change the title bar text
        self.setWindowTitle("Network Info")
                
        # Get computer name
        computer_name = os.uname().nodename
        
        #Get Current IP
        def get_ip_address():
            try:
                # Connect to a dummy address to find the default network IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip_address = s.getsockname()[0]
                s.close()
                return ip_address
            except Exception as e:
                return f"Error: {e}"

        ip_address = get_ip_address()
        
        #Get Public IP
        def get_public_ip():
            try:
                response = requests.get("https://api.ipify.org?format=text")
                response.raise_for_status()  # Raise an error for HTTP issues
                return response.text
            except requests.RequestException as e:
                return f"Error: {e}"

        public_ip = get_public_ip()
        
        # Set display fields
        self.label_ComputerName.setText(computer_name)
        
        self.label_LocalIP.setText(ip_address)
        
        self.label_PublicIP.setText(public_ip)
        
        # Connect the clicked signal to the slot
        self.pushButton_OK.clicked.connect(self.openDialog)
        
    #end of __init__ function
                
    def openDialog(self):
                        
        dialog = Dialog(self)
        dialog.exec_()  # Show the dialog as a modal window
        
                
    

# Create and run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()