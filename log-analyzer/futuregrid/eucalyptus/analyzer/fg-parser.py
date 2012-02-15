#! /usr/bin/env python

from pygooglechart import PieChart3D
from pygooglechart import StackedHorizontalBarChart
from pygooglechart import Axis


import re
import json
import pprint
import sys
import os
from datetime import * 


class Instances:

    in_the_future = datetime.strptime("3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    pp = pprint.PrettyPrinter(indent=0)
    data = {}
    
    def __init__(self):
        self.clear()
        self.data

    def clear(self):
        self.data = {}
        return

    def get(self):
        return self.data

    def print_total(self):
        print "total instances = " + str(len(instance))

    def todatetime (self,instance):
        instance["trace"]["teardown"]["start"] = value_todate(instance["trace"]["teardown"]["start"])
        instance["trace"]["teardown"]["stop"] = value_todate(instance["trace"]["teardown"]["stop"])
        instance["trace"]["extant"]["start"] = value_todate(instance["trace"]["extant"]["start"])
        instance["trace"]["extant"]["stop"] = value_todate(instance["trace"]["extant"]["stop"])
        instance["trace"]["pending"]["start"] = value_todate(instance["trace"]["pending"]["start"])
        instance["trace"]["pending"]["stop"] = value_todate(instance["trace"]["pending"]["stop"])
        instance["t_start"] = value_todate(instance["t_start"])
        instance["date"] = value_todate(instance["date"])
        instance["t_end"] = value_todate(instance["t_end"])
        instance["ts"] = value_todate(instance["ts"])

    def tostr(self,instance):
        instance["trace"]["teardown"]["start"] = str(instance["trace"]["teardown"]["start"])
        instance["trace"]["teardown"]["stop"] = str(instance["trace"]["teardown"]["stop"])
        instance["trace"]["extant"]["start"] = str(instance["trace"]["extant"]["start"])
        instance["trace"]["extant"]["stop"] = str(instance["trace"]["extant"]["stop"])
        instance["trace"]["pending"]["start"] = str(instance["trace"]["pending"]["start"])
        instance["trace"]["pending"]["stop"] = str(instance["trace"]["pending"]["stop"])
        instance["ts"] = str(instance["ts"])
        instance["t_start"] = str(instance["t_start"])
        instance["date"] = str(instance["date"])
        instance["t_end"] = str(instance["t_end"])

    def value_todate(self,string):
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    def dump(self,index = "all"):
        if index == "all":
            pp.pprint(self.data)
            self.print_total()
        elif (index >= 0) and (index < len(str)):
            pp.pprint(self.data[index])
        else:
            print "ERROR printing of index " + index

    def json_dump(self):
         string = ""
         for key in all:
            self.tostr (all[key])
         string = json.dumps(all, sort_keys=False, indent=4)
         for key in all:
             print all[key]
         self.todatetime (all[key])
         return string 

    def add (self,datarecord):
        """prints the information for each instance"""
        if datarecord["linetype"] == "print_ccInstance":
            instanceId = datarecord["instanceId"] 
            ownerId = datarecord["ownerId"]
            timestamp = datarecord["ts"]
            status = datarecord["state"].lower()
            t = datarecord["date"]

            id = instanceId + " " + ownerId + " " + str(timestamp)

            try:
                current = instance[id]
                # if were wereto do a data base this line needs to be replaced
            except:
                current = datarecord

            if not ("t_end" in current):
            #time in the future
                f = self.in_the_future

                current["trace"] = {
                    "pending" : {"start" : f, "stop": t},
                    "teardown" : {"start" : f, "stop": t},
                    "extant" : {"start" : f, "stop": t}
                    }
                current["t_end"] = current["date"]
                current["t_start"] = current["ts"] # for naming consitency
                current["duration"] = 0.0

            current["t_end"] = min(current["t_end"], t)
            current["trace"][status]["start"] = min(current["trace"][status]["start"],t)
            current["trace"][status]["stop"] = max(current["trace"][status]["stop"],t)

            instance[id] = current

    def calculate_delta (self):
        """calculates how long each instance runs in seconds"""
        for i in self.data:
            values = self.data[i]
            t_delta = values["t_end"] - values["ts"]
            self.data[i]["duration"] = str(t_delta.total_seconds())

    def calculate_user_stats (self, users, from_date="all", to_date="all"):
        """calculates some elementary statusticks about the instances per user: count, min time, max time, avg time, total time"""

        # hanlde parameters

        process_all = False
        if (type(from_date).__name__ == "str"):
            process_all = (from_date == "all")
            if not process_all:
                date_from = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
                date_to   = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')

        if (type(from_date).__name__ == "None"):
            process_all = True

        if (type(from_date).__name__ == "datetime"):
            date_from = from_date
            date_to = to_date
            process_all = False

        for i in self.data:
            values = self.data[i]
            process_entry = process_all
            
            if not process_all:
                process_entry = (values['ts'] >= date_from) and (values['ts'] < date_to)

            if process_entry:
                name = values["ownerId"]
                t_delta = float(values["duration"])
                try:
                    users[name]["count"] = users[name]["count"] + 1 # number of instances
                except:
                #          count,sum,min,max,avg
                    users[name] = {'count' : 1,
                                   'sum' : 0.0,
                                   'min' : t_delta,
                                   'max' :t_delta,
                                   'avg' : 0.0
                                   }

                users[name]['sum'] += t_delta  # sum of time 
                users[name]['min'] = min (t_delta, users[name]['min'])
                users[name]['max'] = min (t_delta, users[name]['max'])


                for name in users:
                    users[name]['avg'] = float(users[name]['sum']) / float(users[name]['count'])



users = {}

instances = Instances()
instance = instances.data


pp = pprint.PrettyPrinter(indent=4)

def clear():
    users = {}
    instance = {}

    
        
######################################################################
# GENERATE INSTANCE STATISTICS
######################################################################

#instance_c = {"id": null }

#def instance_cache(id):
#    if id == instance_c["id"]:
#        skip
#    else:
#        # witre instance_c[id] to db
#        # instance_c[id] = get instance with id from db
        
    


######################################################################
# GENERATE USER STATISTICS
######################################################################




# Create a chart object of 250x100 pixels

def display_user_stats(users,type="pie"):
    """displays the number of VMs a user is running"""
    values = []
    label_values = []

    max_v = 0
    for name in users:
        count = users[name][0]
        values.append(count)
        label_values.append(name + ":" + str(count))
        max_v = max(max_v, count)

    print values
    print label_values

    if type == "pie": 
        chart = PieChart3D(500, 200)
        chart.set_pie_labels(label_values)
    if type == "bar":
        chart = StackedHorizontalBarChart(500,200,
                                        x_range=(0, max_v))
        # the labels seem wrong, not sure why i have to call reverse
        chart.set_axis_labels('y', reversed(label_values))
        # setting the x axis labels
        left_axis = range(0, max_v + 1, 1)
        left_axis[0] = ''
        chart.set_axis_labels(Axis.BOTTOM, left_axis)

        chart.set_bar_width(10)
        chart.set_colours(['00ff00', 'ff0000'])

    # Add some data
    chart.add_data(values)

    # Assign the labels to the pie data


    # Print the chart URL
    url = chart.get_url()


    os.system ("open -a /Applications/Safari.app " + '"' + url + '"')

 
######################################################################
# CONVERTER 
######################################################################


        
def convert_data_to_list(data,attribute):
    rest = data[attribute]
    rest = re.sub(" ","' , '", rest)
    rest = "['" + rest[1:-1] + "']"
    restdata = eval(rest)
    data[attribute] = restdata

def convert_data_to_dict(data,attribute):
    rest = data[attribute]
    rest = convert_str_to_dict_str(rest[1:-1])
    restdata = eval(rest)
    data[attribute] = restdata

def convert_str_to_dict_str(line):
    line = re.sub(' +',' ',line)
    line = line.strip(" ")
    line = re.sub(' ',',',line)

    # more regular dict
    line = re.sub('=','\'=\'',line)
    line = re.sub(',','\',\'',line)
    line = re.sub('=',' : ',line)
    return '{\'' + line + '\'}'

def parse_type_and_date(line,data):
    # split line after the third ] to (find date, id, msgtype)
    # put the rest in the string "rest"
    m = re.search( r'\[(.*)\]\[(.*)\]\[(.*)\](.*)', line, re.M|re.I)
    data['date'] = datetime.strptime(m.group(1), '%a %b %d %H:%M:%S %Y')
    data['id']   = m.group(2)
    data['msgtype'] = m.group(3)
    rest =  m.group(4)
    rest = re.sub(' +}','}',rest).strip()

    if rest.startswith("running"):
        data['linetype'] = "running"
        return rest 
    elif rest.startswith("calling"):
        data['linetype'] = "calling"
        return rest 
    else:
        location = rest.index(":")
        linetype = rest[0:location]
        data['linetype'] = re.sub('\(\)','',linetype).strip()
        rest = rest[location+1:].strip()
    return rest


def ccInstance_parser(rest,data):
    """parses the line and returns a dict"""

    # replace print_ccInstance(): with linetype=print_ccInstance
    #rest = rest.replace("print_ccInstance():","linetype=print_ccInstance")
    # replace refreshinstances(): with calltype=refresh_instances


    #RunInstances():
    rest = rest.replace("RunInstances():","calltype=run_instances")   # removing multiple spaces
    rest = rest.replace("refresh_instances():","calltype=refresh_instances")   # removing multiple spaces

    #separate easy assignments from those that would contain groups, for now simply put groups as a string
    # all others are merged into a string with *=* into rest
    m = re.search( r'(.*)keyName=(.*)ccnet=(.*)ccvm=(.*)ncHostIdx=(.*)volumes=(.*)groupNames=(.*)', rest, re.M|re.I)
    data['keyName'] = m.group(2).strip()
    data["ccnet"] = m.group(3).strip()
    data["ccvm"] = m.group(4).strip()
    data["volumes"] = m.group(6).strip()
    data["groupNames"] = m.group(7).strip()
    # assemble the rest string
    rest = m.group(1) + "ncHostIdx=" +m.group(5)

    # GATHER ALL SIMPLE *=* assignments into a single rest line and add each entry to dict via eval
    rest = convert_str_to_dict_str(rest)
    restdata = eval (rest)
    data.update(restdata)

    # convert ccvm and ccnet to dict
    convert_data_to_dict(data,"ccvm")
    convert_data_to_dict(data,"ccnet")

    # converts volumes and groupNAmes to list
    convert_data_to_list(data,"groupNames")
    convert_data_to_list(data,"volumes")

    # convert the timestamp
    data["ts"] = datetime.fromtimestamp(int(data["ts"]))


    return data

def refresh_resource_parser(rest,data):
    #[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
    if (rest.find("received") > -1):
        rest = re.sub("received data from","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        m = re.search( r'node=(.*) mem=(.*)[/](.*) disk=(.*)/(.*) cores=(.*)/(.*)', rest, re.M|re.I)
        data["node"] = m.group(1)
        data["mem"] = m.group(2)
        data["mem_max"] = m.group(3)
        data["disk"] = m.group(4)
        data["disk_max"] = m.group(5)
        data["cores"] = m.group(6)
        data["cores_max"] = m.group(7)
    else:
        data["calltype"] = "ignore" 
    return data

    return data


def terminate_instances_param_parser(rest,data):

    rest = rest.strip()
    if rest.startswith("params"):
#params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2

        rest = re.sub("params:","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        m = re.search( r'userId=(.*) instIdsLen=(.*) firstInstId=(.*)', rest, re.M|re.I)
        userid = m.group(1)
        if userid == "(null),":
            data["userId"] = "null"
        else:
            data["userId"] = m.group(1)
        data["instIdsLen"] = m.group(2)
        data["firstInstId"] = m.group(3)
    else:
        data["calltype"] = "ignore" 
    return data



def print_counter (label,counter):
    print label + " = " + str(counter)

def parse_file (filename,analyze,debug=False,progress=True):
    f = open(filename, 'r')
    lines_total = 0
    lines_ignored = 0
    count_terminate_instances = 0
    count_refresh_resource = 0
    count_ccInstance_parser = 0 
    read_bytes = 0
    file_size = os.path.getsize(filename)
    if debug:
        print "SIZE>:" + str(file_size)

    progress_step = file_size / 100
    for line in f:
        ignore = False
        lines_total += 1
        read_bytes += len(line)
        if (debug or progress) and ((lines_total % 1000) == 0):
            percent = int(100 * read_bytes / file_size ) 
            sys.stdout.write("\r%2d%%" % percent)
            sys.stdout.flush()
        if debug:
            print "DEBUG " + str(lines_total) +"> " + line
        data = {}
        rest = parse_type_and_date (line, data)
        if data["linetype"] == "TerminateInstances":
            count_terminate_instances += 1
            terminate_instances_param_parser(rest, data)
        elif data["linetype"] == "refresh_resources":
            count_refresh_resource += 1
            refresh_resource_parser(rest, data)
        elif data["linetype"] == "print_ccInstance":
            count_ccInstance_parser += 1
            ccInstance_parser(rest, data)
        else:
            ignore = True
        if ignore:
            lines_ignored +=1
            if debug:
                print "IGNORE> " + line
        else:
            analyze(data)


        # For Debugging to make it faster terminate at 5
        if debug and (len(instance) > 5):
            break

    print_counter("lines total",lines_total)
    print_counter ("lines ignored = ", lines_ignored)
    print_counter("count_terminate_instances",count_terminate_instances)
    print_counter("count_refresh_resource",count_refresh_resource)
    print_counter("count_ccInstance_parser ",count_ccInstance_parser )

           
    return

#
#####################################################################
# MAIN
#####################################################################
def parse_test(f, line):
    print "------------------------------------------------------------"
    print "- parsetest: " + str(f)
    print "------------------------------------------------------------"
    print "INPUT>"
    print line
    data = {}
    # parse_type_and_date(line,data,rest)
    rest = parse_type_and_date (line, data)
    print "REST>"
    print rest
    f(rest, data)
    print "OUTPUT>"
    print pp.pprint(data)


def test1():
    parse_test(ccInstance_parser, 
               "[Wed Nov  9 19:58:12 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-42BA06B1 reservationId=r-3D3306BC emiId=emi-0B951139 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320693195 ownerId=sharif keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus ccnet={privateIp=10.0.4.4 publicIp=149.165.159.130 privateMac=D0:0D:42:BA:06:B1 vlan=10 networkIndex=4} ccvm={cores=1 mem=512 disk=5} ncHostIdx=24 serviceTag=http://i1:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={sharifnew }")

    return

def test2():
    #
    # RESOURCE PARSER
    #

    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:10 2011][008128][EUCAERROR ] refresh_resources(): bad return from ncDescribeResource(i23) (1)")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:11 2011][008128][EUCADEBUG ] refresh_resources(): done")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:19 2011][008128][EUCAINFO  ] refresh_resources(): called")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6")


    return

def test3():
    #
    # TerminateInstance Parser
    #
    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 10:14:37 2011][021251][EUCADEBUG ] TerminateInstances(): params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016124][EUCADEBUG ] TerminateInstances(): done.")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016168][EUCAINFO  ] TerminateInstances(): called")
    return

def test4():
    parse_file ("/tmp/cc.log.4",jason_dump,debug=False)
    return

def test5(filename,progress=True, debug=False):
    parse_file (filename,instances.add,debug,progress)
    instances.calculate_delta ()
    instances.dump()

    return

def test6():
    users = {}
    instances.calculate_user_stats (users)
    print pp.pprint(users)

    users = {}
    instances.calculate_user_stats (users, "2011-11-06 00:13:15", "2011-11-08 14:13:15")
    print pp.pprint(users)

    users = {}

    a = datetime.strptime("2011-11-06 00:13:15",'%Y-%m-%d %H:%M:%S')
    b = datetime.strptime("2011-11-08 14:13:15",'%Y-%m-%d %H:%M:%S')
        
    instances.calculate_user_stats (users, a, b)
    print pp.pprint(users)
    

    return

def test_display():
    display_user_stats (users)
    display_user_stats (users, type="bar")

def main():



    if sys.version_info < (2, 7):
        print "ERROR: you must use python 2.7 or greater"
        exit (1)
    else:
        print "Python version: " + str(sys.version_info)

    clear()
    
    # test1()
    # test2()
    # test3()


    #    test5("/tmp/cc.log.4",progress=True)
    #    test5("/tmp/cc.log.prints_cc",progress=False, debug=False)
    test5("/tmp/cc.log.prints_cc",progress=True, debug=True)


    
    test6()
    #    test_display()
    #   




if __name__ == "__main__":
    main()
