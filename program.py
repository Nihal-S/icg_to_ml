import sys

registers = {"r0":"",
"r1":"",
"r2":"",
"r3":"",
"r4":"",
"r5":"",
"r6":"",
"r7":"",
"r8":"",
"r9":"",
"r10":"",
"r11":"",
"r12":""
}

output_list = []

def get_a_free_register():
    for regs in registers:
        if(registers[regs] == ""):
            return regs
#do be completed later

filename = sys.argv[1]
f = open(filename,"r")
fileContent = f.read()
rows = fileContent.split("\n")
for row in rows:
    list_quad = row.split(" ")
    # list_quad = 0 operand 1 arg1 2 arg2 3 result
    #print(list_quad)
    if(list_quad[0] == "="):
        if(list_quad[1].isdigit()):
            reg = get_a_free_register()
            output_list.append(["mov "+reg+","+str(hex(int(list_quad[1])))])


print(output_list)