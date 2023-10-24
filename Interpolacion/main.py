from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import resample as r

#Constants
N_IMG_BUTTONS = 4
IMAGE_COLUMNS=9
IMAGE_SIZE = 270
OPS_DICT = {"Downsampling x2":r.downsample_img, "Upsampling x2":r.upsample_img, "Cuantizacion uniforme":r.cuantize_uniform,
            "Cuantizacion dithering aleatorio":r.cuantize_dither_rand, "Cuantizacion difusion del error":r.cuantize_dither_diffusion}
IMAGE_TYPES = [("Images", "*.png"), ("Images", "*.jpg"), ("Images", "*.jpeg")]
#Global variables
img_arr = [None]*2
tk_imgs = [None]*2

def upload_file(img_index, master):
    filename = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
    img = Image.open(filename).convert("L").resize((IMAGE_SIZE,IMAGE_SIZE))
    tk_img= ImageTk.PhotoImage(img)
    b2 =Button(master,image=tk_img)
    b2.grid(row=0)
    img_arr[img_index] = img
    tk_imgs[img_index] = tk_img

def process_img(frame1, frame2):
    #Reset normal image size
    img_arr[0] = img_arr[0].resize((IMAGE_SIZE, IMAGE_SIZE))
    tk_imgs[0] = ImageTk.PhotoImage(img_arr[0])
    b2 =Button(frame1,image=tk_imgs[0])
    b2.grid(row=0)
    
    img_arr[-1] = OPS_DICT[selected_op.get()](img_arr[0], selected_format.get(), slider.get())
    tk_imgs[-1] = ImageTk.PhotoImage(img_arr[-1])
    if selected_op.get() == "Upsampling x2":
        img_arr[0] = img_arr[0].resize((IMAGE_SIZE*2, IMAGE_SIZE*2), resample=Image.NEAREST)
        tk_imgs[0] = ImageTk.PhotoImage(img_arr[0])
        b2 =Button(frame1,image=tk_imgs[0])
        b2.grid(row=0)
    b3 =Button(frame2, image=tk_imgs[-1])
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
    b1 = Button(first_image_frame, text='Cargar', 
    width=20,command = lambda:upload_file(0, first_image_frame))
    b1.grid(row=1)
    first_image_frame.grid(row=0,column=0)

    third_image_frame = Frame(images_frame)
    b3 = Button(third_image_frame, text='Procesar', 
    width=20,command = lambda:process_img(first_image_frame,third_image_frame))
    b3.grid(row=1, column=0)

    b4 = Button(third_image_frame, text='Guardar', 
    width=20,command = lambda:save_img(img_arr[-1]))
    b4.grid(row=1, column=1)
    third_image_frame.grid(row=0,column=1)

def create_ops(master):
    global slider
    operations_frame = Frame(master)
    operations_frame.grid(row=1)


    #Slider
    slider_frame = LabelFrame(operations_frame, text="Niveles de gris")
    slider_frame.grid(row=0,column=1)
    slider = Scale(slider_frame, from_=2, to=256, orient=HORIZONTAL, resolution=1, length=300, tickinterval=50)
    slider.grid(row=1)
    slider_frame.grid_forget()
    #Dropdown menus
    interp_menu = OptionMenu(operations_frame, selected_format, *r.INTERP)
    interp_menu.grid(row=0, column=1)


    def toggle_widgets(value):
        if (value != "Downsampling x2") and ((value != "Upsampling x2")):
            slider_frame.grid(row=0,column=1)
            interp_menu.grid_forget()
        else:
            slider_frame.grid_forget()
            interp_menu.grid(row=0,column=1)
    operations_menu = OptionMenu(operations_frame, selected_op, *OPS_DICT.keys(), command= toggle_widgets)
    operations_menu.grid(row=0, column=0)

root = Tk()
root.title("Remuestreo e interpolacion")
root.geometry("1200x800+50+50")  # width x height + x + y

#String vars
selected_op = StringVar()
selected_format = StringVar()
selected_op.set(list(OPS_DICT.keys())[0])
selected_format.set(r.INTERP[0])


create_image_frame(root)
create_ops(root)
root.mainloop()