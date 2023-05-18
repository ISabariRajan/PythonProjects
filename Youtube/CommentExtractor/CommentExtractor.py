import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter
from urllib.parse import urlparse, parse_qs
from os.path import join

import youtube_api_extraction
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
    batch_filename = ""
    comment_elements = []
    comments = {}
    output_dir = "Output"

    
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Youtube Comment Extractor")
        self.geometry(f"{1150}x{700}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=90)

        self.tabview = customtkinter.CTkTabview(self, height=80)
        self.tabview.grid(row=0, columnspan=20, sticky="nsew", **self.styles.pady_20)
        self.tabview.add("Single")
        self.tabview.tab("Single").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Single").grid_columnconfigure(1, weight=9)
        # self.tabview.tab("Single").grid_columnconfigure(2, weight=1)
        self.tabview.add("Batch")
        self.tabview.tab("Batch").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Batch").grid_columnconfigure(1, weight=8)
        self.tabview.tab("Batch").grid_columnconfigure(2, weight=1)
        

        # Option "Batch"
        self.batch_input_label = customtkinter.CTkLabel(self.tabview.tab("Batch"), text="Select text file containing data: ")
        self.batch_input_label.grid(row=0, sticky="w")
        self.batch_input_entry = customtkinter.CTkEntry(self.tabview.tab("Batch"))
        self.batch_input_entry.grid(row=0, column=1,sticky="nsew")
        self.batch_input_button = customtkinter.CTkButton(self.tabview.tab("Batch"), text="Browse", command=self.select_file)
        self.batch_input_button.grid(row=0, column=2)

        # Option "Single"
        self.single_input_label = customtkinter.CTkLabel(self.tabview.tab("Single"), text="Enter Youtube video URL: ")
        self.single_input_label.grid(row=0, sticky="w")
        self.single_input_entry = customtkinter.CTkEntry(self.tabview.tab("Single"))
        self.single_input_entry.grid(row=0, column=1,sticky="nsew")
    
        # Scrape Button
        self.progress_frame = customtkinter.CTkFrame(self, height=20)
        self.progress_frame.grid(row=1, columnspan=10, sticky="nsew", **self.styles.pady_20)
        self.progress_frame.grid_rowconfigure(0, weight=1)
        self.scrape_button = customtkinter.CTkButton(self.progress_frame, text="Extract / Scrape", command=self.extract_comments)
        self.scrape_button.grid(row=0, column=0, **self.styles.pad_20)
        self.scrape_progress = customtkinter.CTkLabel(self.progress_frame, text="No Scrapping in Progress")
        self.scrape_progress.grid(row=0, column=1)
        

        # Result Frame
        self.output_frame = customtkinter.CTkFrame(self, height=500)
        self.output_frame.grid(row=2, sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=8)
        self.output_frame.grid_columnconfigure(1, weight=2)
        self.output_frame.grid_rowconfigure(0, weight=1)

        self.result_frame = customtkinter.CTkScrollableFrame(self.output_frame, label_text="Result")
        self.result_frame.grid(row=0, sticky="nsew")
        thead_no = customtkinter.CTkLabel(self.result_frame, text="#")
        thead_no.grid(row=0, **self.styles.padx_20)
        thead_comments = customtkinter.CTkLabel(self.result_frame, text="Comments")
        thead_comments.grid(row=0, column=1, sticky="w", **self.styles.padx_20)

        self.export_frame = customtkinter.CTkFrame(self.output_frame)
        self.export_frame.grid(row=0, column=1, sticky="news")
        self.export_label = customtkinter.CTkLabel(self.export_frame, text="Export Options", font=customtkinter.CTkFont(size=20))
        self.export_label.grid(row=0, columnspan=10, sticky="w", **self.styles.pad_20)
        self.auto_export_checkbox = customtkinter.CTkCheckBox(self.export_frame, text="Auto Export")
        self.auto_export_checkbox.grid(row=1, column=1, **self.styles.padx_20)
        self.export_button = customtkinter.CTkButton(self.export_frame, text="Export", command=self.export)
        self.export_button.grid(row=1, column=0, **self.styles.padx_20)

    def extract_comments_from_url(self, url, auto=False):
        url = url.strip()
        print(f"Extracting from {url}")
        self.scrape_progress.configure(text="Scraping: " + url + " ")
        self.video_id = parse_qs(urlparse(url).query)["v"][0]
        self.comments[self.video_id] = youtube_api_extraction.scrape_youtube_comments(self.video_id)
        print(self.comments[self.video_id].keys())

        if auto:
            pass
        else:
            count = 1
            for data in self.comments[self.video_id]["data"]:
                new_count = (count%20) + 1
                customtkinter.CTkLabel(self.result_frame, text=str(new_count)).grid(row=new_count, **self.styles.padx_20)
                element = customtkinter.CTkLabel(self.result_frame, text=data[1])
                element.grid(row=new_count, column=1, sticky="w", **self.styles.padx_20)
                self.comment_elements.append(element)
                count += 1
        time.sleep(1)

    def extract_comments(self):
        threads = []
        current_tab = self.tabview.get().lower()
        urls = []
        auto = self.auto_export_checkbox.get()
        if current_tab == "batch":
            with open(self.batch_filename, "r") as f:
                urls = f.readlines()
        if current_tab == "single":
            urls = [self.single_input_entry.get()]

        print(urls)
        if auto:
            for url in urls:
                x = threading.Thread(target=self.extract_comments_from_url, args=(url,), daemon=True, name=url).start()
                # self.extract_comments_from_url(url)
                threads.append(x)
                self.export()
        else:
            for url in urls:
                x = threading.Thread(target=self.extract_comments_from_url, args=(url,), daemon=True, name=url).start()
                # self.extract_comments_from_url(url)
                threads.append(x)
                # x.
            self.video_id = "output"
        
        # for index, t in enumerate(threads):
        #     self.scrape_progress.configure(text="Scraping: " + threading.current_thread().getName() + " ")
        #     t.join()




    def select_file(self):
        file_types = [
            ("Text Files", "*.txt"),
        ]
        self.batch_filename = filedialog.askopenfilename(
            title="Select Batch Data",
            initialdir="/",
            filetypes=file_types
        )
        self.batch_input_entry.delete(0, END)
        self.batch_input_entry.insert(0, self.batch_filename)

    def export(self):
        print("Start Exporting")
        with open(join(self.output_dir, self.video_id + ".txt"), "w", encoding="utf-8") as f:
            for element in self.comment_elements:
                f.write(element.cget("text").encode("utf-8").decode("utf-8") + "\n")

    def run(self):
        self.mainloop()
    


app = App()
app.run()