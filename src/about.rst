About This Project
********************
ScoreDiff uses the music21 toolkit to compare scores written in the musicxml format in a variety of ways.  For more information about the specific comparisons supported, have a look at the documentation.

This tool could be used to compare different musicxml versions of a piece of music, as well as for comparing two completely different pieces.

Things To Be Aware Of
======================
There are some things to be aware of when using musicxml and finale.  Most importantly, it is possible to encode accidentals in a piece of music that will not show up with finale, but will be heard when the piece is played.  After parsing a musicxml file with music21, it is not possible to distinguish these invisible accidentals from accidentals that will show up with finale, except for in the special case where the hidden accidentals are actually sharps and flats from the key signature, which I've taken care of.  Therefore, hidden accidentals may show up when using the ScoreDiff tool to compare accidentals.  On the other hand, I would probably include hidden accidentals even if I could detect them, since it's always nice to know you're dealing with a poorly made file.

Plans For The Future
=====================
Additional comparisons will likely be added to those currently supported in future versions.

Contact
=========
If you have any questions or comments regarding this project, you can send an email to:
jdubeau@dons.usfca.edu
