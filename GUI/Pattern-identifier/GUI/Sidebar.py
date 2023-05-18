from tkinter import *
from .packages import *
Generic = Generic.Generic()

class Sidebar:

    MAX_ELEMENTS = 0
    CURRENT_ELEMENTS = 0
    patterns = []
    images_dir = ""
    entry_callback = None

    def __init__(self, **kwargs):
        """Initialize the widget .

        Raises:
            Exception: [description]
        """
        self.__frame = Generic.generate_frame_or_window(**kwargs)
        try:
            self.MAX_ELEMENTS = kwargs["maxelements"]
        except KeyError:
            pass

        try:
            if kwargs["showaddbutton"]:
                self.entry_callback = kwargs["entrycallback"]
                self.search_var = StringVar()
                self.add_entry_label = Entry(self.__frame, text="Search Text", textvariable=self.search_var, name="search-text-pskip")
                self.add_entry_button = Button(self.__frame, text="+", command=self.add_entry, name="add-pattern-pskip")
                self.add_entry_button.grid(column=1, row=0, padx=10)
                self.add_entry_label.grid(column=0, row=0, padx=10)
        except KeyError as e:
            e = str(e)
            if "entrycallback" in e:
                raise Exception("entrycallback should not be empty when showaddbutton is enabled")
            pass
    
    def children(self):
        """Children of the frame .

        Returns:
            [type]: [description]
        """
        return self.__frame.children

    def get_sidebar(self):
        """Returns the sidebar

        Returns:
            [type]: [description]
        """
        return self.__frame

    def update_total_finds_in_pattern(self, pattern, total):
        """Update the total find in the given pattern .

        Args:
            pattern ([type]): [description]
            total ([type]): [description]
        """
        self.children()[pattern.lower()].config(text= pattern + " (" + str(total) + ")")

    def add_entry(self):
        """Add a new entry to the editor .
        """
        pattern = self.search_var.get()
        lpattern = pattern.lower()
        if len(pattern) > 0:
            if pattern in self.patterns:
                return
            self.CURRENT_ELEMENTS += 1
            Button(self.__frame, text=pattern, command=lambda: self.entry_callback(pattern), border=2, name=lpattern).grid(row=self.CURRENT_ELEMENTS, column=0)
            Button(self.__frame, text=" x ", command=lambda: self.remove_entry(pattern), name=lpattern + "-close-pskip").grid(column=1,row=self.CURRENT_ELEMENTS)
            self.patterns.append(pattern)


    def remove_entry(self, pattern):
        """Remove a pattern from the container .

        Args:
            pattern ([type]): [description]
        """
        lpattern = pattern.lower()
        self.children()[lpattern].destroy()
        self.children()[lpattern + "-close-pskip"].destroy()
        self.patterns.remove(pattern)

    def add_element(self, element):
        """Adds an element to the frame .

        Args:
            element ([type]): [description]
        """
        # button.master = 
        self.__frame.add_element(element)