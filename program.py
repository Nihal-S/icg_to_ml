import sys

flag_div = 0

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

# function to return key for any value 
def get_key(val): 
	for key, value in registers.items(): 
		if val == value: 
			return key 

	return "key doesn't exist"

print(get_key(100)) 
print(get_key(11)) 


output_list = []

def get_a_free_register(inside):
    for regs in registers:
        if(registers[regs] == ""):
            registers[regs] = inside
            return regs
#do be completed later

temp_res = {}
data = []


def get_reg(arg):
    if(arg[0] == "T"):
        variable = temp_res[arg]
    elif(arg.isdigit()):
        if(arg not in registers.values()):
            reg = get_a_free_register(arg)
            output_list.append(["mov "+reg+","+str(hex(int(arg)))])
            variable = reg
        else:
            variable = get_key(arg)
    else:
        if(arg not in data):
            data.append(arg)
        if(arg not in registers.values()):
            reg = get_a_free_register(arg)
            output_list.append("ldr "+reg+","+"="+arg)
            output_list.append("ldr "+reg+","+"["+reg+"]")
            variable = reg
        else:
            reg = get_key(arg)
            output_list.append("ldr "+reg+","+"["+reg+"]")
            variable = reg
    return variable


filename = sys.argv[1]
f = open(filename,"r")
fileContent = f.read()
rows = fileContent.split("\n")
for row in rows:
    list_quad = row.split(" ")
    # list_quad = 0 operand 1 arg1 2 arg2 3 result
    #print(list_quad)
    if(list_quad[0] == "="):
        variable = get_reg(list_quad[1])

        if(list_quad[3] not in data):
            data.append(list_quad[3])
        if(list_quad[3] not in registers.values()):
            reg = get_a_free_register((list_quad[3]))
            output_list.append("ldr "+reg+","+"="+list_quad[3])
            output_list.append("ldr "+variable+","+"["+reg+"]")
        else:
            reg = get_key(list_quad[3])
            output_list.append("ldr "+variable+","+"["+reg+"]")

    if(list_quad[0] == "+" or list_quad[0] == "-" or list_quad[0] == "*"):
        variable1 = get_reg(list_quad[1])
        variable2 = get_reg(list_quad[2])
        # if(list_quad[3][0] == "T"):
        reg = get_reg(list_quad[3])
        if(list_quad[0] == "+"):
            output_list.append("add "+reg+","+variable1+","+variable2)
        elif(list_quad[0] == "-"):
            output_list.append("sub "+reg+","+variable1+","+variable2)
        elif(list_quad[0] == "*"):
            output_list.append("mul "+reg+","+variable1+","+variable2)
        temp_res[list_quad[3]] = reg

    if(list_quad[0] == "/"):
        flag_div = 1

    

print(output_list)