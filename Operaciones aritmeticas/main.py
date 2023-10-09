from tkinter import *


def create_ops(master):
    ops= ["Suma", "Resta"]
    formats = ["YIQ Promedio"]
    operations_frame = Frame(master)
    operations_frame.grid(row=1)
    #String vars
    selected_op = StringVar()
    selected_format = StringVar()
    selected_op.set(ops[0])
    selected_format.set(formats[0])
    
    #Dropdown menus
    operations_menu = OptionMenu(operations_frame, selected_op, *ops)
    operations_menu.grid(row=0, column=0)

    format_menu = OptionMenu(operations_frame, selected_format, *formats)
    format_menu.grid(row=0, column=1)

    return 

root = Tk()
root.title("Operaciones aritmeticas entre imagenes")
root.geometry("1300x800+50+50")  # width x height + x + y

images_frame = Frame(root)
images_frame.grid(row=0, pady=200)
create_ops(root)
root.mainloop()