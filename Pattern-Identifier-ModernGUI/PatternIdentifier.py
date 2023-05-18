from tkinter import *
from tkinter import messagebox
import customtkinter

import Utils

from nltk import tokenize, download as nltk_download
from rake_nltk import Rake
nltk_download("stopwords")
nltk_download("punkt")

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class Styles:

    pad_20 = {
        "padx": (20,20),
        "pady": (20,20)
    }

    padx_20 = {
        "padx": 10,
    }

    pady_20_20 = {
        "pady": (20,20)
    }
    pady_20 = {
        "pady": (0, 20)
    }

class App(customtkinter.CTk):

    styles = Styles()
    total_keywords = 0
    keywords = []
    keyword_list = {}
    keyword_elements = {}

    # top_keywords = []
    MAX_KEYWORDS = 20

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Pattern Identifier")
        self.geometry(f"{1150}x{700}")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # create app Name in sidebar
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Pattern Identifier", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, **self.styles.pad_20)

        # Pattern Generation Frame
        self.pattern_generation_selection_frame = customtkinter.CTkFrame(self.sidebar_frame, width=100)
        self.pattern_generation_selection_frame.grid(row=1, column=0, padx=(20, 20), pady=20, sticky="nsew")
        # Pattern Generation Type Selection
        self.pattern_generation_type = StringVar(value="auto")
        self.pattern_generation_type.trace_add("write", lambda a, b, c: self.pattern_generation_type_onchange())
        self.pattern_generation_selection_heading = customtkinter.CTkLabel(self.pattern_generation_selection_frame, text="Select Pattern Generation")
        self.pattern_generation_selection_heading.grid(row=0, column=0, **self.styles.pad_20)
        self.pattern_generation_type_auto_radio = customtkinter.CTkRadioButton(self.pattern_generation_selection_frame, variable=self.pattern_generation_type, text="Auto", value="auto")
        self.pattern_generation_type_auto_radio.grid(row=1, column=0, **self.styles.pady_20)
        self.pattern_generation_type_custom_radio = customtkinter.CTkRadioButton(self.pattern_generation_selection_frame, variable=self.pattern_generation_type, text="Custom", value="custom")
        self.pattern_generation_type_custom_radio.grid(row=2, column=0, **self.styles.pady_20)

        # Pattern Search and Result Frame
        self.pattern_search_and_result_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.pattern_search_and_result_frame.grid(row=2, column=0, sticky="nsew", **self.styles.pad_20)
        self.pattern_search_and_result_frame.grid_columnconfigure(0, weight=8)
        self.pattern_search_and_result_frame.grid_columnconfigure(1, weight=2)
        # Pattern Search
        self.pattern_search_label = customtkinter.CTkLabel(self.pattern_search_and_result_frame, text="No. of keywords")
        self.pattern_search_label.grid(row=0, sticky="w", **self.styles.pad_20)
        self.pattern_search_entry = customtkinter.CTkEntry(self.pattern_search_and_result_frame)
        self.pattern_search_entry.grid(row=1, sticky="nsew", padx=(10,0))
        self.pattern_search_entry.bind("<KeyRelease>", lambda event: self.on_search_button_click(self.pattern_search_entry.get(), stream=True))
        self.pattern_search_button = customtkinter.CTkButton(self.pattern_search_and_result_frame, text="Generate", width=50,
                                                             command=lambda: self.search_for_keyword(self.pattern_generation_type.get(), self.pattern_search_entry.get()))
        self.pattern_search_button.grid(row=1, column=1)
        # Pattern Result
        self.pattern_result_frame = customtkinter.CTkScrollableFrame(self.pattern_search_and_result_frame, label_text="Result")
        self.pattern_result_frame.grid(row=2, columnspan=2, padx=(10,10), pady= (20,20))
        self.pattern_result_frame.grid_columnconfigure(0, weight=8)
        self.pattern_result_frame.grid_columnconfigure(1, weight=1)
        self.pattern_result_frame.grid_columnconfigure(2, weight=1)

        # TextArea
        self.text_area = customtkinter.CTkTextbox(self, width=800, border_width=5, corner_radius=10)
        self.text_area.grid(row=0, column=1, sticky="nsew", rowspan=5, **self.styles.pad_20)
        self.text_area.bind("<KeyRelease>", lambda event: self.search_keyword_in_txtarea())

        # self.progressbar = customtkinter.CTkProgressBar(self, height=30, mode="determinate")
        # self.progressbar.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")

    def pattern_generation_type_onchange(self):
        generation_type = self.pattern_generation_type.get()
        if generation_type == "auto":
            self.pattern_search_label.configure(text="No. of keywords")
            self.pattern_search_button.configure(text="Extract")
        elif generation_type == "custom":
            self.pattern_search_label.configure(text="Enter keywords to search")
            self.pattern_search_button.configure(text="Search")
        # Empty Keywords and its data
        for i in range(len(self.keywords)):
            self.destroy_keyword_row(self.keywords[i])
        self.keywords = []


    def reset_progressbar(self):
        pass

    def tag_textarea(self, tag_data):
        tagname = "tag"
        self.text_area.tag_config(tagname, foreground="green", background="yellow")
        self.text_area.tag_remove(tagname, "1.0", END)
        tag_length = len(tag_data["keyword"])
        line = 1
        for line_indexes in tag_data["indexes"]:
            for index in line_indexes:
                start = str(line) + "." + str(index)
                end = str(line) + "." + str(index + tag_length)
                self.text_area.tag_add(tagname, start, end)
            line += 1
        pass

    def update_element_text(self, element, data):
        """Update text of element

        Args:
            element ([type]): [description]
            data ([type]): [description]
        """
        element.configure(text=f"({data})")

    def on_search_button_click(self, keyword, stream=False):
        if self.pattern_generation_type.get() == "auto":
            return
        if keyword:
            print(keyword, stream)
            keyword_data = self.search_pattern_in_text(keyword)
            self.tag_textarea(keyword_data)

            if not stream:
                self.update_element_text(
                    self.keyword_elements[keyword]["count"],
                    keyword_data["total"]
                )
                self.keyword_list[keyword] = keyword_data

    def tag_first_valid_keyword(self):
        if len(self.keywords) > 0:
            for keyword in self.keywords:
                keyword_data = self.keyword_list[keyword]
                if keyword_data["total"] > 0:
                    self.tag_textarea(keyword_data)
                    break

    def search_keyword_in_txtarea(self):
        """Search for a given keyword in textarea .

        Args:
            keyword ([type]): [description]
        """
        for keyword in self.keywords:
            keyword_data = self.search_pattern_in_text(keyword)
            self.update_element_text(
                self.keyword_elements[keyword]["count"],
                keyword_data["total"]
            )
            self.keyword_list[keyword] = keyword_data
        self.tag_first_valid_keyword()


    def generate_keyword_row(self, textval, lkeyword):
        print("Generating: " + lkeyword)
        label = customtkinter.CTkLabel(self.pattern_result_frame, text=textval)
        label.grid(row=self.total_keywords, sticky="w")
        label.bind("<Button-1>", lambda event: self.tag_textarea(self.keyword_list[lkeyword]))
        count = customtkinter.CTkLabel(self.pattern_result_frame, text="")
        count.grid(row=self.total_keywords, column=1)
        button = customtkinter.CTkButton(self.pattern_result_frame, text="x", width=10, corner_radius=2, fg_color="transparent", text_color=("blue"), command=lambda : self.destroy_keyword_row(lkeyword, True))
        button.grid(row=self.total_keywords, column=2, pady=5, sticky="e")
        self.keyword_elements[lkeyword] = {
            "label": label,
            "count": count,
            "button": button
        }

    def destroy_keyword_row(self, keyword, single=False):
        keyword = keyword.lower()
        element = self.keyword_elements[keyword]
        element["label"].destroy()
        element["count"].destroy()
        element["button"].destroy()
        del self.keyword_elements[keyword]
        del self.keyword_list[keyword]
        if single:
            self.keywords.remove(keyword)

    def search_for_keyword(self, generation_type, keyword):
        if generation_type == "custom":
            klen = len(keyword)
            max_len = 20
            if klen > 0:
                lkeyword = keyword.lower()
                if lkeyword not in self.keywords:
                    if klen > max_len:
                        textval = keyword[:max_len] + ".."
                    else:
                        textval = keyword.ljust(max_len, " ")

                    self.total_keywords += 1
                    self.keywords.append(lkeyword)
                    self.generate_keyword_row(textval, lkeyword)
                self.on_search_button_click(lkeyword)

        elif generation_type == "auto":
            for i in range(len(self.keywords)):
                self.destroy_keyword_row(self.keywords[i])
            self.keywords = []
            self.generate_keywords()
            pass

    def generate_keywords(self):
        big_text = Utils.remove_unwanted_chars(self.text_area.get("1.0", END))
        max_keywords = 0
        try:
            max_keywords = int(self.pattern_search_entry.get())
        except:
            messagebox.showerror("Error!!!", "The Generate keyword value must be an integer")
            return

        rake = Rake()
        rake.extract_keywords_from_text(big_text)
        keywords = rake.get_ranked_phrases()
        keywords = set([keyword for keyword in keywords if len(keyword.split()) == max_keywords])

        # Loop 1 - Find repetition time of keywords
        topkeys = {}
        for keyword in keywords:
            keyword_data = self.search_pattern_in_text(keyword)
            self.keyword_list[keyword] = keyword_data

            # Add keyword data to topkeywords
            total = keyword_data["total"]
            if total not in topkeys:
                topkeys[total] = []
            topkeys[total].append(keyword_data)

        # Identify keywords based on number of times its appearing in text
        topkeys_array = []
        for i in range(0, len(topkeys)):
            if i not in topkeys:
                topkeys_array.append([])
            else:
                topkeys_array.append(topkeys[i])


        # Find top 20 keyword
        count = 0
        for topkey in topkeys_array[::-1]:
            if count > self.MAX_KEYWORDS:
                break
            topkey_array = topkey
            if topkey_array:
                for topkeyword in topkey_array:
                    if count < self.MAX_KEYWORDS:
                        # self.top_keywords.append(topkeyword)
                        # Search the keyword in entire text and update tags
                        keyword = topkeyword["keyword"]
                        self.search_for_keyword("custom", keyword)
                        keyword_data = self.search_pattern_in_text(keyword)
                        self.tag_textarea(keyword_data)
                        self.update_element_text(
                            self.keyword_elements[keyword]["count"],
                            keyword_data["total"]
                        )
                        self.keyword_list[keyword] = keyword_data
                        count += 1
                    else:
                        break

        self.tag_first_valid_keyword()

    def search_pattern_in_text(self, keyword):
        """Search for text in the notepad .

        Args:
            pattern ([type]): [description]

        Returns:
            [type]: [description]
        """
        full_text = self.text_area.get("1.0", END)
        finds = []
        total = 0

        # Code for progression
        lines = full_text.split("\n")
 
        for line in lines:
            indexes = Utils.find_patterns_in_text(line, keyword)
            total += len(indexes)
            finds.append(indexes)
        
        return {
                    "indexes": finds,
                    "total": total,
                    "keyword": keyword
                }


if __name__ == "__main__":
    app = App()
    app.mainloop()