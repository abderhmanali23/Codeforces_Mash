# Make Codeforces mash
<b>Description:</b><br>
This Python script retrieves the names of solved problems for given handles.It returns the problem set for all handles except the one currently logged in.<br> 
For the logged-in handle, it includes all solved problems, including any mash problems.<br>
Return unsolved problems from the problem set with given tags and rates.<br>
Then it make a mash on the logged in handle with given name and duration.<br>
<br>
<b>Required libraries:</b><br>
1- bs4<br>
2- html5lib<br>
3- requests<br>
4- json<br>
<br>
<b>Instructions for how to enter data in input.txt file:</b><br>
1- The first line should contain the desired number of problems on the mash.<br>  
2- The second line should contain the rate of problems and number of each separated by ":"<br>
3- The third line should contain tags of problems separated by "," .. OR "No tags" in case there are no specific tags<br>
4- The fourth one should contain login information : Username and Password separated by space.<br> 
5- The fifth should contain mash information : Name and duration in minuts separated by space.<br>
6- For any number of lines, input handles one handle per line.<br>
<br>
<br>Example:</b><br>
10<br>
800:2 1000:3 1100:4 1200:1<br>
data structure , math , greedy<br>
yasmien 123456789<br>
test 300<br>
mohamed<br>
ahmed<br>
sayed<br>
ebraheem<br> 
<br>
<b>Its excpected that problems name and rate exist on output.txt file, <br>
mash with the given name on gym mashups page on codeforces, <br>
any error exist on error.txt </b><br>

