
###############################################
################# IMPORTS #####################
###############################################

import pexpect
import time
import re
from os import listdir
from os.path import isfile, join


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

    cmd_telnet_node = 'telnet ' + node_name
    cmd_h = str.replace(cmd, ' ', '_')

    file_name = node_name + '_' + my_time + '_' + cmd_h + '.txt'

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

    with open(BASE_DIR + file_name, 'w') as fout:
        child.logfile_read = fout
        child.expect(string_to_expect)

    child.terminate()

    return file_name


def get_node_list(file):
    ''' Open a file and returns its content as a list of lines'''
    with open(file, 'r') as f:
        text_list = f.readlines()
    return text_list


def create_text_with_device_command(file_list, base_dir):
    ''' from <switches_>_command files creates output_commnad file
        with "<switch> command output" as lines '''

    for file in file_list:
        input_file_name = base_dir + file
        file_list = file.split('_')
        node = file_list[0]

        cmd_list = file_list[2:-1] + [file_list[-1:][0][:-4]]
        cmd_string = '_'.join(cmd_list)
        output_file_name = base_dir + 'output_' + cmd_string + '.txt'
        with open(input_file_name, 'r') as fin:
            input_text_list = fin.readlines()
        with open(output_file_name, 'a') as fout:
            for line in input_text_list[3:-1]:
                stripped_line = line.strip()
                #line_list = stripped_line.split()
                right_line = node + ' ' + stripped_line + '\n'
                fout.write(right_line)
    print('end writing')


def get_vlan_list(filename):

    with open(filename, 'r') as fin:
        mylist = [line for line in fin.readlines() if 'enet' in line]
    vlan = [int(re.findall('^\d+', vtag)[0]) for vtag in mylist]
    return vlan

#############################################
################# VARIABLES #################
#############################################


BASE = '/mnt/hgfs/VM_shared/Scripts/'
DIR = 'SEARCH_VLAN/'
BASE_DIR = BASE + DIR
DEVICE_FILE = BASE_DIR + 'devices.txt'
BRIDGE_NAME = '10.192.10.8'
MyUsername = 'zzasp70'
MyBridgePwd = "SPr!0094"
MyTacacsPwd = "0094SPra_"
command_list = ['show vlan', ]


############################################
################# MAIN #####################
############################################

# node_list = get_node_list(DEVICE_FILE)
#
# my_time = time_string()
# #
# file_list = []
# for cmd in command_list:
#     for node in node_list:
#         node = node.strip()
#         if node is not '':
#             file_list.append(get_command_output(node, cmd))


#create_text_with_device_command(file_list, BASE_DIR)

path = '/mnt/hgfs/VM_shared/Scripts/SEARCH_VLAN/'
tot_vtag = []
file_list = ['ANOSW021_1612018_show_vlan.txt',
             'ANOSW022_1612018_show_vlan.txt',
             'BAOSW013_1612018_show_vlan.txt',
             'BAOSW016_1612018_show_vlan.txt',
             'BAOSW023_1612018_show_vlan.txt',
             'BAOSW026_1612018_show_vlan.txt',
             'BGOSW011_1612018_show_vlan.txt',
             'BGOSW012_1612018_show_vlan.txt',
             'BOOSW013_1612018_show_vlan.txt',
             'BOOSW014_1612018_show_vlan.txt',
             'BOOSW015_1612018_show_vlan.txt',
             'BOOSW016_1612018_show_vlan.txt',
             'BOOSW023_1612018_show_vlan.txt',
             'BOOSW024_1612018_show_vlan.txt',
             'BOOSW025_1612018_show_vlan.txt',
             'BOOSW026_1612018_show_vlan.txt',
             'BOOSW027_1612018_show_vlan.txt',
             'BOOSW028_1612018_show_vlan.txt',
             'BSOSW011_1612018_show_vlan.txt',
             'BSOSW012_1612018_show_vlan.txt',
             'CAOSW123_1612018_show_vlan.txt',
             'CAOSW126_1612018_show_vlan.txt',
             'CTOSW023_1612018_show_vlan.txt',
             'CTOSW026_1612018_show_vlan.txt',
             'DROSW020_1612018_show_vlan.txt',
             'FIOSW013_1612018_show_vlan.txt',
             'FIOSW014_1612018_show_vlan.txt',
             'FIOSW015_1612018_show_vlan.txt',
             'FIOSW016_1612018_show_vlan.txt',
             'GEOSW011_1612018_show_vlan.txt',
             'GEOSW012_1612018_show_vlan.txt',
             'MIOSW013_1612018_show_vlan.txt',
             'MIOSW014_1612018_show_vlan.txt',
             'MIOSW015_1612018_show_vlan.txt',
             'MIOSW016_1612018_show_vlan.txt',
             'MIOSW033_1612018_show_vlan.txt',
             'MIOSW036_1612018_show_vlan.txt',
             'MIOSW043_1612018_show_vlan.txt',
             'MIOSW044_1612018_show_vlan.txt',
             'MIOSW045_1612018_show_vlan.txt',
             'MIOSW046_1612018_show_vlan.txt',
             'MIOSW050_1612018_show_vlan.txt',
             'MIOSW051_1612018_show_vlan.txt',
             'MIOSW053_1612018_show_vlan.txt',
             'MIOSW054_1612018_show_vlan.txt',
             'MIOSW055_1612018_show_vlan.txt',
             'MIOSW056_1612018_show_vlan.txt',
             'MIOSW057_1612018_show_vlan.txt',
             'MIOSW058_1612018_show_vlan.txt',
             'MIOSW061_1612018_show_vlan.txt',
             'MIOSW062_1612018_show_vlan.txt',
             'MIOSW503_1612018_show_vlan.txt',
             'MIOSW506_1612018_show_vlan.txt',
             'NAOSW113_1612018_show_vlan.txt',
             'NAOSW116_1612018_show_vlan.txt',
             'NAOSW133_1612018_show_vlan.txt',
             'NAOSW136_1612018_show_vlan.txt',
             'NAOSW213_1612018_show_vlan.txt',
             'NAOSW216_1612018_show_vlan.txt',
             'NAOSW223_1612018_show_vlan.txt',
             'NAOSW224_1612018_show_vlan.txt',
             'NAOSW225_1612018_show_vlan.txt',
             'NAOSW226_1612018_show_vlan.txt',
             'PAOSW011_1612018_show_vlan.txt',
             'PAOSW012_1612018_show_vlan.txt',
             'PDOSW013_1612018_show_vlan.txt',
             'PDOSW014_1612018_show_vlan.txt',
             'PDOSW015_1612018_show_vlan.txt',
             'PDOSW016_1612018_show_vlan.txt',
             'PEOSW121_1612018_show_vlan.txt',
             'PEOSW122_1612018_show_vlan.txt',
             'PROSW011_1612018_show_vlan.txt',
             'PROSW012_1612018_show_vlan.txt',
             'RMOSW013_1612018_show_vlan.txt',
             'RMOSW016_1612018_show_vlan.txt',
             'RMOSW023_1612018_show_vlan.txt',
             'RMOSW026_1612018_show_vlan.txt',
             'RMOSW033_1612018_show_vlan.txt',
             'RMOSW034_1612018_show_vlan.txt',
             'RMOSW035_1612018_show_vlan.txt',
             'RMOSW036_1612018_show_vlan.txt',
             'RMOSW043_1612018_show_vlan.txt',
             'RMOSW044_1612018_show_vlan.txt',
             'RMOSW045_1612018_show_vlan.txt',
             'RMOSW046_1612018_show_vlan.txt',
             'RMOSW047_1612018_show_vlan.txt',
             'RMOSW048_1612018_show_vlan.txt',
             'SAOSW011_1612018_show_vlan.txt',
             'SAOSW012_1612018_show_vlan.txt',
             'TOOSW011_1612018_show_vlan.txt',
             'TOOSW012_1612018_show_vlan.txt',
             'TOOSW505_1612018_show_vlan.txt',
             'TOOSW506_1612018_show_vlan.txt',
             'TOOSW507_1612018_show_vlan.txt',
             'TOOSW508_1612018_show_vlan.txt',
             'TSOSW011_1612018_show_vlan.txt',
             'TSOSW012_1612018_show_vlan.txt',
             'VEOSW013_1612018_show_vlan.txt',
             'VEOSW016_1612018_show_vlan.txt']

for filename in file_list:
    filepath = path + filename
    lst = get_vlan_list(filepath)
    tot_vtag += lst
tot_vtag_s = set(tot_vtag)
tot_vtag_l = list(tot_vtag_s)
tot_vtag_l.sort()
print(tot_vtag_l)
