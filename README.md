PiRadio
=======
![http://i.imgur.com/GUYePV8.jpg](http://i.imgur.com/GUYePV8l.jpg)

This is a graphical [MPD][mpd] and [AirPlay][airplay] client for a [Raspberry Pi](pi)
with Adafruit’s 320×240 2.8″ [PiTFT][pitft] touchscreen.
Instead of using the small screen for playback control, it shows the artist and song title in a rather large font.
Also, when streaming from another device via AirPlay, it shows that device’s name.

The base for this was [Adafruit’s tutorial][adaradio] (please go there for setup information),
but it is heavily customized for my personal use, or more specifically, for my wife.
It is just a frontend to drive the LCD.
MPD and [shairport] have to be set up independently.
For AirPlay, I made the shairport daemon pause (rather than stop) MPD while it is streaming.
While MPD is paused, PiRadio will show the AirPlay information instead.
If MPD is stopped I have another script to restart it.

[mpd]: http://www.musicpd.org/
[airplay]: https://en.wikipedia.org/wiki/AirPlay
[pi]: http://www.raspberrypi.org/
[pitft]: https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi
[shairport]: https://github.com/abrasive/shairport
[adaradio]: https://learn.adafruit.com/raspberry-pi-radio-player-with-touchscreen/
