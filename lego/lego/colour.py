class Colour:
    def __init__(self, line):
        i = 3
        self.name = line[2]
        self.alpha = 255
        self.edge = None
        while i < len(line):
            if line[i] == 'CODE':
                self.code = int(line[i + 1])
                i += 2
            elif line[i] == 'VALUE':
                self.value = line[i + 1]
                i += 2
            elif line[i] == 'EDGE':
                self.edge = line[i + 1]
                i += 2
            elif line[i] == 'ALPHA':
                self.alpha = int(line[i + 1])
                i += 2
            else:
                i += 1

    def __repr__(self):
        return self.name + ' (' + str(self.code) + ') = ' + self.value + ', ' + str(self.alpha) + ', ' + str(self.edge)
