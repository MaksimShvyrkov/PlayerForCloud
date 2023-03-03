from tkinter import *
import tkinter
import customtkinter
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title('Cloud Player')
root.iconbitmap()
root.geometry("400x480")

pygame.mixer.init()


global song_length


def play_time():
    global paused
    if paused:
        return
    current_time = pygame.mixer.music.get_pos() / 100
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = song_list.get(ACTIVE)
    song = f'{root.directory}/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
    elif paused:
        pass
    elif int(slider.get()) == int(current_time):
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(slider.get()))

        converted_current_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        next_time = int(slider.get()) + 1
        slider.config(value=next_time)

    status_bar.after(1000, play_time)


def add_song():
    root.directory = filedialog.askdirectory()
    song = filedialog.askopenfilename(initialdir=root.directory, title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))

    song = song.replace(root.directory + '/', "")
    song = song.replace(".mp3", "")

    song_list.insert(END, song)


def add_many_songs():
    root.directory = filedialog.askdirectory()
    songs = filedialog.askopenfilenames(initialdir=root.directory, title="Choose A Songs", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        song = song.replace(root.directory + '/', "")
        song = song.replace(".mp3", "")
        song_list.insert(END, song)


def play():
    song = song_list.get(ACTIVE)
    song = f'{root.directory}/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()

    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100


paused = False


def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song():
    next_one = song_list.curselection()
    next_one = next_one[0] + 1

    song = song_list.get(next_one)
    song = f'{root.directory}/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    status_bar.config(text='')
    slider.config(value=0)

    song_list.selection_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one, last=None)


def previous_song():
    next_one = song_list.curselection()
    next_one = next_one[0]-1
    song = song_list.get(next_one)
    song = f'{root.directory}/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    status_bar.config(text='')
    slider.config(value=0)

    song_list.selection_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one, last=None)


def slide(x):
    song = song_list.get(ACTIVE)
    song = f'{root.directory}/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))


def volume(x):

    pygame.mixer.music.set_volume(volume_slider.get())

    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100


# Song_list
song_list = Listbox(root, bg="black", fg="#07e897", width=60, selectbackground="gray", selectforeground="#07e897")
song_list.pack(pady=20)

# Button images
play_btn_img = PhotoImage(file='img/play.png')
pause_btn_img = PhotoImage(file='img/pause.png')
back_btn_img = PhotoImage(file='img/back.png')
next_btn_img = PhotoImage(file='img/next.png')

# Control Frame
controls_frame = Frame(root)
controls_frame.pack()

# Control Buttons
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
next_button = Button(controls_frame, image=next_btn_img, borderwidth=0, command=next_song)

play_button.grid(row=0, column=1, padx=10)
pause_button.grid(row=0, column=2, padx=10)
back_button.grid(row=0, column=0, padx=10)
next_button.grid(row=0, column=3, padx=10)

# Menu
my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Song", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Slider position
slider = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.place(relx=0.5, rely=0.73, anchor=tkinter.CENTER)

# Volume Slider
volume_slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume, width=210)
volume_slider.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

root.mainloop()