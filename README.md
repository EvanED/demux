demux
=====

`demux` is a utility to split up the lines of a file into several
different files. It takes /n/ regular expressions and /n/ output
files, and it puts each line of input into the file that corresponds
to the first matching regular expression.

(This differs from the standard `csplit` utility in that the patterns
denote which file the line should go into instead of the points where
the input should be split.)

Installation
------------

There isn't any. Just copy `src/demux.py` into your path somewhere,
and rename it to just `demux` if you wish. Or leave it where it is now
and just specify the path.

Usage
-----

See the included manpage (you can view it with, e.g., `less`) for
usage information.


