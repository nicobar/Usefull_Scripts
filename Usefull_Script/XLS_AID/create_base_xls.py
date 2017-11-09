
###############################################
################# IMPORTS #####################
###############################################

import pexpect
import time
#import string
# from os import listdir
# from os.path import isfile, join
#import tempfile

from openpyxl import load_workbook
from openpyxl.workbook import Workbook

#from ciscoconfparse import CiscoConfParse
#from xlwt import Workbook


#################################################
################# Functions #####################
#################################################


def time_string():
    ''' This function returns time in DDMMYYYY format '''

    tempo = time.gmtime()
    return str(tempo[2]) + str(tempo[1]) + str(tempo[0])


def get_command_output(node_name, cmd):
    ''' This function read devices names from file, 
     connects to them and write on file output of a file '''

    cmd_telnet_bridge = 'telnet ' + BRIDGE_NAME

    #nname = node_name.rstrip('\n')
    cmd_telnet_node = 'telnet ' + node_name
    cmd_h = str.replace(cmd, ' ', '_')
    file_name = node_name + '-' + my_time + '_' + cmd_h + '.txt'
    fout = open(BASE_DIR + file_name, 'w')
    lower_string_to_expect = node_name + '#'

    string_to_expect = str.upper(lower_string_to_expect)

    child = pexpect.spawn(cmd_telnet_bridge, encoding='utf-8')

    child.expect('login: ')
    child.sendline(MyUsername)
    child.expect('Password: ')
    child.sendline(MyBridgePwd)
    child.expect('\$')

    child.sendline(cmd_telnet_node)
    child.expect('username: ')
    child.sendline(MyUsername)
    child.expect('password: ')
    child.sendline(MyTacacsPwd)
    child.expect(string_to_expect)
    child.sendline('term len 0')
    child.expect(string_to_expect)

    child.sendline(cmd)

    child.logfile_read = fout

    child.expect(string_to_expect)

    fout.close()
    child.terminate()

    return file_name


def from_range_to_list(range_str):

    l = []

    h_l = range_str.split('-')
    start = int(h_l[0])
    stop = int(h_l[1])
    for x in range(start, stop + 1):
        l.append(x)
    return l


def manage_OSW2OSW_allowed_list(ws, file_name):

    vlan_set = set()
    OUTPUT_XLS = BASE_DIR + 'AID_to_{}_NMP.xls'.format(SITE[:-1])

    fin = open(BASE_DIR + file_name, 'r')
    text = fin.readlines()
    for line in text:
        if 'Po1' in line:
            line = line.strip()
            line_list = line.split()
            vlan_string = line_list[1]
            vlan_list = vlan_string.split(',')
            break

    for v in vlan_list:

        if v.find('-') > 0:
            help_l = from_range_to_list(v)
            for elem in help_l:
                vlan_set.add(int(elem))
        else:
            vlan_set.add(int(v))

    lst = list(vlan_set)
    lst.sort()
    mycol = 1
    max_row = len(lst) + 1

    for elem, myrow in zip(lst, range(1, max_row)):
        ws.cell(row=myrow, column=mycol, value=int(elem))
#     print (lst)
#     for i in lst:
#         print (i)


def manage_simple(ws, node, sheet, file):

    #ws = wb.create_sheet(title=node + '_' + sheet)
    fin = open(BASE_DIR + file, 'r')
    myrow = 1
    for line in fin:
        line = line.strip()
        line_list = line.split()
        for elem, mycol in zip(line_list, range(1, len(line_list) + 1)):
            ws.cell(row=myrow, column=mycol, value=elem)
        myrow += 1


def manage_show_vlan_brief(ws, file):

    fin = open(BASE_DIR + file, 'r')
    myrow = 1

    for line in fin:
        line_list = line.split()
        if line_list[0][0].isnumeric() or line_list[0] == 'show':
            for elem, mycol in zip(line_list, range(1, len(line_list) + 1)):
                ws.cell(row=myrow, column=mycol, value=elem)
            myrow += 1
        else:
            continue


def create_xlsx(node_list, file_list, sheet_list):

    OUTPUT_XLS = BASE_DIR + 'AID_to_{}_NMP.xlsx'.format(SITE[:-1])
    wb = Workbook()
    for node in node_list:

        for sheet, cmd in zip(sheet_list, command_list):
            #ws = wb.create_sheet(title=node + '_' + sheet)
            cmd_split = cmd.split()
            cmd_h = str.replace(cmd, ' ', '_')
            time = file_list[0].split('-')[1].split('_')[0]
            file = node + '-' + time + '_' + cmd_h + '.txt'

            if 'trunk' in cmd_split:
                ws = wb.create_sheet(title=node + '_' + sheet)
                manage_OSW2OSW_allowed_list(ws, file)
            elif 'vlan' in cmd_split and 'brief' in cmd_split:
                ws = wb.create_sheet(title=node + '_' + sheet)
                manage_show_vlan_brief(ws, file)
            else:
                ws = wb.create_sheet(title=node + '_' + sheet)
                manage_simple(ws, node, sheet, file)

    wb.save(filename=OUTPUT_XLS)

#############################################
################# VARIABLES #################
#############################################


BASE = '/mnt/hgfs/VM_shared/VF-2017/NMP/'
SITE = 'BO01/'
SWITCH_1 = 'BOOSW013'
SWITCH_2 = 'BOOSW016'
BASE_DIR = BASE + SITE + 'AID/'
BRIDGE_NAME = '10.192.10.8'
MyUsername = 'zzasp70'
MyBridgePwd = "SP9400ra"
MyTacacsPwd = "0094SPra_"
command_list = ['show interfaces description',
                'show vlan brief | i [1-9]',
                'show standby brief',
                'show vrrp brief',
                'show interfaces trunk | begin Vlans allowed on trunk']
sheet_list = ['show_int_desc',
              'show_vlan_brief',
              'show_stdby_brief',
              'show_vrrp_brief',
              'show_int_trunk']

node_list = ['BOOSW013',
             'BOOSW016']

# DEVICES = 'devices.txt'
# OUTFILE = 'results.txt'

############################################
################# MAIN #####################
############################################

file_list = [
    'BOOSW013-9112017_show_interfaces_trunk_|_begin_Vlans_allowed_on_trunk.txt',
    'BOOSW013-9112017_show_interfaces_description.txt',
    'BOOSW013-9112017_show_standby_brief.txt',
    'BOOSW013-9112017_show_vlan_brief_|_i_[1-9].txt',
    'BOOSW013-9112017_show_vrrp_brief.txt',
    'BOOSW016-9112017_show_interfaces_description.txt',
    'BOOSW016-9112017_show_standby_brief.txt',
    'BOOSW016-9112017_show_vlan_brief_|_i_[1-9].txt',
    'BOOSW016-9112017_show_vrrp_brief.txt',
    'OOSW016-9112017_show_interfaces_trunk_|_begin_Vlans_allowed_on_trunk.txt', ]

my_time = time_string()


# for node in node_list:
#     for cmd in command_list:
#         file_list.append(get_command_output(node, cmd))

create_xlsx(node_list, file_list, sheet_list)
# elaborate_on_files()
