#!/usr/bin/env python
import sys, time, subprocess, os, glob, pygame
from pygame.locals import *

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.display.init()
pygame.font.init()


def process_touch(pos):
    x, y = pos
    if 0 <= x <= 50 and 0 <= y <= 50:
        do_refresh()
    if 270 <= x <= 320 and 0 <= y <= 50:
        do_exit()


def process_key(key):
    if key == K_SPACE:
        do_refresh()
    if key == K_ESCAPE:
        do_exit()


def do_refresh():
    subprocess.call("mpc stop -q", shell=True)


def do_play():
    subprocess.call("mpc play -q", shell=True)


def do_exit():
    screen.fill(black)
    font = pygame.font.Font(None, 24)
    label = font.render("Radioplayer will continue in background", True, white)
    screen.blit(label, (0, 90))
    pygame.display.flip()
    time.sleep(1)
    sys.exit()


def paint_screen():
    # special hack: show pic of Bill and Rebecca during spoken announcements
    if artist == "Radio Paradise":
        screen.blit(radioparadise, (0, 0))
        pygame.display.flip()
        return

    artist_label = artist_font.render(artist, True, black)
    song_label = song_font.render(song, True, black)
    station_label = station_font.render(station, True, black)

    screen.blit(background, (0, 0))
    screen.blit(title, (105, 10))
    screen.blit(refresh, (0, 5))
    screen.blit(exit, (270, 0))
    screen.blit(station_label, (10, 50))
    screen.blit(artist_label, (10, 100))
    screen.blit(song_label, (10, 160))

    pygame.display.flip()


def get_mpd_status():
    global artist, song, station
    try:
        lines = subprocess.check_output("mpc -f '[%name%$][%artist% - ]%title%]|[%file%]'", shell = True).decode('utf-8').split("\n")[:3]
        if len(lines) < 3:
            current = ""
            status = "[not playing]"
            volume = lines[0]
        else:
            current, status, volume = lines
    except subprocess.CalledProcessError:
        current = "Error: cannot talk to mpd"
        status = "[not running]"
        volume = "?"

    if "$" in current:
        station, info = current.split("$", 1)
    else:
        station, info = "", current

    if " - " in info:
        artist, song = info.split(" - ", 1)
    else:
        artist, song = "", info


def mainloop():
    prev_artist = prev_song = prev_station = None
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                process_touch(event.pos)
            if event.type == KEYDOWN:
                process_key(event.key)
        get_mpd_status()
        if artist != prev_artist or song != prev_song or station != prev_station:
            paint_screen()
            prev_artist = artist
            prev_song = song
            prev_station = station
        time.sleep(0.5)


#################### STARTUP CODE ###########################

pygame.mouse.set_visible(False)
screen = pygame.display.set_mode()

# colors
black = 0, 0, 0
white = 255, 255, 255

# images
background = pygame.image.load("background.jpg")
refresh = pygame.image.load("refresh.png")
exit = pygame.image.load("exit.png")
radioparadise = pygame.image.load("radio-paradise.jpg")

# fonts
title_font = pygame.font.Font('fonts/Vollkorn-Bold.ttf', 30)
station_font = pygame.font.Font('fonts/Vollkorn-Regular.ttf', 20)
artist_font = pygame.font.Font('fonts/Vollkorn-Regular.ttf', 50)
song_font = pygame.font.Font('fonts/Vollkorn-Regular.ttf', 30)
title = title_font.render("PiRadio", True, black)

do_play()
mainloop()
