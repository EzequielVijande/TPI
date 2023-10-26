from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import img_transforms as t

#Constants
N_IMG_BUTTONS = 4
IMAGE_COLUMNS=9
IMAGE_TYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg"), ("Images", "*.bmp")]
#Global variables
img_arr = [None]*2
phase_arr = [None]*2
tk_imgs = [None]*2

def upload_img(img_index, master):
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    if filename is not None:
        img = Image.open(filename).convert("L").resize((600,600))
        tk_img= ImageTk.PhotoImage(img)
        b2 =Button(master,image=tk_img)
        b2.grid(row=0,columnspan=6)
        img_arr[img_index] = img
        tk_imgs[img_index] = tk_img

def upload_phase():
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    if filename is not None:
        img = Image.open(filename).convert("L").resize((600,600))
        phase_arr[-1] = img

def transform_img(master, img_index, transform):
    if img_arr[img_index] is not None:
        img_arr[(img_index+1)%2], phase_arr[(img_index+1)%2] = transform(img_arr[img_index], phase_arr[img_index])
        if (img_arr[(img_index+1)%2] is None) or (phase_arr[(img_index+1)%2] is None):
            messagebox.showwarning("Falla en IFFT", "No se encontro imagen de fase cargada.\n Por favor seleccione 'Cargar fase' antes de realizar la T.inversa")
            return
        tk_imgs[(img_index+1)%2] = ImageTk.PhotoImage(img_arr[(img_index+1)%2])
        b =Button(master,image=tk_imgs[(img_index+1)%2])
        b.grid(row=0,columnspan=6)
    else:
        messagebox.showwarning("No se encontro imagen", "Debe cargar una imagen o espectro antes de realizar la transformación correspondiente.")
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
    b1 = Button(first_image_frame, text='Cargar imagen', 
    width=20,command = lambda:upload_img(0, first_image_frame))
    b1.grid(row=1, column=0)

    b2 = Button(first_image_frame, text='Guardar imagen', 
    width=20,command = lambda:save_img(img_arr[0]))
    b2.grid(row=1, column=1)
    first_image_frame.grid(row=0,column=0)

    third_image_frame = Frame(images_frame)
    b5 = Button(third_image_frame, text='Cargar espectro', 
    width=20,command = lambda:upload_img(1, third_image_frame))
    b5.grid(row=1, column=0)

    b6 = Button(third_image_frame, text='Guardar espectro', 
    width=20,command = lambda:save_img(img_arr[1]))
    b6.grid(row=1, column=1)

    b7 = Button(third_image_frame, text='Cargar fase', 
    width=20,command = lambda:upload_phase())
    b7.grid(row=1, column=2)

    b8 = Button(third_image_frame, text='Guardar Fase', 
    width=20,command = lambda:save_img(phase_arr[-1]))
    b8.grid(row=1, column=3)
    third_image_frame.grid(row=0,column=3)

    second_image_frame = Frame(images_frame)
    b3 = Button(second_image_frame, text='Transformar ->', 
    width=20,command = lambda:transform_img(third_image_frame, 0, t.fourier_transform))
    b3.grid(row=1)
    b4 = Button(second_image_frame, text='<- T.inversa', 
    width=20,command = lambda:transform_img(first_image_frame, 1, t.inv_fourier))
    b4.grid(row=3)
    second_image_frame.grid(row=0,column=1)


root = Tk()
root.title("Operaciones aritmeticas entre imagenes")
root.geometry("1800x800+50+50")  # width x height + x + y


create_image_frame(root)
root.mainloop()