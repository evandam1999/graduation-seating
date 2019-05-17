# Graduation seating
import os

#Read text file with names
ins = open( "FullList.txt", "r" )
kids = []
for line in ins:
    kid = line.strip('"\n')
    if kid is not '':
        kids.append( kid )
ins.close()
print "Total Kids = " + str(len(kids))

#Read in the file with the Smart kids
ins = open("Top_20.txt", "r")
SKids = []
for line in ins:
    kid = line.strip('"\n')
    if kid is not '':
        SKids.append( kid )
ins.close()

#No more val and sal, they are automatically at the top
#of the top 20(previously the smart list)
#in the smart list is a val(^) and a sal($)
##Val = ''
##for k in SKids:    
##    if k[0] == '^':
##        Val = k.lstrip('^')
##        SKids.remove(k)
##        kids.remove(Val)
##print '\tVal is ' + str(Val)
##
##Sal = ''        
##for k in SKids:    
##    if k[0] == '$':
##        Sal = k.lstrip('$')
##        SKids.remove(k)
##        kids.remove(Sal)
##print '\tSal is ' + str(Sal)

#Find handicap kids
HKids = []
for k in kids:
    if k[0] == '*':
        hk = k.lstrip('*')
        HKids.append(hk)
        index = kids.index(k)
        kids.insert(index, hk)
        kids.remove(k)

#Remove kids in the smart list that are not in the full list, they are not walking
for sk in SKids:
    if kids.count(sk) == 0:
        print "\t** " + str(sk) + " is not in the FullList, removing from SmartList"
        SKids.remove(sk)        
    elif kids.count(sk) > 1:
        print "\t** " + str(sk) + " is in the full list multiple times"

#Go over full list and remove smart kids, they will sit up front.
for sk in SKids:
    if kids.count(sk) == 1:
        kids.remove(sk)
    elif kids.count(sk) == 0:
        print "\t****" + str(sk) + " Error1"
    elif kids.count(sk) > 1:
        print "\t****" + str(sk) + " Error2"

kids = sorted(kids)
#don't sort cause this is now a top 20 and they are already in
#order and don't need to be alphabetized.
##SKids = sorted(SKids)
HKids = sorted(HKids)

#go in and find kids that have suffix Jr, II or III, etc.  this is after the 2nd comma in the names list.  
print 'FIXING SUFFIX KIDS'
for k in kids:
    idx = k.find(',',k.find(',')+1)
    if (idx != -1):
        oldname = k
        suffix = k[idx:].strip(',').strip(' ')
        k = k[:idx]
        # now that we have already sorted, lets put the suffix at the end of the last name.
        k = k[:k.find(',')] + ' ' + suffix + k[k.find(','):]
        print '\t' + oldname + ' is now ' + k
        currentIndex = kids.index(oldname)
        kids.remove(oldname)
        kids.insert(currentIndex, k)


SeatsPerRow = 10 #Harcoded for now.
SeatsPerFullRow = SeatsPerRow*2
#Sections = 4 #Hardcoded to 4 for now.

OS = []
LineupA = []
LineupB = []
LineupS = []

##OS.append(Val)
##OS.append(Sal)
for k in SKids:
    OS.append(k)
for k in kids:
    OS.append(k)

#now lets find the handicap kids and move them to the begining of their row
print 'MOVING HANDICAP KIDS'
for hk in HKids:
    index = OS.index(hk)
    OS.remove(hk)
    newIndex = index - (index%(SeatsPerFullRow))
    OS.insert(newIndex, hk)
    print '\t' + str(hk) + ' moved from ' +str(index) + ' to ' + str(newIndex) + ' (Handicap)'

print 'Kids Seated = ' + str(len(OS))

if not os.path.exists('Output'):
    os.makedirs('Output')
    
seat = 0;
sA = open('./Output/SectionA.txt', "w")
sB = open('./Output/SectionB.txt', "w")

last_index = 0;
for idx, name in enumerate(OS):
      
    sec = (int(idx/SeatsPerRow) + 1)%2;
    row = int(idx/SeatsPerFullRow) + 1;
    seat = (idx)%SeatsPerRow + 1;
    
    
    
    if sec == 1: #section A
        sA.write('A  Row {:3d} Seat {:3d} - {:s}\n'.format(row, seat, name))
        
        #the val and sal are not in the lineup
        #if row == 1 and (seat == 1 or seat == 2):
        if row == 1:
            if not(seat == 1 or seat == 2):
                LineupS.append(name)
        else:      
            LineupA.append(name)
    else: #section B        
        sB.write('B  Row {:3d} Seat {:3d} - {:s}\n'.format(row, seat, name))
        
        if row == 1:
            LineupS.append(name)
        else:
            LineupB.append(name)    
        # row 1 seat 9 needs to be 1st in the Lineup A to fix the issue where the val and sal do not line up.
        #if row == 1 and seat == 9:
        #    LineupA.insert(0, name)            
        #    LineupB.append('') 
        #    continue
        
        #LineupB.append(name)
        
    #print name + ' sec ' + section + ' row ' + str(row) + ' seat ' + str(seat)
sA.close()
sB.close()

lA = open('./Output/LineupA.txt', "w")
lB = open('./Output/LineupB.txt', "w")
lS = open('./Output/LineupS.txt', "w")

for idx, name in enumerate(LineupA):
    lA.write('{:3d} {:s}\n'.format(idx+1, name))

#since the lineup list for this side is reversed by row, we must
#reverse every row (set of SeatsPerRow)
startRev = 0
endRev = SeatsPerRow
while endRev < len(LineupB):
    LineupB[startRev:endRev] = reversed(LineupB[startRev:endRev])
    startRev += SeatsPerRow
    endRev += SeatsPerRow

startRev = endRev-SeatsPerRow
endRev = len(LineupB)
LineupB[startRev:endRev] = reversed(LineupB[startRev:endRev])
    
for idx, name in enumerate(LineupB):    
    lB.write('{:3d} {:s}\n'.format(idx+1, name))    
    
for idx, name in enumerate(LineupS):    
    lS.write('{:3d} {:s}\n'.format(idx+1, name))  
    
lA.close()
lB.close()
lS.close()


# Print out full list of names.
s1 = open('./Output/FullListDebug.txt', "w")
s2 = open('./Output/CallOutList.txt', "w")

for k in OS:
    s1.write(k)
    s1.write('\n')


#Swap first and last names
for i in range(len(OS)):
    k = OS[i]
    #print k
    name = k[k.find(',')+1:] + ' ' + k[:k.find(',')]
    name = name.rstrip(',')
    #print name
    OS[i] = name

#alternating names callout
##for i in xrange(0,len(OS),2):
##    if i+1 < len(OS):
##        if len(OS) - i+1 >=2:
##            s2.write('{:s}\n {:>70s}\n'.format(str(OS[i]) ,str(OS[i+1])))
##        elif len(OS) - i+1 == 1:
##            s2.write(OS[i])

#two col with spaces
##for i in xrange(0,len(OS),2):
##    if i+1 < len(OS):
##        if len(OS) - i+1 >=2:
##            s2.write('{:s} {:>70s}\n\n\n'.format(str(OS[i]) ,str(OS[i+1])))
##        elif len(OS) - i+1 == 1:
##            s2.write(OS[i])

for i in xrange(0,len(OS),2):
    if i+1 < len(OS):
        if len(OS) - i+1 >=2:
            s2.write('{:s}\n {:>70s}\n\n\n'.format(str(OS[i]) ,str(OS[i+1])))
        elif len(OS) - i+1 == 1:
            s2.write(OS[i])



s1.close()
s2.close()

print HKids
