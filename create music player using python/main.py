import tkinter as tk
from tkinter import filedialog, PhotoImage, Button, Listbox, Scrollbar, Label, Frame
import os
import pygame.mixer
import random

class MusicPlayerApp:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")
        master.geometry("485x700+290+10")
        master.configure(background='#333333')
        master.resizable(False, False)

        # Initialize pygame.mixer for playing music
        pygame.mixer.init()

        # Initialize current song index
        self.current_song_index = 0

        # Initialize loop status
        self.repeat_all = False
        self.repeat_one = False

        # Create lower frame for buttons
        self.lower_frame = Frame(master, bg="#FFFFFF", width=485, height=180)
        self.lower_frame.place(x=0, y=400)

        # Load image icon for the window
        image_icon = PhotoImage(file=r"create music player using python\logo.png")
        master.iconphoto(False, image_icon)

        # Load GIF frames for animation
        frameCnt = 30
        self.frames = [PhotoImage(file=r'C:/Users/HP/Downloads/Music Player/create music player using python/aa1.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

        # Function to update GIF animation
        def update(ind):
            frame = self.frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            self.label.configure(image=frame)
            master.after(40, update, ind)
        self.label = Label(master)
        self.label.place(x=0, y=0)
        master.after(0, update, 0)

        # Load button images
        self.ButtonPrevious = PhotoImage(file=r"C:/Users/HP/Downloads/Music Player/create music player using python/previous.png")
        self.ButtonPlay = PhotoImage(file=r"C:/Users/HP/Downloads/Music Player/create music player using python/play1.png")
        self.ButtonNext = PhotoImage(file=r"C:/Users/HP/Downloads/Music Player/create music player using python/next.png")
        self.ButtonPause = PhotoImage(file=r"C:/Users/HP/Downloads/Music Player/create music player using python/pause1.png")
        self.ButtonShuffle = PhotoImage(file=r"C:/Users/HP/Downloads/Music Player/create music player using python/shuffle1.png")

        # Create buttons for controlling music playback
        Button(master, image=self.ButtonPrevious, bg="#FFFFFF", bd=0, height=55, width=60, command=self.previous_music).place(x=20, y=499.5)
        Button(master, image=self.ButtonPlay, bg="#FFFFFF", bd=0, height=55, width=60, command=self.play_all_songs).place(x=100, y=499.5)
        Button(master, image=self.ButtonNext, bg="#FFFFFF", bd=0, height=55, width=60, command=self.next_music).place(x=180, y=499.5)
        Button(master, image=self.ButtonPause, bg="#FFFFFF", bd=0, height=55, width=60, command=self.pause_music).place(x=260, y=499.5)
        self.shuffle_button = Button(master, image=self.ButtonShuffle, bg="#FFFFFF", bd=0, height=55, width=60, command=self.shuffle_music)
        self.shuffle_button.place(x=340, y=499.5)

        # Create loop button
        self.loop_button = Button(master, text="Loop Off", bg="#FFFFFF", bd=0, height=2, width=8, command=self.handle_loop_button_click)
        self.loop_button.place(x=420, y=499.5)

        # Load menu image
        self.Menu = PhotoImage(file=r"C:/Users/HP/Downloads/Music Player/create music player using python/menu.png")
        Label(master, image=self.Menu).place(x=0, y=580, width=485, height=120)

        # Create frame for music playlist
        self.Frame_Music = Frame(master, bd=2, relief=tk.RIDGE)
        self.Frame_Music.place(x=0, y=585, width=485, height=100)

        # Button to browse and add music
        Button(master, text="Browse Music", width=59, height=1, font=("calibri", 12, "bold"), fg="Black", bg="#FFFFFF", command=self.add_music).place(x=0, y=550)

        # Create scrollbar for playlist
        self.Scroll = Scrollbar(self.Frame_Music)
        self.Playlist = Listbox(self.Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="grey", selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=self.Scroll.set)
        self.Scroll.config(command=self.Playlist.yview)
        self.Scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.Playlist.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Set an event to trigger when music ends
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT + 1)
        master.bind(pygame.constants.USEREVENT + 1, self.play_next_song)

    def add_music(self):
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs = os.listdir(path)
            for song in songs:
                if song.endswith(".mp3"):
                    self.Playlist.insert(tk.END, song)

    def play_music(self, index=None):
        if index is None:
            index = self.current_song_index
        else:
            self.current_song_index = index
        Music_Name = self.Playlist.get(index)
        pygame.mixer.music.load(self.Playlist.get(index))
        pygame.mixer.music.play()
        if self.repeat_all:
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT + 1)
        elif self.repeat_one:
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT + 2)
        else:
            pygame.mixer.music.set_endevent(0)
        self.Playlist.selection_clear(0, tk.END)
        self.Playlist.selection_set(index)
        self.Playlist.activate(index)

    def pause_music(self):
        pygame.mixer.music.pause()

    def repeat_all_music_loop(self):
        self.repeat_all = not self.repeat_all
        self.repeat_one = False
        self.update_loop_button_text()

    def repeat_one_music_loop(self):
        self.repeat_one = not self.repeat_one
        self.repeat_all = False
        self.update_loop_button_text()

    def handle_loop_button_click(self):
        if not self.repeat_all and not self.repeat_one:
            self.repeat_all = True
            self.loop_button.configure(text="Repeat All")
        elif self.repeat_all and not self.repeat_one:
            self.repeat_all = False
            self.repeat_one = True
            self.loop_button.configure(text="Repeat One")
        else:
            self.repeat_all = False
            self.repeat_one = False
            self.loop_button.configure(text="Loop Off")

    def update_loop_button_text(self):
        if self.repeat_one:
            self.loop_button.configure(text="Repeat One")
        elif self.repeat_all:
            self.loop_button.configure(text="Repeat All")
        else:
            self.loop_button.configure(text="Loop Off")

    def shuffle_music(self):
        playlist = list(self.Playlist.get(0, tk.END))
        random.shuffle(playlist)
        self.Playlist.delete(0, tk.END)
        for song in playlist:
            self.Playlist.insert(tk.END, song)
        # After shuffling, reset current song index
        self.current_song_index = 0

    def next_music(self):
        current_index = self.Playlist.curselection()
        if current_index:
            next_index = current_index[0] + 1
            if next_index < self.Playlist.size():
                self.Playlist.selection_clear(0, tk.END)
                self.Playlist.selection_set(next_index)
                self.Playlist.activate(next_index)
                self.play_music(next_index)

    def previous_music(self):
        current_index = self.Playlist.curselection()
        if current_index:
            prev_index = current_index[0] - 1
            if prev_index >= 0:
                self.Playlist.selection_clear(0, tk.END)
                self.Playlist.selection_set(prev_index)
                self.Playlist.activate(prev_index)
                self.play_music(prev_index)

    def play_next_song(self, event=None):
        self.current_song_index += 1
        if self.current_song_index >= self.Playlist.size():
            if self.repeat_all:
                self.current_song_index = 0
            elif self.repeat_one:
                self.current_song_index -= 1
        self.play_music(self.current_song_index)

    def play_all_songs(self):
        self.current_song_index = 0
        self.play_music()

root = tk.Tk()
app = MusicPlayerApp(root)
root.mainloop()
