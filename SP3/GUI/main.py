import tkinter as tk
from tkinter import filedialog
import subprocess
import os

class VideoToAudioConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Video to Audio Converter")

        self.video_path = tk.StringVar()
        self.audio_format = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Select Video File:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.video_path, width=40, state="disabled").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Browse", command=self.browse_video).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.master, text="Select Audio Format:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        tk.OptionMenu(self.master, self.audio_format, "mp2", "mp3", "wav").grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.master, text="Convert", command=self.convert_video).grid(row=2, column=1, pady=20)

    def browse_video(self):
        file_path = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects",
                                              filetypes=(("video files", "*.mp4"),
                                                         ("all files", "*.*")))
        if file_path:
            self.video_path.set(file_path)

    def convert_video(self):
        input_video = self.video_path.get()
        output_format = self.audio_format.get()

        if not input_video:
            tk.messagebox.showerror("Error", "Please select a video file.")
            return

        if not output_format:
            tk.messagebox.showerror("Error", "Please select an audio format.")
            return

        output_file = os.path.join(os.path.dirname(input_video), "result." + output_format)

        try:
            subprocess.run(["ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", output_file])
            tk.messagebox.showinfo("Success", f"Conversion complete. Audio saved as 'result.{output_format}'")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToAudioConverter(root)
    root.mainloop()
