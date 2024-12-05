#Customized MessageBox module using tkinter


from tkinter import messagebox as m, Tk

#Standard MessageBox for Errors/prompts
def messagebox(msg_title, msg_text, msg_type="INFO"):
    r = Tk()
    r.withdraw()
    r.option_add('*Dialog.msg.font', 'Helvetica 11')
    
    match msg_type:
        case "ERROR":
            return m.showerror(title=msg_title, message='\n' + msg_text)
        case "WARNING":
            return m.showwarning(title=msg_title, message='\n' + msg_text)
        case "YESNO":
            return m.askyesno(title=msg_title, message='\n' + msg_text)
        case "OKCANCEL":
            return m.askokcancel(title=msg_title, message='\n' + msg_text)
        case _:
            return m.showinfo(title=msg_title, message='\n' + msg_text)
    

#result = messagebox("Title of Message", "This is message text", "OKCANCEL")
#print(result)