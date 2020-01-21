from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
from functools import partial
import numpy as np
from skimage.metrics import structural_similarity as ssim


choices = {"MSE", "SSIM"}

class Window:
    window = Tk()
    browse1 = None  # first browse button
    browse2 = None  # second browse button
    entryStr1 = StringVar()
    entryBox1 = None  # first entry
    entryStr2 = StringVar()
    entryBox2 = None  # second entry 
    submit = None  # submit button
    res_lab = None
    menu_var = StringVar()  # string for popup menu
    popupMenu = None
    menuFrame = None  # frame for dropdown menu and prompt
    dropdownPrompt = None

    def __init__(self):
        self.window.title("Picture Difference Classifier")
        self.window.geometry("500x250")

        self.browse1 = Button(self.window, text='Browse', command=self.windowsExplore1, height=1, width=10)
        self.browse1.grid(column=1, row=0)

        # entry box 1 config
        self.entryBox1 = Entry(self.window, textvariable=self.entryStr1, width=50)
        self.entryBox1.grid(column=0, row=0)
        self.entryStr1.set("Enter path for picture 1")

        # browse button 2 config
        self.browse2 = Button(self.window, text='Browse', command=self.windowsExplore2, height=1, width=10)
        self.browse2.grid(column=1, row=1)

        # entry box 2 config
        self.entryBox2 = Entry(self.window, textvariable=self.entryStr2, width=50)
        self.entryBox2.grid(column=0, row=1)
        self.entryStr2.set("Enter path for picture 2")

        # submit button config
        self.submit = Button(self.window, text='Submit', command=self.submitPics, height=1, width=10)
        self.submit.grid(column=0, row=3, columnspan=2)

        # result label config
        self.res_lab = Label(self.window, text="")
        self.res_lab.grid(column=0, row=4, columnspan=2, pady=(10,10))

        # menu frame config
        self.menuFrame = Frame(self.window)
        self.menuFrame.grid(column=0, row=2, columnspan=2, pady=10)

        # dropdown menu config
        self.popupMenu = OptionMenu(self.menuFrame, self.menu_var, *choices)
        self.popupMenu.grid(column=1, row=0)
        self.menu_var.set("MSE")

        # dropdown prompt config
        self.dropdownPrompt = Label(self.menuFrame, text="Choose algorithm: ")
        self.dropdownPrompt.grid(column=0, row=0)

    def getAlgo(self):
        return self.menu_var.get()
    
    def windowsExplore1(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.setEntryText1(filename)

    def windowsExplore2(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.setEntryText2(filename)
    
    def setEntryText1(self, new_text):
        self.entryStr1.set(new_text)
        self.entryBox1.xview("end")
    
    def setEntryText2(self, new_text):
        self.entryStr2.set(new_text)
        self.entryBox2.xview("end")
    
    def getEntryText1(self):
        return self.entryStr1.get()
    
    def getEntryText2(self):
        return self.entryStr2.get()
    
    def setResult(self, new_text):
        self.res_lab.configure(text=new_text)
    
    def submitPics(self):
        # get two paths
        path1 = self.getEntryText1()
        path2 = self.getEntryText2()
        
        if(not checkExtension(path1) or not checkExtension(path2)):
            # Catch invalid file type errors
            self.setResult("Invalid File Types")
        else:
            # get two images
            im1 = Image.open(path1).convert("LA")
            data1 = np.asarray( im1, dtype="uint8")
            
            im2 = Image.open(path2).convert("LA")
            data2 = np.asarray( im2, dtype="uint8")

            algoType = self.getAlgo()

            # compare the two images
            result = compareImages(algoType, data1, data2)
            res_str = "%s result = %f" % (algoType, result)
            self.setResult(res_str)


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
        

def checkExtension(path):
    ext = path[-4:]

    # TODO: change this to handle all types of image files
    if(ext == ".jpg" or ext == ".png"):
        return True
    else:
        return False


def compareImages(type, im1, im2):

    if(type == "MSE"):
        res_val = mse(im1, im2)
    elif(type == "SSIM"):
        res_val = ssim(im1, im2, multichannel=True)
    else:
        res_val = -1.0

    return res_val


if __name__ == "__main__":
    window = Window()
    window.window.mainloop()
