import ciscoconfparse as c


old2new_dict = {'Bundle-Ether70': 'Bundle-fcavalie',
                'GigabitEthernet0/7/0/11': 'GigabitEthernet6/6/6/fcavalie',
                }

file = '/mnt/hgfs/VM_shared/VF-2017/XR/BOVPE013.txt'

with open(file, 'r') as fin:
    text = fin.read()

#(r'^interface')

for intf in old2new_dict.keys():
    if intf in text:
        new_text = text.replace(intf, old2new_dict[intf])
        text = new_text


with open('/mnt/hgfs/VM_shared/VF-2017/XR/new_text.txt', 'w') as fout:
    fout.write(new_text)

with open('/mnt/hgfs/VM_shared/VF-2017/XR/text.txt', 'w') as fout:
    fout.write(text)

parse = c.CiscoConfParse('/mnt/hgfs/VM_shared/VF-2017/XR/new_text.txt')
intf_obj_list = parse.find_objects_w_all_children(parentspec, childspec, ignore_ws)