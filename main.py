import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from io import BytesIO
import tempfile

from PIL import Image, ImageTk
import cv2


import mysql.connector

# Set up your database connection credentials here
DB_CONFIG = {
    'host': 'localhost',     # <--- CHANGE THIS FROM 'dataret' to 'localhost'
    'user': 'root',          # (Keep your actual MySQL username, usually 'root')
    'password': '0101023',  # (Keep your actual MySQL password, leave blank '' if none)
    'database': 'ImageDatabase' # (Make sure this matches the database you created)
}

def db_save_record(text_value: str, image_bytes: bytes, original_filename: str):
    """Inserts the text and image into the MySQL database."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # We only insert keyword, image_data, and filename now
        sql = """INSERT INTO Images (keyword, image_data, filename) 
                 VALUES (%s, %s, %s)"""
        val = (text_value, image_bytes, original_filename)
        
        cursor.execute(sql, val)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def db_get_image_by_text(text_value: str):
    """Retrieves the image bytes and filename from MySQL using the keyword."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        sql = "SELECT image_data, filename FROM Images WHERE keyword = %s"
        cursor.execute(sql, (text_value,))
        result = cursor.fetchone()
        
        if result:
            return result[0], result[1]  # Returns (image_bytes, filename)
        return None
    finally:
        cursor.close()
        conn.close()


# ============================================================
# TKINTER GUI
# ============================================================

class ImageDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Storage System")
        self.root.geometry("760x700")
        self.root.resizable(False, False)

        self.text_var = tk.StringVar()
        self.current_image_bytes = None
        self.current_image_name = None
        self.preview_photo = None

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="Image Storage System",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=(0, 8))

        subtitle = ttk.Label(
            main_frame,
            text="Enter a name / ID / keyword, upload or capture an image, then submit or download it.",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 15))

        input_frame = ttk.LabelFrame(main_frame, text="Text Information", padding=12)
        input_frame.pack(fill="x", pady=8)

        ttk.Label(input_frame, text="Name / ID / Keyword:").pack(anchor="w")

        text_entry = ttk.Entry(
            input_frame,
            textvariable=self.text_var,
            font=("Segoe UI", 12)
        )
        text_entry.pack(fill="x", pady=(5, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=12)

        upload_btn = ttk.Button(
            button_frame,
            text="Upload Image",
            command=self.upload_image
        )
        upload_btn.grid(row=0, column=0, padx=8, ipadx=10, ipady=5)

        camera_btn = ttk.Button(
            button_frame,
            text="Capture Image",
            command=self.capture_image
        )
        camera_btn.grid(row=0, column=1, padx=8, ipadx=10, ipady=5)

        submit_btn = ttk.Button(
            button_frame,
            text="Submit",
            command=self.submit_data
        )
        submit_btn.grid(row=0, column=2, padx=8, ipadx=20, ipady=5)

        download_btn = ttk.Button(
            button_frame,
            text="Download",
            command=self.download_data
        )
        download_btn.grid(row=0, column=3, padx=8, ipadx=20, ipady=5)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)

        image_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding=12)
        image_frame.pack(fill="both", expand=True, pady=8)

        self.preview_box = tk.Frame(
            image_frame,
            width=420,
            height=300,
            bg="white",
            relief="solid",
            bd=1
        )
        self.preview_box.pack(pady=10)
        self.preview_box.pack_propagate(False)

        self.preview_label = tk.Label(
            self.preview_box,
            text="No image selected",
            bg="white",
            anchor="center"
        )
        self.preview_label.pack(fill="both", expand=True)

        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

    def set_status(self, message):
        self.status_label.config(text=message)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            path = Path(file_path)
            self.current_image_bytes = path.read_bytes()
            self.current_image_name = path.name

            self.show_image_preview(self.current_image_bytes)
            self.set_status(f"Selected image: {self.current_image_name}")

        except Exception as e:
            messagebox.showerror("Upload Error", f"Could not upload image:\n{e}")

    def capture_image(self):
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            messagebox.showerror("Camera Error", "Could not open the camera.")
            return

        messagebox.showinfo(
            "Camera Instructions",
            "Camera will open now.\n\nPress SPACE or C to capture.\nPress ESC or Q to cancel."
        )

        captured_frame = None

        while True:
            ret, frame = camera.read()

            if not ret:
                messagebox.showerror("Camera Error", "Could not read from camera.")
                break

            display_frame = frame.copy()

            cv2.putText(
                display_frame,
                "Press SPACE/C to capture - ESC/Q to cancel",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow("Camera Capture", display_frame)

            key = cv2.waitKey(1) & 0xFF

            if key in [32, ord("c"), ord("C")]:
                captured_frame = frame
                break

            if key in [27, ord("q"), ord("Q")]:
                break

        camera.release()
        cv2.destroyAllWindows()

        if captured_frame is None:
            self.set_status("Camera capture cancelled.")
            return

        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            cv2.imwrite(temp_file.name, captured_frame)

            image_path = Path(temp_file.name)
            self.current_image_bytes = image_path.read_bytes()
            self.current_image_name = "captured_image.jpg"

            self.show_image_preview(self.current_image_bytes)
            self.set_status("Image captured successfully.")

        except Exception as e:
            messagebox.showerror("Capture Error", f"Could not save captured image:\n{e}")

    def show_image_preview(self, image_bytes):
        try:
            image = Image.open(BytesIO(image_bytes))
            image.thumbnail((400, 280))

            self.preview_photo = ImageTk.PhotoImage(image)

            self.preview_label.config(
                image=self.preview_photo,
                text="",
                bg="white"
            )

        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not display image:\n{e}")

    def submit_data(self):
        text_value = self.text_var.get().strip()

        if not text_value:
            messagebox.showwarning("Missing Text", "Please enter a name, ID, or keyword.")
            return

        if self.current_image_bytes is None:
            messagebox.showwarning("Missing Image", "Please upload or capture an image first.")
            return

        try:
            db_save_record(
                text_value=text_value,
                image_bytes=self.current_image_bytes,
                original_filename=self.current_image_name
            )

            messagebox.showinfo("Success", "Data submitted successfully.")
            self.set_status("Data submitted successfully.")

        except NotImplementedError:
            messagebox.showwarning(
                "SQL Not Connected",
                "The GUI is working.\nNow connect db_save_record() to your existing SQL INSERT code."
            )

        except Exception as e:
            messagebox.showerror("Submit Error", f"Could not submit data:\n{e}")

    def download_data(self):
        text_value = self.text_var.get().strip()

        if not text_value:
            messagebox.showwarning("Missing Text", "Please enter a name, ID, or keyword to search.")
            return

        try:
            result = db_get_image_by_text(text_value)

            if result is None:
                messagebox.showinfo("Not Found", "No image found for this text.")
                self.set_status("No image found.")
                return

            image_bytes, filename = result

            self.current_image_bytes = image_bytes
            self.current_image_name = filename

            self.show_image_preview(image_bytes)

            messagebox.showinfo("Success", "Image retrieved successfully.")
            self.set_status(f"Retrieved image: {filename}")

        except NotImplementedError:
            messagebox.showwarning(
                "SQL Not Connected",
                "The GUI is working.\nNow connect db_get_image_by_text() to your existing SQL SELECT code."
            )

        except Exception as e:
            messagebox.showerror("Download Error", f"Could not retrieve image:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDatabaseApp(root)
    root.mainloop()