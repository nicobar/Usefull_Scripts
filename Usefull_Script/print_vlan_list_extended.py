#import ciscoconfparse as c

#po_vlan_string = '7-11,13,14,18,19,22,23,31,32,37,38,43,45,47,49-57,65,69,74-78,91-97,105,130,143,145,156,170-181,184,192-197,260,261,289,299,322-324,327-329,536,537,600-609,614,615,631-639,643-654,721,740,741,820-827,830,831,868,869,878'

po_vlan_string = '1,7,8,17,24,32,40,50,53,55,91-93,99,100,106,115,130,132,145,156,168-170,199,201-205,230-237,240-249,260,261,299,327-329,380-382,598,630,635,820-823,825,827,828,830,850,851,868,869,875,929'

# def get_all_vlan_list(conf)
#     parse = c.CiscoConfParse(conf)
#
#     list_obj = parse.find_objects('vlan')
#     
#     for obj in list_obj:
        
    

def from_range_to_list(range_str):
    
    l = []
    
    h_l = range_str.split('-')
    start = int(h_l[0])
    stop = int(h_l[1])
    for x in range(start,stop+1):
        l.append(x)
    return l

vlan_l = po_vlan_string.split(',')
vlan_set = set()


for v in vlan_l:
    
    if v.find('-') > 0:
        help_l = from_range_to_list(v)
        for elem in help_l:
            vlan_set.add(int(elem))
    else:
        vlan_set.add(int(v))
        
lst = list(vlan_set)
lst.sort()
print (lst)
for i in lst:
    print (i)
