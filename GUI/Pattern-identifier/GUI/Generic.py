import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
class Generic:
    def __init__(self):
        pass

    def center_window(self, window, width=300, height=300):
        """Center the given window on the screen .

        Args:
            window ([type]): [description]
            width (int, optional): [description]. Defaults to 300.
            height (int, optional): [description]. Defaults to 300.
        """
        # Center the window
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()

        # For left-align
        left = (screenWidth / 2) - (width / 2)

        # For right-align
        top = (screenHeight / 2) - (height /2)

        # For top and bottom
        window.geometry('%dx%d+%d+%d' % (width,
        height,
        left, top))

    def generate_frame_or_window(self, **kwargs):
        """Generate a Tkinter object from the given kwargs

        Returns:
            [type]: [description]
        """
        print(kwargs)
        __thisWidth = 300
        __thisHeight = 300
        tkinter_object = None
        try:
            # Set window size (the default is 300x300)
            __thisWidth = kwargs['width']
            __thisHeight = kwargs['height']
        except KeyError:
            pass

        try:
            # Option to import as Window
            if kwargs["iswindow"]:
                tkinter_object = Tk()
                if kwargs["center"]:
                    self.center_window(tkinter_object, __thisWidth, __thisHeight)
            # Option to import as Frame
            else:
                __root = kwargs['root']
                tkinter_object = Frame(None, width=__thisWidth, height=__thisHeight)
                # tkinter_object.master = __root
                # tkinter_object.pack()
        except KeyError as e:
            e = str(e)
            if "iswindow" in e:
                raise Exception("iswindow is Required")
            elif "root" in e:
                raise Exception("root is Required")
            else:
                raise Exception(e)
        except:
            raise Exception("root is Required")
        
        return tkinter_object