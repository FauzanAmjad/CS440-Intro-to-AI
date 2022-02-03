class Node:
    def __init__(self, xvalue, yvalue, neighbors,is_closed,parent, gvalue, hvalue):
        self.xvalue=xvalue
        self.yvalue=yvalue
        self.neighbors = neighbors
        self.is_closed = is_closed
        self.parent = None
        self.is_closed = False
        self.gvalue = 0
        self.hvalue = 0
    def close(self):
        self.is_closed= True
    def set_parent(self, newparent):
        self.parent= newparent
    def set_g(self, newg):
        self.gvalue=newg
    def set_h(self, newh):
        self.hvalue=newh


