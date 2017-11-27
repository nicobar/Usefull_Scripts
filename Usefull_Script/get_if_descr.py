#!/usr/local/bin/python

# Get CAM from each devices in devices.txt

###############################################
################# IMPORTS #####################
###############################################

import pexpect
import time
#import string
from os import listdir
from os.path import isfile, join
#import tempfile

#from ciscoconfparse import CiscoConfParse
#from xlwt import Workbook


#################################################
################# Functions #####################
#################################################


def time_string():
    # This function returns time in DDMMYYYY format
    # package time

    tempo = time.gmtime()
    return str(tempo[2]) + str(tempo[1]) + str(tempo[0])


def get_command_output():
    # This function read devices names from file,
    # connects to them and write on file output of a file

    devices_file = BASE_DIR + DEVICES

    cmd_telnet_bridge = 'telnet ' + BRIDGE_NAME

    fin = open(devices_file, 'r')

    nn_list = fin.read()
    list_fin = nn_list.split()
    for node_name in list_fin:

        nname = node_name.rstrip('\n')
        cmd_telnet_node = 'telnet ' + nname
        nname_time = nname + '-' + my_time
        fout = open(BASE_DIR + nname_time + '.txt', 'w')
        lower_string_to_expect = nname + '#'

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

        child.sendline(CMD)

        child.logfile = fout

        child.expect(string_to_expect)

        fout.close()
        child.terminate()

    fin.close()


def elaborate_on_files():
    # This function read file (in this case one show command per file whose filename is the device)
    # then consider the rigt lines and prepend th name of devices

    fout = open(BASE_DIR + OUTFILE, 'a')
    onlyfiles = [f for f in listdir(BASE_DIR) if isfile(join(BASE_DIR, f))]
    for fin_name in onlyfiles:
        node = fin_name.split('-')[0]
        if fin_name == ".DS_Store" or fin_name == OUTFILE or fin_name == DEVICES:
            continue
        else:
            fin = open(BASE_DIR + fin_name, 'r')
            f_in = fin.read()
            text_list = str.split(f_in, '\r\n')
            for line_h in text_list[2:-1]:
                line = line_h.rstrip()
                right_line = node + '\t' + line + '\n'
                fout.write(right_line)
            fin.close()
    fout.close()


#############################################
################# VARIABLES #################
#############################################


BASE_DIR = '/Users/aspera/py3/descr/'
BRIDGE_NAME = '10.192.10.8'
MyUsername = 'zzasp70'
MyBridgePwd = 'spRA0094'
MyTacacsPwd = '0094SPra'
CMD = 'show interfaces description'
DEVICES = 'devices.txt'
OUTFILE = 'results.txt'

############################################
################# MAIN #####################
############################################
my_time = time_string()
get_command_output()
elaborate_on_files()
