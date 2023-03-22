import customtkinter
from customtkinter import filedialog

from moviepy.editor import *
import wave
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


def selectInputFolder():
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        input_file_address.configure(text="No Folder Selected", text_color="red")
    else:
        input_file_address.configure(text=folder_path, text_color="white")
        root.update()
        

def selectOutputFolder():
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        output_file_address.configure(text="No Folder Selected", text_color="red")
    else:
        output_file_address.configure(text=folder_path, text_color="white")
        root.update()


def merge_audio_video():
    get_files = input_file_address.cget("text") + "\\"
    paste_files = output_file_address.cget("text") + "\\"

    already_converted_files = []

    for filename in os.listdir(paste_files):
        if filename.endswith("mp4"):
            already_converted_files.append(filename.split(".mp4")[0])

    for filename in os.listdir(get_files):
        if filename.endswith("avi"):
            if filename.split(".avi")[0] in already_converted_files:
                print(filename + " - File Already Merged")
            else:
                # Open the input WAV file
                with wave.open(get_files + filename.split(".avi")[0] + ".wav", 'rb') as input_wav:
                    nchannels, sampwidth, framerate, nframes, comptype, compname = input_wav.getparams()

                    with wave.open(get_files + filename.split(".avi")[0] + "1" + ".wav", 'wb') as output_wav:
                        output_wav.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

                        chunk_size = 1024
                        while True:
                            chunk = input_wav.readframes(chunk_size)
                            if not chunk:
                                break
                            output_wav.writeframes(chunk)

                os.remove(get_files + filename.split(".avi")[0] + ".wav")
                os.rename(get_files + filename.split(".avi")[0] + "1" + ".wav", get_files + filename.split(".avi")[0] + ".wav")

                video = VideoFileClip(get_files + filename)
                audio = AudioFileClip(get_files + filename.split(".avi")[0] + ".wav")

                # video_duration = video.duration
                # audio_duration = audio.duration

                # if video.duration > audio.duration:
                #     print("hi")
                #     # If video is longer than audio, add a silent audio clip
                #     audio = CompositeAudioClip([audio.set_start(0.5)])

                audio = CompositeAudioClip([audio.set_start(0.5)])

                video_with_audio = video.set_audio(audio)

                video_with_audio.write_videofile(paste_files + filename.split(".avi")[0] + ".mp4", fps=video.fps)

root = customtkinter.CTk()
root.title("Audio Video Merged")
root.geometry("500x500")
root.resizable(0,0)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Select Input Folder", font=("Roboto", 24))
label.pack(pady=5, padx=10)

input_file_address = customtkinter.CTkLabel(master=frame, text="")
input_file_address.pack(pady=5, padx=10)

input_button = customtkinter.CTkButton(master=frame, text="Input Folder", command=selectInputFolder)
input_button.pack(pady=5, padx=10)

label3 = customtkinter.CTkLabel(master=frame, text="", font=("Roboto", 24))
label3.pack(pady=15, padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="Select Output File", font=("Roboto", 24))
label2.pack(pady=5, padx=10)

output_file_address = customtkinter.CTkLabel(master=frame, text="")
output_file_address.pack(pady=5, padx=10)

output_button = customtkinter.CTkButton(master=frame, text="Output Folder", command=selectOutputFolder)
output_button.pack(pady=5, padx=10)

label4 = customtkinter.CTkLabel(master=frame, text="", font=("Roboto", 24))
label4.pack(pady=15, padx=10)

start_button = customtkinter.CTkButton(master=frame, text="S T A R T", command=merge_audio_video)
start_button.configure(fg_color="black")
start_button.pack(pady=5, padx=10)

root.mainloop()