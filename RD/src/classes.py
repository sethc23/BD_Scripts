

class DG():
    def __init__(self):
        self.dg_id=' '
        self.dg_point = ' '
        self.dg_node = ' '
        self.ave_speed=' '
        self.status=' '
        self.deliv_num=' '
        self.travel_time_to_loc=' '
        self.delivery=Delivery()

    def toDict(self):
        t={}
        for k,v in self.__dict__.iteritems():
            if str(type(v)).find('instance')!=-1:
                t.update(v.__dict__.copy())
            else:
                t.update({k:v})
        return t

    def printHeader(self,printer=False,fullHeading=False):
        z= ('id'+'\t'+
               'dg_point'+'\t'+
               'dg_node'+'\t'+
               'ave_speed'+'\t'+
               'status'+'\t'+
               'd_Num'+'\t'+
               'd_TTloc'+'\t')
        z+=self.delivery.printHeader(printer,fullHeading)

        if fullHeading==True:
            z= ('id'+'\t'+
                   'dg_node'+'\t'+
                   'ave_speed'+'\t'+
                   'status'+'\t'+
                   'deliv_num'+'\t'+
                   'travel_time_to_loc'+'\t')
            z+=self.delivery.printHeader(printer,fullHeading)

        if printer == True:
            z='\n'+z+'\n\r'
            print z
            z=z.lstrip('\n')
            z=z.rstrip('\n\r')

        return z

    def toList(self):
        output=[]
        output.append(self.id)
        output.append(self.dg_point)
        output.append(self.dg_node)
        output.append(self.ave_speed)
        output.append(self.status)
        output.append(self.deliv_num)
        output.append(self.travel_time_to_loc)
        output.extend(self.delivery.toList())
        return output

    def toString(self):
#         s=''
#         for x in self.__dict__.iterkeys(): s+=self.__dict__.get(x)+'\t'
#         return s
        return (str(self.id)+'\t'+
                str(self.dg_point)+'\t'+
                str(self.dg_node)+'\t'+
                str(self.ave_speed)+'\t'+
                str(self.status)+'\t'+
                str(self.deliv_num)+'\t'+
                str(self.travel_time_to_loc)+'\t'+
                str(self.delivery.order_time)+'\t'+
                str(self.delivery.start_time)+'\t'+
                str(self.delivery.start_point)+'\t'+
                str(self.delivery.start_node)+'\t'+
                str(self.delivery.end_time)+'\t'+
                str(self.delivery.end_point)+'\t'+
                str(self.delivery.end_node)+'\t'+
                str(self.delivery.total_order_time)+'\t'+
                str(self.delivery.travel_time))
class Delivery():
    def __init__(self):
        self.deliv_id=' '
        self.order_time=' '
        self.start_point=' '
        self.start_node=' '
        self.start_time=' '
        self.end_time=' '
        self.end_point=' '
        self.end_node=' '
        self.total_order_time=' '
        self.travel_time=' '

    def toList(self):
        output=[]
#         for x in self.__dict__.iterkeys(): output.append(self.__dict__.get(x))
        output.append(self.deliv_id)
        output.append(self.order_time)
        output.append(self.start_point)
        output.append(self.start_node)
        output.append(self.start_time)
        output.append(self.end_time)
        output.append(self.end_point)
        output.append(self.end_node)
        output.append(self.total_order_time)
        output.append(self.travel_time)
        return output

    def toString(self):
        s=''
        for x in self.__dict__.iterkeys(): s+=self.__dict__.get(x)+'\t'
        return s

    def printHeader(self,printer,fullHeading):
        z=('del-ID'+'\t'+
           'ord-T'+'\t'+
           'st_P'+'\t'+
           'st_N'+'\t'+
           'st-T'+'\t'+
           'endT'+'\t'+
           'end_P'+'\t'+
           'end_N'+'\t'+
           'totOrd'+'\t'+
           'travT')
        if fullHeading==True:
            z=('deliv_id'+'\t'+
               'order_time'+'\t'+
               'start_point'+'\t'+
               'start_node'+'\t'+
               'start_time'+'\t'+
               'end_time'+'\t'+
               'end_point'+'\t'+
               'end_node'+'\t'+
               'total_order_time'+'\t'+
               'travel_time')
        return z
class Vendor():
    def __init__(self,vendor=''):
        if vendor=='':
            self.vend_id=' '
            self.order_num=' '
            self.delivery=Delivery()
        else:
            self.fromString(vendor)

    def toDict(self):
        t={}
        for k,v in self.__dict__.iteritems():
            if str(type(v)).find('instance')!=-1:
                t.update(v.__dict__.copy())
            else:
                t.update({k:v})
        return t

    def toString(self):
        return (str(self.vend_id)+'\t'+
                # str(self.node)+'\t'+
                str(self.orderNum)+'\t'+
                str(self.delivery.order_time)+'\t'+
                str(self.delivery.start_time)+'\t'+
                str(self.delivery.start_point)+'\t'+
                str(self.delivery.start_node)+'\t'+
                str(self.delivery.end_time)+'\t'+
                str(self.delivery.end_point)+'\t'+
                str(self.delivery.end_node)+'\t'+
                str(self.delivery.total_order_time)+'\t'+
                str(self.delivery.travel_time))

    def printHeader(self,printer=False,fullHeading=False):
        z= ('vend_id'+'\t'+
               # 'v_node'+'\t'+
               'ord_num'+'\t')
        z+=self.delivery.printHeader(printer,fullHeading)

        if fullHeading==True:
            z= ('vend_id'+'\t'+
                   # 'vend_node'+'\t'+
                   'order_num'+'\t')
            z+=self.delivery.printHeader(printer,fullHeading)

        if printer == True:
            z='\n'+z+'\n\r'
            print z
            z=z.lstrip('\n')
            z=z.rstrip('\n\r')

        return z

    def fromString(self,it):
        try:
            self.vend_id=eval(it.split('\t')[0])
        except:
            self.vend_id=it.split('\t')[0]
        # try:
        #     self.vend_node=eval(it.split('\t')[1])
        # except:
        #     self.vend_node=it.split('\t')[1]
        try:
            self.order_num=eval(it.split('\t')[3])
        except:
            self.order_num=it.split('\t')[3]
        try:
            self.delivery.order_time=eval(it.split('\t')[4])
        except:
            self.delivery.order_time=it.split('\t')[4]
        try:
            self.delivery.start_time=eval(it.split('\t')[5])
        except:
            self.delivery.start_time=it.split('\t')[5]
        try:
            self.delivery.start_point=eval(it.split('\t')[6])
        except:
            self.delivery.start_point=it.split('\t')[6]
        try:
            self.delivery.start_node=eval(it.split('\t')[6])
        except:
            self.delivery.start_node=it.split('\t')[6]
        try:
            self.delivery.end_time=eval(it.split('\t')[8])
        except:
            self.delivery.end_time=it.split('\t')[8]
        try:
            self.delivery.end_point=eval(it.split('\t')[9])
        except:
            self.delivery.end_point=it.split('\t')[9]
        try:
            self.delivery.end_node=eval(it.split('\t')[9])
        except:
            self.delivery.end_node=it.split('\t')[9]
        try:
            self.delivery.total_order_time=eval(it.split('\t')[11])
        except:
            self.delivery.total_order_time=it.split('\t')[11]
        try:
            self.delivery.travel_time=eval(it.split('\t')[12])
        except:
            self.delivery.travel_time=it.split('\t')[12]

    def toList(self):
        output=[]
        output.append(self.vend_id)
        # output.append(self.vend_node)
        output.append(self.order_num)
        output.extend(self.delivery.toList())
        return output

    def fromList(self,it_list):
        s=''
        for it in it_list: s+=str(it)+'\t'
        return self.fromString(it)

