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

filename = sys.argv[1]
f = open(filename,"r")
fileContent = f.read()
rows = fileContent.split("\n")
for row in rows:
    list_quad = row.split(" ")
    # list_quad = 0 operand 1 arg1 2 arg2 3 result
    #print(list_quad)
    if(list_quad[0] == "="):
        if(list_quad[1][0] == "T"):
            variable = temp_res[list_quad[1]]
        elif(list_quad[1].isdigit()):
            if(list_quad[1] not in registers.values()):
                reg = get_a_free_register(list_quad[1])
                output_list.append(["mov "+reg+","+str(hex(int(list_quad[1])))])
                variable = reg
            else:
                variable = get_key(list_quad[1])
        else:
            if(list_quad[1] not in data):
                data.append(list_quad[1])
            reg = get_a_free_register(list_quad[1])
            output_list.append("ldr "+reg+","+"="+list_quad[1])
            output_list.append("ldr "+reg+","+"["+reg+"]")
            variable = reg
        if(list_quad[3] not in data):
            data.append(list_quad[3])
        if(list_quad[3] not in registers.values()):
            reg = get_a_free_register((list_quad[3]))
            output_list.append("ldr "+reg+","+"="+list_quad[3])
            output_list.append("ldr "+variable+","+"["+reg+"]")
        else:
            reg = get_key(list_quad[3])
            output_list.append("ldr "+variable+","+"["+reg+"]")


print(output_list)