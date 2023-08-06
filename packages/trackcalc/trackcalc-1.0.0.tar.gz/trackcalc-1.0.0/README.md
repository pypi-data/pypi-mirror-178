**trackcalc**

trackcalc is a tool to help you convert a list of tracks like this:

01:33 first track
03:21 second track
...

into something like this:

00:00 first track
01:33 second track
... etc

it takes a tracklist as input, and spits the calculated result to stdout.

You can then redirect stdout into a file, or use sponge to update your tracks file in-place.

ie:

    trackcalc tracks.txt > tracks_o.txt

You can use my other tool, albumsplit, to use this tracks file to split up an mp3 file into tracks.

here is a vim macro I use to reformat tracks:

     $Bd$0Pa 0j
