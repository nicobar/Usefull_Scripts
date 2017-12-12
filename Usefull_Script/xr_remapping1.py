old2new_dict = {'Bundle-Ether70.51': 'Bundle-Ether.fcavalie',
                'GigabitEthernet0/7/0/11': 'GigabitEthernet6/6/6/fcavalie',
                }
new_text = []

with open(file, 'r') as fin:
    text_list = fin.readlines()

for line in text_list:
    for intf in old2new_dict.keys():
        if intf in text:
            new_text += [line.replace(old2new_dict[intf])]
            break
    new_text += [line]
