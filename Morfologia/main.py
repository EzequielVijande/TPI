from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import img_morphology as m

#Constants
WINDOW_H = 700
WINDOW_W = 800
IMAGE_SIZE = 350
N_IMG_BUTTONS = 4
IMAGE_COLUMNS=9
IMAGE_TYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg"), ("Images", "*.bmp")]
FILTERS_DICT = {"Erosion":m.erode, "Dilatacion":m.dilate, "Apertura":m.opening,
                "Cierre":m.closing, "Frontera int":m.edge_int, "Frontera ext":m.edge_ext,
                "Mediana":m.median2d, "Top-Hat":m.top_hat}
#Global variables
img_arr = [None]*2
tk_imgs = [None]*2

def upload_file(img_index, master):
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    if filename is not None:
        img = Image.open(filename).convert("L").resize((IMAGE_SIZE,IMAGE_SIZE))
        tk_img= ImageTk.PhotoImage(img)
        b2 =Button(master,image=tk_img)
        b2.grid(row=0, columnspan=IMAGE_COLUMNS)
        img_arr[img_index] = img
        tk_imgs[img_index] = tk_img

def filter_img(master, img_index):
    if img_arr[img_index] is not None:
        filtered = FILTERS_DICT[selected_filter.get()](img_arr[img_index])
        img_arr[(img_index+1)%2] = Image.fromarray(filtered.astype(np.uint8), mode="L")
        tk_imgs[(img_index+1)%2] = ImageTk.PhotoImage(img_arr[(img_index+1)%2])
        b =Button(master,image=tk_imgs[(img_index+1)%2])
        b.grid(row=0,columnspan=IMAGE_COLUMNS)

def copy_img(master, index):
    img_arr[(index+1)%2] = img_arr[index]
    tk_imgs[(index+1)%2] = ImageTk.PhotoImage(img_arr[(index+1)%2])
    b =Button(master,image=tk_imgs[(index+1)%2])
    b.grid(row=0,columnspan=IMAGE_COLUMNS)

def save_img(img_index):
    if img_arr[img_index] is not None:
        filename = filedialog.asksaveasfilename(filetypes = IMAGE_TYPES, defaultextension = IMAGE_TYPES)
        name, ext = filename.split('.')
        img_arr[img_index].save(filename)

def create_image_frame(master):
    global images_frame
    images_frame = Frame(master)
    images_frame.grid(row=0)
    #Create image upload buttons
    first_image_frame = Frame(images_frame)
    b1 = Button(first_image_frame, text='Cargar', 
    width=15,command = lambda:upload_file(0, first_image_frame))
    b1.grid(row=1, column=0)

    b2 = Button(first_image_frame, text='Guardar', 
    width=15,command = lambda:save_img(0))
    b2.grid(row=1, column=1)
    first_image_frame.grid(row=0,column=0)

    third_image_frame = Frame(images_frame)
    b6 = Button(third_image_frame, text='Guardar', 
    width=15,command = lambda:save_img(1))
    b6.grid(row=1, column=1)
    third_image_frame.grid(row=0,column=2)

    second_image_frame = Frame(images_frame)
    operations_menu = OptionMenu(second_image_frame, selected_filter, *FILTERS_DICT.keys())
    operations_menu.grid(row=1,sticky="W")
    b3 = Button(second_image_frame, text='Filtrar ->', 
    width=20,command = lambda:filter_img(third_image_frame, 0))
    b3.grid(row=2,sticky="W")
    b4 = Button(second_image_frame, text='<- Copiar', 
    width=20,command = lambda:copy_img(first_image_frame, 1))
    b4.grid(row=3,sticky="W")
    second_image_frame.grid(row=0,column=1)


root = Tk()
root.title("Operaciones aritmeticas entre imagenes")
root.geometry(str(WINDOW_W)+"x"+str(WINDOW_H)+"+50+50")  # width x height + x + y
#String vars
selected_filter = StringVar()
selected_filter.set("Elegir filtro")
create_image_frame(root)
root.mainloop()