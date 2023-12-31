from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import luminance_ops as l
import numpy as np
from matplotlib import pyplot as plt
import io

#Constants
N_IMG_BUTTONS = 4
IMAGE_COLUMNS=3
FILTERS_DICT = {"Raiz":l.sqrt_ilum, "Cuadrado":l.pow2_ilum, "Lineal":l.lineal_ilum, "Ecualización":l.equalize_ilum}
IMAGE_TYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg")]
#Global variables
img_arr = [None]*2
tk_imgs = [None]*2

def view_histogram(master, img_index):
    if not showing_hist[img_index]:
        my_dpi=96
        yiq_img = l.rgb_to_yiq(np.array(img_arr[img_index]))
        img_counts, bins = np.histogram(yiq_img[:,:,0], bins=20)
        buf = io.BytesIO()
        buf.seek(0)
        fig = plt.figure(figsize=(600/my_dpi, 600/my_dpi), dpi=my_dpi)
        plt.stairs(img_counts, bins)
        fig.savefig(buf)
        buf.seek(0)
        png_hist =  Image.open(buf)
        tk_imgs[img_index] = ImageTk.PhotoImage(png_hist)
        showing_hist[img_index] = True
    else:
        tk_imgs[img_index] = ImageTk.PhotoImage(img_arr[img_index])
        showing_hist[img_index] = False
    img_b =Button(master,image=tk_imgs[img_index])
    img_b.grid(row=0, columnspan=IMAGE_COLUMNS)

def upload_file(img_index, master):
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    img = Image.open(filename).convert("RGB").resize((600,600))
    tk_img= ImageTk.PhotoImage(img)
    img_b =Button(master,image=tk_img)
    img_b.grid(row=0, columnspan=IMAGE_COLUMNS)
    img_arr[img_index] = img
    tk_imgs[img_index] = tk_img

def filter_img(img1, master):
    img_arr[-1] = FILTERS_DICT[selected_filter.get()](img1)
    tk_imgs[-1] = ImageTk.PhotoImage(img_arr[-1])
    b3 =Button(master,image=tk_imgs[-1])
    b3.grid(row=0,columnspan=6)

def create_image_frame(master):
    images_frame = Frame(master)
    images_frame.grid(row=0)
    #Create image upload buttons
    first_image_frame = Frame(images_frame)
    b1 = Button(first_image_frame, text='Cargar primera imagen', 
    width=20,command = lambda:upload_file(0, first_image_frame))
    b1.grid(row=1, column=0)

    b2 = Button(first_image_frame, text='Histograma', 
    width=20,command = lambda:view_histogram(first_image_frame,0))
    b2.grid(row=1, column=1)
    first_image_frame.grid(row=0,column=0)
    #Second image
    second_image_frame = Frame(images_frame)
    operations_menu = OptionMenu(second_image_frame, selected_filter, *FILTERS_DICT.keys())
    operations_menu.grid(row=1, column=0)

    b3 = Button(second_image_frame, text='Filtrar', 
    width=20,command = lambda:filter_img(img_arr[0], second_image_frame))
    b3.grid(row=1, column=1)

    b4 = Button(second_image_frame, text='Histograma', 
    width=20,command = lambda:view_histogram(second_image_frame,1))
    b4.grid(row=1, column=2)
    second_image_frame.grid(row=0, column=1)

root = Tk()
root.title("Operaciones aritmeticas entre imagenes")
root.geometry("1200x800+50+50")  # width x height + x + y

#String vars
selected_filter = StringVar()
selected_filter.set("Elegir filtro")
#Flags
showing_hist = [False, False]

create_image_frame(root)
root.mainloop()