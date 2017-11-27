
###############################################
################# IMPORTS #####################
###############################################

import pexpect
import time
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

    with open(BASE_DIR + file_name, 'a') as fout:
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
            for line in input_text_list:
                stripped_line = line.strip()
                #line_list = stripped_line.split()
                right_line = node + ' ' + stripped_line + '\n'
                fout.write(right_line)
    print('end writing')


#############################################
################# VARIABLES #################
#############################################


BASE = '/mnt/hgfs/VM_shared/Scripts/'
DIR = 'FORMAL_L2VPN-FORMAL_INTERFACE/'
BASE_DIR = BASE + DIR
DEVICE_FILE = BASE_DIR + 'devices.txt'
BRIDGE_NAME = '10.192.10.8'
MyUsername = 'zzasp70'
MyBridgePwd = "SPra0094"
MyTacacsPwd = "0094SPra_"
command_list = ['show run formal l2vpn | i interface', 'show run formal interface | i "bundle id"']


############################################
################# MAIN #####################
############################################

node_list = get_node_list(DEVICE_FILE)

my_time = time_string()

file_list = []
for cmd in command_list:
    for node in node_list:
        node = node.strip()
        file_list.append(get_command_output(node, cmd))

# file_list = ['BOGSR201_27112017_sh_run_formal_explicit-path.txt',
#              #'FIGSR100_27112017_sh_run_formal_explicit-path.txt',
#              #'MIGSR101_27112017_sh_run_formal_explicit-path.txt',
#              #'MIGSR300_27112017_sh_run_formal_explicit-path.txt',
#              #'NAGSR201_27112017_sh_run_formal_explicit-path.txt',
#              #'PDGSR100_27112017_sh_run_formal_explicit-path.txt',
#              #'RMGSR101_27112017_sh_run_formal_explicit-path.txt',
#              'RMGSR201_27112017_sh_run_formal_explicit-path.txt']


create_text_with_device_command(file_list, BASE_DIR)
