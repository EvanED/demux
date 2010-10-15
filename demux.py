#!/u/d/r/driscoll/bin/python

import sys

def debug(m):
    sys.stderr.write(str(m))
    pass

num_matches = 0
num_differ = 0

def demux(pattern, matching, differing, inputs):
    import re
    pattern = re.compile(pattern)

    global num_matches
    global num_differ

    for input in inputs:
        debug("Processing %s\n" % input.name)
        for line in input.readlines():
            line = line.strip()
            if re.search(pattern, line):
                debug('+ ')
                matching.write(line)
                matching.write('\n')
                num_matches += 1
            else:
                debug('- ')
                differing.write(line)
                differing.write('\n')
                num_differ += 1
    

def open_or_std(filename, mode):
    if filename == '-':
        if mode == 'r':
            return sys.stdin
        else:
            assert mode == 'w'
            return sys.stdout
    else:
        return open(filename, mode)

def main():
    if len(sys.argv) <5:
        sys.stderr.write('RTFM\n')
        exit(1)

    argv = sys.argv
    pattern = argv[1]
    matching_out = argv[2]
    differing_out = argv[3]
    input = argv[4:]

    debug('Pattern:   %s\n' % pattern)
    debug('Matching:  %s\n' % matching_out)
    debug('Differing: %s\n' % differing_out)
    debug('Inputs:    %s\n' % input)

    demux(pattern,
          open_or_std(matching_out, 'w'),
          open_or_std(differing_out, 'w'),
          [open_or_std(file, 'r') for file in input])


    debug('\n# matching lines:  %s\n' % str(num_matches))
    debug('# differing lines: %s\n' % str(num_differ))

if __name__ == '__main__':
    main()

