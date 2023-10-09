from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import img_arithemtics as ar

#Constants
N_IMG_BUTTONS = 4
IMAGE_COLUMNS=9
OPS_DICT = {"Suma":ar.cuasi_sum, "Resta":ar.cuasi_diff, "If-lighter":ar.if_lighter, "If-darker":ar.if_darker}
IMAGE_TYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg")]
#Global variables
img_arr = [None]*3
tk_imgs = [None]*3

def upload_file(img_index, master):
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    img = Image.open(filename).convert("RGB").resize((270,270))
    tk_img= ImageTk.PhotoImage(img)
    b2 =Button(master,image=tk_img)
    b2.grid(row=0)
    img_arr[img_index] = img
    tk_imgs[img_index] = tk_img

def process_img(img1, img2, master):
    img_arr[-1] = OPS_DICT[selected_op.get()](img1, img2, selected_format.get())
    tk_imgs[-1] = ImageTk.PhotoImage(img_arr[-1])
    b3 =Button(master,image=tk_imgs[-1])
    b3.grid(row=0,columnspan=6)

def save_img(img):
    if img is not None:
        filename = filedialog.asksaveasfilename(filetypes = IMAGE_TYPES, defaultextension = IMAGE_TYPES)
        img.save(filename)

def create_image_frame(master):
    global images_frame
    images_frame = Frame(master)
    images_frame.grid(row=0)
    #Create image upload buttons
    first_image_frame = Frame(images_frame)
    b1 = Button(first_image_frame, text='Cargar primera imagen', 
    width=20,command = lambda:upload_file(0, first_image_frame))
    b1.grid(row=1)
    first_image_frame.grid(row=0,column=0)

    second_image_frame = Frame(images_frame)
    b2 = Button(second_image_frame, text='Cargar segunda imagen', 
    width=20,command = lambda:upload_file(1, second_image_frame))
    b2.grid(row=1)
    second_image_frame.grid(row=0,column=1)

    third_image_frame = Frame(images_frame)
    b3 = Button(third_image_frame, text='Procesar', 
    width=20,command = lambda:process_img(img_arr[0], img_arr[1], third_image_frame))
    b3.grid(row=1, column=0)

    b4 = Button(third_image_frame, text='Guardar', 
    width=20,command = lambda:save_img(img_arr[-1]))
    b4.grid(row=1, column=1)
    third_image_frame.grid(row=0,column=2)

def create_ops(master):
    operations_frame = Frame(master)
    operations_frame.grid(row=1)
    
    #Dropdown menus
    operations_menu = OptionMenu(operations_frame, selected_op, *OPS_DICT.keys())
    operations_menu.grid(row=0, column=0)

    format_menu = OptionMenu(operations_frame, selected_format, *ar.FORMATS)
    format_menu.grid(row=0, column=1)

    return 

root = Tk()
root.title("Operaciones aritmeticas entre imagenes")
root.geometry("900x400+50+50")  # width x height + x + y

#String vars
selected_op = StringVar()
selected_format = StringVar()
selected_op.set(list(OPS_DICT.keys())[0])
selected_format.set(ar.FORMATS[0])


create_image_frame(root)
create_ops(root)
root.mainloop()