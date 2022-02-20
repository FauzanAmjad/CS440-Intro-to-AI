import heapq, math


class pathfinder:
    def __init__(self, vertices, startx, starty, goalx, goaly, filewidth, filelength, data):
        self.vertices = vertices
        self.startx = startx
        self.starty = starty
        self.goalx = goalx
        self.goaly = goaly
        self.startindex = (startx, starty)
        self.endindex = (goalx, goaly)
        self.filewidth = filewidth
        self.filelength = filelength
        self.data = data

    def hfunction(self, pointx, pointy):
        root2 = math.sqrt(2)
        xminusgoal = abs(pointx - self.goalx)
        yminusgoal = abs(pointy - self.goaly)
        answer = (root2 * min(xminusgoal, yminusgoal)) + max(xminusgoal, yminusgoal) - min(xminusgoal, yminusgoal)
        return answer

    def inisetup(self):
        for key in self.vertices:
            self.vertices[key].gvalue = math.inf
            self.vertices[key].fvalue = self.vertices[key].hvalue
            self.vertices[key].parent = None
            self.vertices[key].is_closed = False

            # change h values
            px = self.vertices[key].coords[0]
            py = self.vertices[key].coords[1]
            d = math.sqrt(pow((px - self.goalx), 2) + pow((py - self.goaly), 2))
            self.vertices[key].hvalue = d
            self.vertices[key].fvalue = d

    def lineofsight(self, sourcex, sourcey, pointx, pointy):
        x0 = sourcex
        y0 = sourcey
        x1 = pointx
        y1 = pointy
        f = 0
        dy = y1 - y0
        dx = x1 - x0
        sy = 0
        sx = 0
        if dy < 0:
            dy = -1 * dy
            sy = -1
        else:
            sy = 1
        if dx < 0:
            dx = -1 * dx
            sx = -1
        else:
            sx = 1
        if dx >= dy:
            while x0 != x1:
                f = f + dy
                addx0 = -1
                addy0 = -1
                if sx == 1:
                    addx0 = 0
                if sy == 1:
                    addy0 = 0
                blocked = 0
                blocked2 = 0
                blocked3 = 0
                a1 = y0 - 1
                a2 = y0 - 1 - 1
                a3 = x0 + addx0 - 1
                if (((y0 + addy0 - 1) < self.filelength) and ((y0 + addy0 - 1) >= 0)) and (
                        ((x0 + (addx0 - 1)) < self.filewidth) and ((x0 + (addx0 - 1)) >= 0)):
                    blocked = self.data[y0 + addy0 - 1][x0 + addx0 - 1]
                if (((y0 - 1) < self.filelength) and (y0 - 1) >= 0) and (
                        ((x0 + addx0 - 1) < self.filewidth) and ((x0 + addx0 - 1) >= 0)):
                    blocked2 = self.data[y0 - 1][x0 + addx0 - 1]
                if (((y0 - 1 - 1) < self.filelength) and ((y0 - 1 - 1) >= 0)) and (
                        ((x0 + addx0 - 1) < self.filewidth) and ((x0 + addx0 - 1) >= 0)):
                    blocked3 = self.data[y0 - 1 - 1][x0 + addx0 - 1]

                if f >= dx:
                    if blocked == 1:
                        return False
                    y0 = y0 + sy
                    f = f - dx

                if f != 0 and blocked == 1:
                    return False
                if dy == 0 and blocked2 == 1 and blocked3 == 1:
                    return False
                x0 = x0 + sx


        else:
            while y0 != y1:
                f = f + dx
                addx0 = -1
                addy0 = -1
                if sx == 1:
                    addx0 = 0
                if sy == 1:
                    addy0 = 0
                blocked = 0
                blocked2 = 0
                blocked3 = 0
                a1 = y0 - 1
                a2 = y0 - 1 - 1
                a3 = x0 + addx0 - 1
                if (((y0 + addy0 - 1) < self.filelength) and ((y0 + addy0 - 1) >= 0)) and (
                        ((x0 + addx0 - 1) < self.filewidth) and ((x0 + addx0 - 1) >= 0)):
                    blocked = self.data[y0 + addy0 - 1][x0 + addx0 - 1]
                if (((y0 - 1) < self.filelength) and (y0 - 1) >= 0) and (
                        ((x0 + addx0 - 1) < self.filewidth) and ((x0 + addx0 - 1) >= 0)):
                    blocked2 = self.data[y0 - 1][x0 + addx0 - 1]
                if (((y0 - 1 - 1) < self.filelength) and ((y0 - 1 - 1) >= 0)) and (
                        ((x0 + addx0 - 1) < self.filewidth) and ((x0 + addx0 - 1) >= 0)):
                    blocked3 = self.data[y0 - 1 - 1][x0 + addx0 - 1]
                if f >= dy:
                    if blocked == 1:
                        return False
                    x0 = x0 + sx
                    f = f - dy

                if f != 0 and blocked == 1:
                    return False
                if dx == 0 and blocked2 == 1 and blocked3 == 1:
                    return False
                y0 = y0 + sy
        return True

    def new_cmp_lt(self, a, b):
        return a.fvalue < b.fvalue

    def Astar(self):


        start=self.vertices.get(self.startindex)
        end=self.vertices.get(self.endindex)

        if start==end:
            print("Path found, Start/End Vertices Are the Same")
            return True

        if start==None or end==None:
            print("Path not found, Start/End Vertices Invalid")
            return False
        # Start
        closed=set()
        self.vertices[self.startindex].parent = None
        self.vertices[self.startindex].gvalue = 0
        tx=self.vertices[self.startindex].coords[0]
        ty=self.vertices[self.startindex].coords[1]
        hvalstart= self.hfunction(tx, ty)
        self.vertices[self.startindex].hvalue = hvalstart
        self.vertices[self.startindex].fvalue = hvalstart
        fringe = []
        tempset=set(fringe)
        heapq.heappush(fringe, self.vertices[self.startindex])
        tempset.add(self.vertices[self.startindex])

        while fringe:
            currentv = heapq.heappop(fringe)
            tempset.remove(currentv)
            if currentv.coords[0] == self.goalx and currentv.coords[1] == self.goaly:
                print("Path found")
                return True
            currentv.is_closed = True
            closed.add(currentv)
            currentneighborlist = currentv.neighbors

            for n in currentneighborlist:
                if n not in closed:

                    if n not in tempset:
                        n.parent=None
                        n.gvalue=math.inf
                        tempx = n.coords[0]
                        tempy = n.coords[1]
                        hval = self.hfunction(tempx, tempy)
                        n.hvalue=hval
                        n.fvalue=hval
                    # Update Vertex if applicable
                    gs = currentv.gvalue
                    # Determine path cost
                    cost = 0
                    nx = n.coords[0]
                    ny = n.coords[1]
                    currx = currentv.coords[0]
                    curry = currentv.coords[1]
                    if nx != currx and ny != curry:
                        cost = math.sqrt(2)
                    else:
                        cost = 1
                    # See if path cost is less
                    if gs == float("inf") or gs + cost < n.gvalue:
                        n.gvalue = gs + cost
                        n.fvalue = n.hvalue + n.gvalue
                        n.parent = currentv

                        if n in tempset:
                            fringe.remove(n)
                            tempset.remove(n)
                        heapq.heapify(fringe)

                        heapq.heappush(fringe, n)
                        tempset.add(n)

        print("No path found")
        return False

    def Thetastar(self):

        start = self.vertices.get(self.startindex)
        end = self.vertices.get(self.endindex)

        if start==end:
            print("Path found, Start/End Vertices Are the Same")
            return True

        if start == None or end == None:
            print("Path not found, Start/End Vertices Invalid")
            return False
        # Reset f's and g's


        # Main part
        # Start
        self.vertices[self.startindex].parent = self.vertices[self.startindex]
        self.vertices[self.startindex].gvalue = 0
        px = self.vertices[self.startindex].coords[0]
        py = self.vertices[self.startindex].coords[1]
        hvalstart = math.sqrt(pow((px - self.goalx), 2) + pow((py - self.goaly), 2))
        self.vertices[self.startindex].hvalue = hvalstart
        self.vertices[self.startindex].fvalue = hvalstart
        fringe = []
        tempset=set(fringe)
        closed=set()

        heapq.heappush(fringe, self.vertices[self.startindex])
        tempset.add(self.vertices[self.startindex])

        while fringe:
            currentv = heapq.heappop(fringe)
            tempset.remove(currentv)
            if currentv.coords[0] == self.goalx and currentv.coords[1] == self.goaly:
                print("Path found")
                return True
            currentv.is_closed = True
            closed.add(currentv)
            currentneighborlist = currentv.neighbors
            for n in currentneighborlist:
                if n not in closed:
                    # Update Vertex if applicable
                    if n not in tempset:
                        n.parent = None
                        n.gvalue = math.inf
                        tempx = n.coords[0]
                        tempy = n.coords[1]
                        hval = math.sqrt(pow((tempx - self.goalx), 2) + pow((tempy - self.goaly), 2))
                        n.hvalue = hval
                        n.fvalue = hval
                    gs = currentv.gvalue
                    # Determine path cost0
                    cost = 0
                    nx = n.coords[0]
                    ny = n.coords[1]
                    currx = currentv.coords[0]
                    curry = currentv.coords[1]
                    if nx != currx and ny != curry:
                        cost = math.sqrt(2)
                    else:
                        cost = 1

                    currparent = currentv.parent
                    parentx = currparent.coords[0]
                    parenty = currparent.coords[1]

                    # Cost between parent and s'
                    distance = math.sqrt(pow((nx - parentx), 2) + pow((ny - parenty), 2))

                    if self.lineofsight(parentx, parenty, nx, ny):
                        if currparent.gvalue + distance < n.gvalue:
                            n.gvalue = currparent.gvalue + distance
                            n.fvalue = n.hvalue + n.gvalue
                            n.parent = currparent
                            if n in tempset:
                                fringe.remove(n)
                                tempset.remove(n)
                            heapq.heapify(fringe)
                            heapq.heappush(fringe, n)
                            tempset.add(n)
                    else:
                        # See if path cost is less
                        if gs == float("inf") or gs + cost < n.gvalue:
                            n.gvalue = gs + cost
                            n.fvalue = n.hvalue + n.gvalue
                            n.parent = currentv
                            if n in tempset:
                                fringe.remove(n)
                                tempset.remove(n)
                            heapq.heapify(fringe)
                            heapq.heappush(fringe, n)
                            tempset.add(n)

        print("No path found")
        return False

    def is_path_bfs(self):
        startvertex = self.vertices[self.startindex]
        visited = []
        q = []
        q.append(startvertex)
        while q:
            currv = q.pop(0)
            nlist = currv.neighbors
            for element in nlist:
                if element not in visited:
                    q.append(element)
                    visited.append(element)
                if element.coords[0] == self.goalx and element.coords[1] == self.goaly:
                    return True
        return False
