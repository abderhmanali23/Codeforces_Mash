import sys
import requests
from bs4 import BeautifulSoup
import json
from input_data import *
from random import shuffle

session = requests.Session() 
#----------------------------------------------------------------------------------------------
sys.stdin = open("input.txt","r")
sys.stdout = open("output.txt","w",encoding='utf-8')
sys.stderr = open("error.txt","w")

#----------------------------------------------------------------------------------------------
def check_login(request):
    soup = BeautifulSoup(request.content, 'html5lib')
    status = soup.find('body').find('div', {'id': 'header'}).find_all('a')[-1].text
    if status == 'Logout':
        return True
    return False


def login(handle, password):
    URL = "https://codeforces.com/enter"
    session.get(URL)
    csrf_token_login = getCsrf(URL)

    # login data

    login_data = {
        'action' : 'enter',
        'handleOrEmail' : handle,
        'password' : password,
        'csrf_token' : csrf_token_login,
        'remember' : 'on'
    }
    headers = {
        'X-Csrf-Token' : csrf_token_login
    }
    request = session.post(URL,data=login_data,headers=headers)
    return check_login(request)

def solved_for_handle(handle):
    # Enter the status page and get it decoded as html and find number of pages of submissions                        
    User_URL = f"https://codeforces.com/submissions/{handle}/page/1"        
    get = session.get(User_URL)                                         
    soup = BeautifulSoup(get.content,'html5lib')                              
    body = soup.find_all('tr')[1:-1]     
    problems = set()
    lastPageIndex = 1
    page = 1
    # Handle no pages case
    try:
        lastPageIndex = soup.find_all('span', {'class':"page-index"})[-1].text
    except:
        problem_details = body[0].find_all('td')
        if len(problem_details) == 1:
            return problems
    
    # Get all accepted problem in all pages
    while page <= int(lastPageIndex):
        for problem in body:
            problem_details = problem.find_all('td')
            problem_truth = problem_details[5].find('span')['submissionverdict']
            if problem_truth == 'OK':
                problem_name = problem_details[3].find('a').text.strip().strip('\n').split('-')
                problem_name = '-'.join(problem_name[1:]).strip()
                problems.add(problem_name)
        page += 1
        User_URL = f"https://codeforces.com/submissions/{handle}/page/{page}"         
        get = session.get(User_URL)                                                      
        soup = BeautifulSoup(get.content,'html5lib')                 
        body = soup.find_all('tr')[1:-1] 
    return problems

# combine all solved problems for each handle in a dictionary
def solved_problems_for_all(handles):                                        
    accepted = frozenset()                                                        
    for handle in handles:
        # for every handle get solved problems
        for_handle = solved_for_handle(handle.strip('\n'))
        accepted = accepted.union(for_handle)
    return accepted

def getCsrf(URL:str):
    auth = session.get(URL).content
    soup = BeautifulSoup(auth, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf

def makeMash(problems:list, mash_name:str, Duration):
    URL = "https://codeforces.com/mashup/new"
    csrf_token_mash = getCsrf(URL)
    index = 0

    # JSON Payload
    js = []
    for problem in problems:
        dataForProblem = {
            'action' : 'problemQuery',
            'problemQuery' : problem,
            'csrf_token' : csrf_token_mash
        }
        # Get information

        result = session.post('https://codeforces.com/data/mashup', data=dataForProblem)
        data = result.json()

        # Make Payload
        place = data['problems'][0]
        dic = {"id": place['id'], "index": chr(ord('A')+index)}
        index += 1
        js.append(dic)

    make_the_mash = json.dumps(js)
    Payload = {
            'action': 'saveMashup',
            'isCloneContest': 'false',
            'parentContestIdAndName': "",
            'parentContestId': "",
            'contestName': mash_name,
            'contestDuration': Duration,
            'problemsJson': make_the_mash,
            'csrf_token': csrf_token_mash,
        }
    session.post('https://codeforces.com/data/mashup', data=Payload) 
    
# main-----------------------------------------------------------------------------------------------------------------
validity = login(self_handle,password)
#  Handle login error

if not validity:
    print('Incorrect Password or Username')
    quit()

accepted = solved_problems_for_all(handles)              # Get all solved problems of all handles    
while problems_counter:
    page += 1            

    # No tags case
                                                                                            
    if tags == 'No tags':
        URL = f"https://codeforces.com/problemset/page/{page}?tags={rate[rate_index]}-{rate[rate_index]}" 
        
    else:
        URL = f"https://codeforces.com/problemset/page/{page}?tags={tags},{rate[rate_index]}-{rate[rate_index]}"

    # check if the current page is the last one

    if now == URL:
        print('There are no more problems')     
        break

    now = URL
    request = session.get(URL)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html5lib')                                      # get problemset html code
        tmp = soup.find_all('tbody')[1]                                                             # go to body section 
        links = tmp.findAll('div',{'style':"float: left;"})                                         # find all <td> that has an class = id (which contains problems links) 
        problems = []
        for link in links:
            index = link.a['href']                                                             # for every problem get it's link https://codeforces.com/problem/...
            name = link.a.text
            index = index.split('/')                                                           # split this link to get contest id and peoblem index
            problems.append((name.strip('\n').strip(' '),index[-2]+index[-1]))

        if not len(problems):
            print('There are no problems with these tags')
            quit()

        for problem,index in problems:                                                                           
            if (problem not in accepted) and (problem not in visited):                             # for every problem check that it isn't solved by any one and not been taken before
                problems_counter -= 1
                visited.add(problem)
                result.append(f"--> Problem: {problem}, with rate: {rate[rate_index]}")        # add the problem whith its rate to output list
                final.append(index)
                break
    
    rate_with_count[rate[rate_index]] -= 1                                                     # decrease the number of wanted problems for this rate
    if rate_with_count[rate[rate_index]] == 0:                                                 # if there are no more wanted problems for this rate go to the next 
        rate_index += 1
        page = 0

shuffle(final)    # To shuffle problems (can be removed if you want problems be ordered with given rate )
print('\n'.join(result))
makeMash(final, contest_name, duration)
