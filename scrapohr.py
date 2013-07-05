class Scrapohr:

    def __init__(self, data):
        self.data = data
        self.curr = ord(data[0])
        self.curridx = 0
        self.currbits = 8
        self.currbidx = 0

    def fillBuffer(self, bytes):
        if bytes > 0:
            self.currbits += 8 * bytes

        for i in range(0, bytes):
            self.curridx += 1
            if self.curridx < len(self.data):
                self.curr *= 256
                self.curr += ord(self.data[self.curridx])

    def getBits(self, count):
        while count > self.currbits:
            self.fillBuffer(1)

        ret = self.curr >> (self.currbits-count)
        self.curr = self.curr % (2**(self.currbits-count))
        self.currbits -= count
        self.currbidx += count

        if ret < 0 or ret > (2**count)-1:
            raise Exception('getBits(): Something was wrong')

        return ret

    def align(self, count):
        while (self.currbidx % count) != 0:
            self.curr = self.curr % (2**(self.currbits-1))
            self.currbidx += 1
            self.currbits -= 1

    def getBytes(self, count):
        return self.getBits(count*8)

    def getLBytes(self, count):
        ret = []
        for i in range(0, count):
            ret.append(self.getBytes(1))
        return ret

class ScrapohrPro(Scrapohr):

    def __init__(self, data):
        Scrapohr.__init__(self, data)

    def getASCIIString(self, size):
        ret = ''
        for i in range(0, size):
            b = self.getBytes(1)
            ret += chr(b)
        return ret

    def getUI8(self, le=True, align=8):
        self.align(align)
        return self.getBytes(1)

    def getUI16(self, le=True, align=8):
        self.align(align)
        b = [self.getBytes(1), self.getBytes(1)]
        if le:
            return b[0]*(2**8) + b[1]
        else:
            return b[1]*(2**8) + b[0]

    def getUI32(self, le=True, align=8):
        self.align(align)
        b = [self.getBytes(1), self.getBytes(1), self.getBytes(1), self.getBytes(1)]
        if le:
            return b[0]*(2**24) + b[1]*(2**16) + b[2]*(2**8) + b[3]
        else:
            return b[3]*(2**24) + b[2]*(2**16) + b[1]*(2**8) + b[0]

    def getSBits(self, count):
        r = self.getBits(count)
        if r >= 2**(count-1):
            r = -(~r+1)
        return r