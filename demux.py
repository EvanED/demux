#!/usr/bin/env python

# Copyright 2011 Evan Driscoll  [driscoll@cs.wisc.edu]
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. A copy
# of the license is included with this distribution as "LICENSE.txt",
# or you may obtain a copy of the License from
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.


import sys

def shift(l):
    """Removes and returns the first element of 'l'"""
    return l.pop(0)
    

def debug(m):
    """Writes the given object to stderr"""
    sys.stderr.write(str(m))
    pass


def demux(specs, inputs):
    """Demux the given 'input's with respect to 'specs'

    - 'inputs' is a list of filenames (or - for stdin) to be read
    
    - 'specs' is a specification of regex -> file that should receive lines
       matching that regex. It is a list of (string, string) tuples; the
       first coordinate of each tuple is a regular expression string, and the
       second coordinate is the name of the file (or - for stdout) that
       should receive those lines.

    Leading and trailing whitespace on each line is removed, and empty lines
    (after that process) are discarded, for whatever reason.

    If there is a line that matches no spec, then there is an assertion
    violation.

    Lines are only printed to the FIRST file with a matching regex.
    """
    
    import re
    # specs comes in as a list of (string, string) tuples. Convert the first
    # string to an actual regex object and the second to the corresponding
    # file object.
    specs = [ (re.compile(pattern), open_or_std(filename, 'w'))
              for (pattern, filename) in specs ]

    for input_name in inputs:
        debug("Processing %s\n" % input_name)
        with open_or_std(input_name, 'r') as input:
            for line in input.readlines():
                line = line.strip()
                if line == '':
                    continue
                match_no = 0
                for (pattern, file) in specs:
                    if re.search(pattern, line):
                        debug('%s ' % (str(match_no),))
                        file.write(line)
                        file.write('\n')
                        break
                    match_no += 1
                else:
                    assert False



def open_or_std(filename, mode):
    """Opens 'filename' with the given 'mode'. If 'filename' is "-", then
    open either stdin or stdout as appropriate (given the mode)."""
    
    #debug('Opening %s as %s\n' % (filename, mode))
    if filename == '-':
        if mode == 'r':
            return sys.stdin
        else:
            assert mode == 'w'
            return sys.stdout
    else:
        return open(filename, mode)

def main():
    argv = sys.argv

    # A spec is a (regex, filename) pair
    specs = []

    # Command line syntax is one of the following:
    #   demux [-e pattern filename]+ [-d filename] -- [filename]*
    #   demux -f specfile [-d filename] -- [filename]*

    shift(argv) # kill the script name
    if argv[0] == '-e':
        # Parse the specs from the command line.
        spec_no = 0
        while len(argv) > 0 and argv[0] == '-e':
            shift(argv) # kill the -e
            pattern = shift(argv)
            file = shift(argv)
            specs.append( (pattern,file) )
            debug('Spec %s: %s <- %s\n' % (str(spec_no), file, pattern) )
            spec_no += 1
    else:
        # Parse the specs from a file
        assert shift(argv) == '-f'
        specs_file = shift(argv)
        with open_or_std(specs_file, 'r') as file:
            debug('Processing specs from file %s' % specs_file)
            spec_no = 0
            for line in file.readlines():
                line = line.strip()
                split = line.split('<-', 1)
                if len(split) != 2:
                    debug('Skipping line %s' % line)
                    continue
                [outfile, pattern] = split
                outfile = outfile.strip()
                pattern = pattern.strip()
                specs.append( (pattern, outfile) )
                debug('Spec %s: %s <- %s\n' % (str(spec_no), outfile, pattern) )
                spec_no += 1

    if len(argv) == 0 or argv[0] != '-d':
        # If len(argv)==0 then the user obviously didn't give a default
        # file. If the next token is not "-d", then either it is "--" or we
        # will discover that fact (and give an error) in a bit. Either way,
        # we put non-matching lines to standard out.
        default_file = '-'
    else:
        assert shift(argv) == '-d'
        default_file = shift(argv)

    specs.append( ('.*', default_file) )

    # Okay, we have all information about output files. Now get inputs.
    if len(argv) > 0:
        assert shift(argv) == '--'
        inputs = argv
    else:
        # No inputs specified; read from stdin
        inputs = ['-']
        
    demux(specs, inputs)



if __name__ == '__main__':
    main()
    debug('\n')

