#!/usr/bin/env python

import sys

def shift(l):
    return l.pop(0)
    

def debug(m):
    sys.stderr.write(str(m))
    pass


def demux(specs, inputs):
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
    #   demux [-e pattern filename]* [-d filename] -- [filename]*
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
            spec_no = 0
            for line in file.readlines():
                line = line.strip()
                split = line.split('<-', 1)
                if len(split) != 2:
                    continue
                [outfile, pattern] = split
                outfile = outfile.strip()
                pattern = pattern.strip()
                specs.append( (pattern, outfile) )
                debug('Spec %s: %s <- %s\n' % (str(spec_no), outfile, pattern) )
                spec_no += 1

    if len(argv) == 0 or argv[0] != '-d':
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

