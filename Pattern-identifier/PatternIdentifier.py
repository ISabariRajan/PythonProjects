from tkinter import *
from tkinter.ttk import *
from os.path import join as joinpath, dirname, abspath

import core
import GUI.Generic as Generic
import GUI.Notepad as Notepad
import GUI.Sidebar as SideBar

Generic = Generic.Generic()
core = core.Core()

script_dir = dirname(abspath(__file__))
image_dir = joinpath(script_dir, "GUI", "Images")

class PatternIdentifier:
    """Classifier for the pattern Identifier .

    Returns:
        [type]: [description]
    """

    patterns_list = {}

    def __init__(self) -> None:
        """Initialize the class .
        """
        
        # Main window
        self.root = Tk()
        # Title
        self.root.title("Pattern Identifier")

        Generic.center_window(self.root, 900, 500)
        # Heading
        label = Label(self.root, text="Pattern Identifier!", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=10)
        self.sidebar = SideBar.Sidebar(root=self.root, iswindow=False, showaddbutton=True, entrycallback=self.show_tags_of_pattern)
        self.sidebar.get_sidebar().grid(row=2, column=0)
        print(self.sidebar.children())
        self.sidebar.images_dir = image_dir

        self.notepad = Notepad.Notepad(root=self.root, iswindow=False)
        self.notepad_frame = self.notepad.get_frame()
        self.notepad_frame.grid(row=2, column=2, columnspan=5, rowspan=14)

        self.button = Button(self.root, text="Find all", command=lambda: self.search_text_for_all_patterns_and_add_tags()).grid(row=1, column=3, columnspan=2)
        self.reset = Button(self.root, text="Clear Text", command=self.notepad.resetText).grid(row=1, column=6, columnspan=2)

    def search_text_for_all_patterns_and_add_tags(self):
        """Search for text in all the registered patterns and add them to the list of sub - patterns .
        """
        elements = self.sidebar.patterns
        for pattern in elements:
            if "-pskip" in pattern:
                continue
            output = self.search_for_text_in_patterns(pattern)
            self.sidebar.update_total_finds_in_pattern(pattern, output["total"])
            self.patterns_list[pattern] = output
        if len(self.sidebar.patterns) > 1:
            self.show_tags_of_pattern(self.sidebar.patterns[0])

    def show_tags_of_pattern(self, pattern):
        """Show tags of a given pattern .

        Args:
            pattern ([type]): [description]
        """
        self.notepad.add_tags_to_text(self.patterns_list[pattern])

    def search_for_text_in_patterns(self, pattern):
        """Search for text in the notepad .

        Args:
            pattern ([type]): [description]

        Returns:
            [type]: [description]
        """
        full_text = self.notepad.getText()
        finds = []
        total = 0
        for line in full_text.split("\n"):
            core.set_text(line)
            indexes = core.find_patterns_in_text(pattern)
            total += len(indexes)
            finds.append(indexes)
        
        return {
                    "indexes": finds,
                    "total": total,
                    "pattern": pattern
                }

    def run(self):
        # Run
        self.root.mainloop()
    
PatternIdentifier().run()