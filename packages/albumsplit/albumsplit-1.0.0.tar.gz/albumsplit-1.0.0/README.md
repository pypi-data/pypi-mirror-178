**albumsplit**

albumsplit is a tool to split up full-length album mp3s into individual tracks.

First, you need the mp3 file, and a tracks file, listing the temporal offset of each track, followed by its title, ie:

00:00 first track
01:33 second track (where first track was a minute 33 seconds long
... etc

You can use my other tool, trackcalc, to calculate out these offsets.

then you can split up the mp3 file like this:

    albumsplit "Album Name.mp3" tracks.txt

here is a vim macro I use to reformat tracks:

     $Bd$0Pa 0j
