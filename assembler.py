path = input('Enter filename: ')
import re

# path = 'rect/Rect.asm'          #load file
f = open(path, 'rt').read()

#Source Tables
srcTbl = {'R0':'0','R1':'1','R2':'2','R3':'3','R4':'4','R5':'5','R6':'6','R7':'7','R8':'8','R9':'9','R10':'10','R11':'11','R12':'12','R13':'13','R14':'14','R15':'15','SCREEN':'16384','KBD':'24576','SP':'0','LCL':'1','ARG':'2','THIS':'3','THAT':'4'}
dest = {'null':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
jump = {'null':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
control = {'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}

def splitInstruction(p):
    p = p.split('=')
    if(len(p) == 1):
        p.insert(0,'null')
    p[1] = p[1].split(';')
    if(len(p[1]) == 1):
        p[1].insert(1,'null')
    return [p[0],p[1][0],p[1][1]];

def instBin(ins):
    abit = str(int('M' in ins[1]))
    ins[1] = ins[1].replace('M', 'A')
    return ''.join(['111',abit,control[ins[1]],dest[ins[0]],jump[ins[2]]])

x = re.sub("//.*", "", f).strip()               #regex to remove comments and whitespace charecters
x = re.sub("\s+", "\n", x).split('\n')          #to clean the input and convert string to list

count = 0
for line in x:
    if(line.startswith('(')):                   #scan file for (****) blocks and
        srcTbl[line[1:-1]] = str(count)         #add addresses to the source table
    else:
        count = count + 1

x = '\n'.join(x)                                #convert list to string

x = re.sub("^\(.*", ' ', x, 0, re.MULTILINE).strip()        #removing (****) blocks
x = re.sub("\s+", "\n", x)                                  #cleaning
pattern = re.compile("|".join([re.escape(k) for k in sorted(srcTbl,key=len,reverse=True)]), flags=re.DOTALL)
x = pattern.sub(lambda p: srcTbl[p.group(0)], x)            #replace addresses from source table

v = re.finditer("@\D.*", x)                     #get all the variables
count = {'':''}                                      #dict for storing variables, value paires
i = 16
for a in v:
    try:
        temp = count[a.group(0)]
    except KeyError:
        count[a.group(0)] = '@'+str(i)
        i = i + 1
pattern = re.compile("|".join([re.escape(k) for k in sorted(count,key=len,reverse=True)]), flags=re.DOTALL)
x = pattern.sub(lambda p: count[p.group(0)], x).splitlines()    #replaced variables with pointer addresses

#----------------------------------------Symbol-less code acquired-----------------------------------------#

#--------------------------------------assembler starts here--------------------------------------#

op = [None] * len(x)            #create empty list for output

for i in range(len(x)):
    ins = bin(0)[2:].zfill(16)
    if(x[i].startswith('@')):   #check wether OP Code or Instruction
        op[i] = bin(int(x[i][1:]))[2:].zfill(16)
    else:
        op[i] = splitInstruction(x[i])          #split instruction into parts
        op[i] = instBin(op[i])        #convert to binary

path = input('Enter name for output file: ') + '.hack'
f = open(path, "w")
f.write('\n'.join(op))
f.close()

#open and read the file after the appending
f = open(path, "r")
print(f.read())
