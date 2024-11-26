#!/usr/bin/env python3
#Project added to Git with VSCODE.

import gi, os, socket, requests

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk # type: ignore  (this supresses warning message)

class SimpleApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Network Info")
        
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
                
        # Set up the window properties ---------------------------------------------
        self.set_border_width(5)
        self.set_default_size(300, 200)

        # Create a grid layout
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.add(grid)
        
        
        # Create a label and reserve 5 columns for each label
        #label = Gtk.Label(label="Computer Name: " + computer_name)
        label = Gtk.Label()
        label.set_markup("Computer Name: <b>" + computer_name + "</b>")
        label.set_halign(Gtk.Align.START)  # Align label to the left
        label.set_margin_bottom(10)  # Add some spacing below the label
        grid.attach(label, 0, 0, 5, 1)  # Place label at (0, 0)
        
        # Create a label
        label1 = Gtk.Label()
        label1.set_markup("Local IP Address: <b>" + ip_address + "</b>")
        label1.set_halign(Gtk.Align.START)  # Align label to the left
        label1.set_margin_bottom(10)  # Add some spacing below the label
        grid.attach(label1, 0, 1, 5, 1)  # Place label at (0, 1)
        
        # Create a label
        label2 = Gtk.Label()
        label2.set_markup("Public IP Address: <b>" + public_ip + "</b>")
        label2.set_halign(Gtk.Align.START)  # Align label to the left
        label2.set_margin_bottom(20)  # Add some spacing below the label
        grid.attach(label2, 0, 2, 5, 1)  # Place label at (0, 2)
                   

        # Create a button
        button = Gtk.Button(label="OK")
        
        # Add the button to the box
        
        # Apply CSS styling from a file
        self.load_css("style.css")
    
        grid.attach(button, 2, 4, 1, 1)  #place button at col 4
        
        button.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        print("Button clicked, closing window.")
        Gtk.main_quit()
        
    def load_css(self, css_file):
        """Load CSS from a file."""
        if os.path.exists(css_file):
            css_provider = Gtk.CssProvider()
            with open(css_file, "rb") as file:
                css_provider.load_from_data(file.read())
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER,
            )
        else:
            print(f"***ERROR - CSS file '{css_file}' not found!")

# Create and run the application
if __name__ == "__main__":
    app = SimpleApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()