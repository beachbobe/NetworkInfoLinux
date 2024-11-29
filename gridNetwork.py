#!/usr/bin/env python3
#Project added to Git with VSCODE.

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel

import gi, os, socket, requests, speedtest

class NetworkInfo(QMainWindow):
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
        self.label = self.findChild(QLabel, 'label_ComputerName')
        self.label.setText(computer_name)
        
        self.label = self.findChild(QLabel, 'label_LocalIP')
        self.label.setText(ip_address)
        
        self.label = self.findChild(QLabel, 'label_PublicIP')
        self.label.setText(public_ip)
        

        # Access the QPushButton by its object name (pushButton)
        self.pushButton = self.findChild(QPushButton, 'pushButton_OK')
        
         # Connect the clicked signal to the close slot
        self.pushButton.clicked.connect(self.pushButtonClicked)
        
    def pushButtonClicked(self):
                        
        self.close()
        
                
    def speed_test(self):
        st = speedtest.Speedtest(secure=True)

        # Measure speeds
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps

        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")

# Create and run the application
if __name__ == "__main__":
    app = QApplication([])
    window = NetworkInfo()
    window.show()
    app.exec()