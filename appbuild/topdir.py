import os.path

class TopDir:
    def __init__(self, marker_file):
        self.topdirs = []
        self.marker_file = marker_file
        self.prev_pn = None

    def topdir(self, pn):
        if self.prev_pn is not None and pn == self.prev_pn: # at the top
            if len(self.topdirs) > 1:
                raise Exception("topdir: multiple marker files found: %s" % self.topdirs)
            elif len(self.topdirs) == 0:
                raise Exception("topdir: no marker file found: %s" % self.marker_file)
            return os.path.dirname(self.topdirs[0])

        self.prev_pn = pn
        marker_pn = os.path.join(pn, self.marker_file)
        #print marker_pn, os.path.exists(marker_pn), os.path.isfile(marker_pn)
        # looks like TOPDIR and topdir are the same filename on MacOS
        if os.path.exists(marker_pn):
            if not os.path.isfile(marker_pn):
                raise Exception("topdir: name clash, marker file %s is directory or else" % marker_pn)
            self.topdirs.append(marker_pn)

        return self.topdir(os.path.dirname(pn))

def topdir(marker_file = 'TOP-DIR'):
    o = TopDir(marker_file)
    pn = os.path.realpath(os.getcwd())
    return o.topdir(pn)

if __name__ == "__main__":
    print "__file__:", __file__
    print topdir(marker_file = "TOP-DIR")
