import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from .packages import Generic

Generic = Generic.Generic()

class Notepad:

    # default window width and height
    # Set window size (the default is 300x300)
    __thisWidth = 300
    __thisHeight = 300
    __old_tags = []
    def __init__(self,**kwargs):
        self.__frame = Generic.generate_frame_or_window(**kwargs)
        try:
            if kwargs["iswindow"]:
                self.__add_window_level_options()
        except KeyError:
            pass
        self.txtarea = StringVar()
        self.__thisTextArea = Text(self.__frame)
        # To add scrollbar
        self.__thisScrollBar = Scrollbar(self.__thisTextArea, orient="vertical")

        # Set icon
        try:
            self.__frame.wm_iconbitmap("Notepad.ico")
        except:
            pass

        self.__configure_text_area()

    def getText(self):
        return self.__thisTextArea.get("1.0", END)

    def resetText(self):
        self.__thisTextArea.delete(1.0,END)

    def update_text(self, text):
        self.__thisTextArea.delete(1.0,END)
        self.__thisTextArea.insert(1.0,text)

    def remove_tags(self, tagname):
        self.__thisTextArea.tag_remove(tagname, "1.0", END)

    def add_tags_to_text(self, tag_data):
        print(tag_data)
        tagname = "tagname"
        self.__thisTextArea.tag_config(tagname, foreground="red", background="yellow")
        self.remove_tags(tagname)
        tag_length = len(tag_data["pattern"])
        line = 1
        for line_indexes in tag_data["indexes"]:
            for index in line_indexes:
                start = str(line) + "." + str(index)
                end = str(line) + "." + str(index + tag_length)
                self.__thisTextArea.tag_add(tagname, start, end)
            line += 1

    def __configure_text_area(self):
        # To make the textarea auto resizable
        # self.__frame.grid_rowconfigure(0, weight=1)
        # self.__frame.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__frame.grid(sticky =(N, E, S, W))
        self.__thisTextArea.grid(row=1, column=0)
        self.__thisScrollBar.grid(row=1, column=1)
        # self.__thisScrollBar.grid(row=0,column=1,sticky=NS)			

        # # Scrollbar will adjust automatically according to the content	
        # self.__thisScrollBar.config(command=self.__thisTextArea.yview)	
        # self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __add_window_level_options(self):
        # Set the window text
        self.__frame.title("Untitled - Notepad")

        self.__file = None
        self.__thisMenuBar = Menu(self.__frame)
        self.__thisFileMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisHelpMenu = Menu(self.__thisMenuBar, tearoff=0)

        Generic.center_window(self.__frame, self.__thisWidth, self.__thisHeight)

        # To open new file
        self.__thisFileMenu.add_command(label="New",
        command=self.__newFile)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open",
        command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save",
        command=self.__saveFile)

        # To create a line in the dialog	
        self.__thisFileMenu.add_separator()										
        self.__thisFileMenu.add_command(label="Exit",
        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",
        menu=self.__thisFileMenu)	

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut",
        command=self.__cut)			

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy",
        command=self.__copy)		

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste",
        command=self.__paste)		

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit",
        menu=self.__thisEditMenu)	

        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About Notepad",
        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help",
        menu=self.__thisHelpMenu)

        self.__frame.config(menu=self.__thisMenuBar)

    def __quitApplication(self):
        self.__frame.destroy()
        # exit()

    def __showAbout(self):
        showinfo("Notepad","Mrinal Verma")

    def __openFile(self):
		
        self.__file = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files","*.*"),
                                        ("Text Documents","*.txt")])

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            # Try to open the file
            # set the window title
            self.__frame.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0,END)

            file = open(self.__file,"r")

            self.__thisTextArea.insert(1.0,file.read())

            file.close()

		
    def __newFile(self):
        self.__frame.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0,END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.txt")])

            if self.__file == "":
                self.__file = None
            else:
                
                # Try to save the file
                file = open(self.__file,"w")
                file.write(self.__thisTextArea.get(1.0,END))
                file.close()
                
                # Change the window title
                self.__frame.title(os.path.basename(self.__file) + " - Notepad")
				
			
        else:
            file = open(self.__file,"w")
            file.write(self.__thisTextArea.get(1.0,END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        # Run main application
        self.__frame.mainloop()

    def get_frame(self):
        return self.__frame


# # Run main application
# notepad = Notepad(width=600,height=400)
# notepad.run()
