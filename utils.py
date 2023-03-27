import datetime, json



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
            if res[1] <=12 and res[1] >0 and res[2]<=31 and res[2]>0 and res[0]>2000:
                return datetime.datetime(year=res[0], month=res[1], day=res[2])
            return False
        return False
        

    # def convert_datetime_str(self, data):
    #     str_data = datetime.datetime.strptime(data, "%Y-%m-%d")
    #     print(str_data, type(str_data))
    #     return str_data.strftime("%Y-%m-%d")
    
    def convert_datetime_str(self, data):
        str_data = data.strftime("%Y-%m-%d")
        return str_data


# er = Utils()
# data = datetime.datetime(year=2023, month=4, day=2)
# print(er.convert_today("2023-01-30"))
    

# print(er.convert_datetime_str(data))