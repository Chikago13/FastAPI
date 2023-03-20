import datetime

class Utils:
    def __init__(self, *args):
        self.args = args
        

    def convert_today(self, dt):
        chislo = dt.split('-')
        res = []
        for i in chislo:
            try:
                num = int(i)
                res.append(num)
            except:
                return False
        if len(res) ==3:
            if res[1] <=12 and res[1] >0 and res[2]<=31 and res[2]>0 and res[0]<2000:
                return datetime.datetime(year=res[0], month=res[1], day=res[2])
            return False
        return False
        
                
                


    

