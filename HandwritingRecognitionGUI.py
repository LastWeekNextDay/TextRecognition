import tkinter as tk
from tkinter import ttk
from ImageProcessor import ImageProcessor


class HandwritingRecognitionGUI:
    def __init__(self, master):
        self.master = master
        self.image_processor = ImageProcessor()
        self.master.title("Handwritten Text Recognition")

        self.canvas_frame = ttk.Frame(master)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=400, height=200)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.console_frame = ttk.Frame(master)
        self.console_frame.pack(fill=tk.BOTH, expand=True)

        self.console = tk.Text(self.console_frame, height=10, bg="#D5D4D4", fg="#000000", bd=2, relief=tk.SUNKEN,
                               state='disabled')
        self.console.pack(fill=tk.BOTH, expand=True)

        self.setup_bindings()
        self.is_drawing = False
        self.processing_timer = None

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_draw_start)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_draw_stop)
        self.master.bind('<space>', lambda event: self.clear_canvas())

    def on_draw_start(self, event):
        self.is_drawing = True
        self.cancel_processing()
        self.clear_text()

    def on_draw(self, event):
        self.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill='black')

    def on_draw_stop(self, event):
        self.is_drawing = False
        self.schedule_processing()

    def schedule_processing(self, delay=1000):
        self.cancel_processing()
        self.processing_timer = self.canvas.after(delay, self.process_image)

    def cancel_processing(self):
        if self.processing_timer is not None:
            self.canvas.after_cancel(self.processing_timer)
            self.processing_timer = None

    def process_image(self):
        if not self.is_drawing:
            self.insert_text("Processing...")
            text = self.image_processor.process_image(self.canvas)
            self.clear_text()
            self.insert_text(text)

    def insert_text(self, text):
        self.console.configure(state='normal')
        self.console.insert(tk.END, f"{text}\n")
        self.console.yview(tk.END)
        self.console.configure(state='disabled')

    def clear_text(self):
        self.console.configure(state='normal')
        self.console.delete("1.0", tk.END)
        self.console.configure(state='disabled')

    def clear_canvas(self):
        self.canvas.delete("all")
        self.cancel_processing()
