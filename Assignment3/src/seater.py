import re

_author__ = "Aonghus Lawlor"
__copyright__ = "Copyright (c) 2015"
__credits__ = ["Aonghus Lawlor"]
__license__ = "All Rights Reserved"
__version__ = "1.0.0"
__maintainer__ = "Aonghus Lawlor"
__email__ = "aonghus.lawlor@insight-centre.org"
__status__ = "Development"

# its a good idea to make a class to hold the various bits of data 
# and functions we need to solve this problem
class Seater:
    
    # this regular expression will give us the command and the rectangular bounding box
    # https://docs.python.org/2/library/re.html#re.MatchObject.group
    pat = re.compile("(.*) (\d+),(\d+) through (\d+),(\d+)")
    def __init__(self, size=1000):
        # need to do some initialisation of data structures here...
        return
    
    def get_cmd(self, line):
        cmd, x1, y1, x2, y2 = Seater.pat.match(line).groups()
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        return cmd, x1, y1, x2, y2
    
    def seat(self, line):
        cmd, x1, y1, x2, y2 = self.get_cmd(line)
        print cmd, x1, y1, x2, y2
        if cmd == 'toggle':
            self.toggle(x1, y1, x2, y2)
        elif cmd == "occupy":
            self.occupy(x1, y1, x2, y2)
        elif cmd == 'empty':
            self.empty(x1, y1, x2, y2)
        else:
            # YIKES!
            pass
        return
    
    def occupy(self, x1, y1, x2, y2):
        #...
        return
    
    def empty(self, x1, y1, x2, y2):
        #...
        return 
    
    def toggle(self, x1, y1, x2, y2):
        # ...
        return
    
    def number_occupied(self):
        # ...
        return
    
if __name__ == '__main__':
    pass

