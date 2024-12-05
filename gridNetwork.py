#!/usr/bin/env python3
#Project added to Git with VSCODE.

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

import os, socket, requests, speedtest
import sys

from tkinter import messagebox

#MainWindow class ----------------------------------------------------------------------
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
                
    #Open the Speed Test dialog
    def openDialog(self):
                        
        dialog = Dialog(self)
        dialog.exec_()  # Show the dialog as a modal window
        
    #Check for active network
    def check_network(host="8.8.8.8", count=1, timeout=1):
        try:
            # Connect to a well-known address like Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            pass
            
        return False
           
  

# Dialog Class for Speed Test ----------------------------------------------------------------------   
class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
                      
        uic.loadUi("ui/dialog.ui", self)  # Load the dialog UI dynamically
        
         # Change the title bar text
        self.setWindowTitle("Speed Test")
        
        # Set up worker thread
        self.worker = WorkerThread()
        
        #Define slots for signals passed from workerthread
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.task_completed)

        # Start the task when dialog is shown
        QTimer.singleShot(0, self.start_task)

    def start_task(self):
        #print("Starting task...")
        self.label.setText("Starting Task")
        self.worker.start()  # Start the worker thread

    def update_progress(self, step):
        self.label.setText("Running Test...")
        #print(f"Processing step {step}/5...")
        self.progressBar.setValue(step * 35)

    def task_completed(self, float1, float2):
        self.label.setText("Test Completed")
        #print("Task Completed!")"""
        self.progressBar.setValue(100)
        self.label_downloadspeed.setText(f"{float1:.2f}");
        self.label_uploadspeed.setText(f"{float2:.2f}");
           
# #Work thread for speed test which updates UI ----------------------------------------------------------------------   
class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)  # Signal to update progress
    finished_signal = pyqtSignal(float, float)    # Signal to indicate task completion, pass speed values

    def run(self):
        st = speedtest.Speedtest(secure=True)
        self.progress_signal.emit(1)  # Emit progress
        #print("Speed Test")
  
        # Measure speeds
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        self.progress_signal.emit(2)  # Emit progress
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps

        #print(f"Download Speed: {download_speed:.2f} Mbps")
        self.progress_signal.emit(3)  # Emit progress with signal
        #print(f"Upload Speed: {upload_speed:.2f} Mbps")
   
        self.finished_signal.emit(download_speed, upload_speed)  # Emit completion signal



# Create and run the application ------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    
    #check if there is an active network available
    if (window.check_network() == False):
        messagebox.showinfo(title="Error", message="No Network Available.", icon=messagebox.WARNING)
        sys.exit(0)
    
    window.show()
    app.exec()