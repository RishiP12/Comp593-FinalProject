import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import apod_desktop

class APODViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("APOD Viewer")
        self.root.geometry("800x600")

        # Create a Frame for the image
        self.image_frame = ttk.Frame(self.root)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Canvas to display the image
        self.canvas = tk.Canvas(self.image_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a Frame for the APOD details
        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Add labels for the title and explanation
        self.title_label = ttk.Label(self.info_frame, text="APOD Title", font=("Helvetica", 16))
        self.title_label.pack(fill=tk.X, padx=10, pady=5)

        self.explanation_label = ttk.Label(self.info_frame, text="APOD Explanation", wraplength=600, justify=tk.LEFT)
        self.explanation_label.pack(fill=tk.X, padx=10, pady=5)

        # Load the APOD image and info for today
        self.load_apod_image()

    def load_apod_image(self):
        # Get today's APOD info
        apod_date = apod_desktop.get_apod_date()
        apod_id = apod_desktop.add_apod_to_cache(apod_date)
        apod_info = apod_desktop.get_apod_info(apod_id)

        if apod_id == 0:
            print("Error loading APOD.")
            return

        # Display the image on the canvas
        image_path = apod_info['file_path']
        image = Image.open(image_path)
        image = image.resize(apod_desktop.scale_image(image.size), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(400, 300, image=self.photo)

        # Display the title and explanation
        self.title_label.config(text=apod_info['title'])
        self.explanation_label.config(text=apod_info['explanation'])

if __name__ == "__main__":
    root = tk.Tk()
    app = APODViewer(root)
    root.mainloop()
