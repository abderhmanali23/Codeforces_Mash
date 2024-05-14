import sys
sys.stdin = open("input.txt","r")
sys.stdout = open("output.txt","w",encoding='utf-8')
sys.stderr = open("error.txt","w")
enter = sys.stdin.readlines()    

# some declaration ----------------------------------------------------------------------------------------------------
problems_counter = 0
page = 0
result = []
final = []
URL = ""
now = ""
visited = set()
rate_index = 0

# check the input validity --------------------------------------------------------------------------------------------

try:
    problems_counter = int(enter[0][:-1])
    tg = enter[2].rstrip('\n').split(',')
    tags = ""
    for tag in range(len(tg)):
        tags += tg[tag].strip(' ')
        if tag < len(tg)-1:
            tags += ','
    tags = tags.replace(' ','%20') 
    self_handle , password = enter[3].split()
    contest_name , duration = enter[4].split()
    handles = enter[5:]                                                            
    input_rate = enter[1][:-1].split()                                             # the input is like this 800:2 1000:4 ..
    rate_with_count = {}
    
    for i in input_rate:
        rate_with_count[int(i.split(':')[0])] = int(i.split(':')[-1])
        
    rate = list(rate_with_count.keys())
    
except:
    print("Read README.md file to know input format")
    quit()