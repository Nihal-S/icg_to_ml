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

# print(get_key(100))
#  
# print(get_key(11)) 


output_list = []

list_of_args = []
filename = sys.argv[1]
f = open(filename,"r")
fileContent = f.read()
rows = fileContent.split("\n")
for row in rows:
    list_of_args.append(row.split(" ")[1:-1])


def get_a_free_register(inside):
    for regs in registers:
        if("" in registers.values()):
            if(registers[regs] == ""):
                registers[regs] = inside
                return regs
    list_of_regs_values = registers.values()
    for i in list_of_regs_values:
        if i not in list_of_args:
            reg = get_key(i)
            registers[reg] = ""
    if ("" in registers.values()):
        return get_a_free_register(inside)
    else:
        for i in reversed(list_of_args):
            if i in list_of_regs_values:
                reg = get_key(i)
                registers[reg] = ""
                return get_a_free_register(inside)

#do be completed later

temp_res = {}
data = []


def get_reg(arg):
    if(arg[0] == "T"):
        variable = temp_res[arg]
    elif(arg.isdigit()):
        if(arg not in registers.values()):
            reg = get_a_free_register(arg)
            output_list.append("mov "+reg+","+str(hex(int(arg))))
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
    # print(list_quad)
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

    elif(list_quad[0] == "+" or list_quad[0] == "-" or list_quad[0] == "*" or list_quad[0] == "/"):
        variable1 = get_reg(list_quad[1])
        variable2 = get_reg(list_quad[2])
        # if(list_quad[3][0] == "T"):
        # reg = get_reg(list_quad[3])
        reg = get_a_free_register(list_quad[3])
        if(list_quad[0] == "+"):
            output_list.append("add "+reg+","+variable1+","+variable2)
        elif(list_quad[0] == "-"):
            output_list.append("sub "+reg+","+variable1+","+variable2)
        elif(list_quad[0] == "*"):
            output_list.append("mul "+reg+","+variable1+","+variable2)
        elif(list_quad[0] == "/"):
            # print(reg)
            # print(variable1)
            # print(variable2)
            output_list.append("div "+reg+","+variable1+","+variable2)
        temp_res[list_quad[3]] = reg

    elif(list_quad[0] =="goto" or list_quad[0] == "Label"):
        if(list_quad[0] == "goto"):
            output_list.append("b "+list_quad[3])
        else:
            output_list.append(list_quad[3]+":")

    elif(list_quad[0] == "if"):
        output_list.append("b"+temp_res[list_quad[1]]+","+list_quad[3])

    elif(list_quad[0] == "==" or list_quad[0] == ">" or list_quad[0] == "<" or list_quad[0] == "<=" or list_quad[0] == ">=" or list_quad[0] == "!="):
        variable1 = get_reg(list_quad[1])
        variable2 = get_reg(list_quad[1])
        output_list.append("cmp "+variable1+","+variable2)
        if(list_quad[0] == "<"):
            temp_res[list_quad[3]] = "lt"
        elif(list_quad[0] == ">"):
            temp_res[list_quad[3]] = "gt"
        elif(list_quad[0] == ">="):
            temp_res[list_quad[3]] = "ge"
        elif(list_quad[0] == "<="):
            temp_res[list_quad[3]] = "le"
        elif(list_quad[0] == "=="):
            temp_res[list_quad[3]] = "eq"
        else:
            temp_res[list_quad[3]] = "ne"

    elif(list_quad[0] == "not"):
        if temp_res[list_quad[1]] == "lt":
            temp_res[list_quad[3]] = "ge"
        elif temp_res[list_quad[1]] == "gt":
            temp_res[list_quad[3]] = "le"
        elif temp_res[list_quad[1]] == "ge":
            temp_res[list_quad[3]] = "lt"
        elif temp_res[list_quad[1]] == "le":
            temp_res[list_quad[3]] = "gt"
        elif temp_res[list_quad[1]] == "eq":
            temp_res[list_quad[3]] = "ne"
        else:
            temp_res[list_quad[3]] = "eq"
    list_of_args = list_of_args[2:]
print(".data")
for i in data:
    print("\t"+i[0]+":",".word",hex(0),sep=' ')

print(".text")
for i in output_list:
    print("\t"+i)
    
print("end:")
print("\t","swi","0x011")
f.close()
# print(output_list)