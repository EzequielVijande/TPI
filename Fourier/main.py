from tkinter import *
from tkinter import filedialog
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

def upload_file(img_index, master):
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    if filename is not None:
        img = Image.open(filename).convert("L").resize((600,600))
        tk_img= ImageTk.PhotoImage(img)
        b2 =Button(master,image=tk_img)
        b2.grid(row=0)
        img_arr[img_index] = img
        tk_imgs[img_index] = tk_img
        if img_index == 1:
            name, ext = filename.split(".")
            phase_arr[img_index] = Image.open(name+"_phase."+ext).convert("L").resize((600,600))

def transform_img(master, img_index, transform):
    if img_arr[img_index] is not None:
        img_arr[(img_index+1)%2], phase_arr[(img_index+1)%2] = transform(img_arr[img_index], phase_arr[img_index])
        tk_imgs[(img_index+1)%2] = ImageTk.PhotoImage(img_arr[(img_index+1)%2])
        b =Button(master,image=tk_imgs[(img_index+1)%2])
        b.grid(row=0,columnspan=6)

def save_img(img_index):
    if img_arr[img_index] is not None:
        filename = filedialog.asksaveasfilename(filetypes = IMAGE_TYPES, defaultextension = IMAGE_TYPES)
        name, ext = filename.split('.')
        img_arr[img_index].save(filename)
        phase_arr[img_index].save(name+"_phase."+ext)

def create_image_frame(master):
    global images_frame
    images_frame = Frame(master)
    images_frame.grid(row=0)
    #Create image upload buttons
    first_image_frame = Frame(images_frame)
    b1 = Button(first_image_frame, text='Cargar imagen', 
    width=20,command = lambda:upload_file(0, first_image_frame))
    b1.grid(row=1, column=0)

    b2 = Button(first_image_frame, text='Guardar imagen', 
    width=20,command = lambda:save_img(0))
    b2.grid(row=1, column=1)
    first_image_frame.grid(row=0,column=0)

    third_image_frame = Frame(images_frame)
    b5 = Button(third_image_frame, text='Cargar espectro', 
    width=20,command = lambda:upload_file(1, third_image_frame))
    b5.grid(row=1, column=0)

    b6 = Button(third_image_frame, text='Guardar espectro', 
    width=20,command = lambda:save_img(1))
    b6.grid(row=1, column=1)
    third_image_frame.grid(row=0,column=2)

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