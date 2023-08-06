from nudisxs import _nudisxs as xs
class disxs:
    def initpdf(self,name):
        xs.initpdf(name)
    def xs_cc(self,Enu,x,y):
        return xs.d2sdiscc_dxdy(Enu,x,y)
