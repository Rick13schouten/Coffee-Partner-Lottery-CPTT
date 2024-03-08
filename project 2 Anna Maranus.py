# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 11:31:08 2024

@author: annam
"""

#%%
#1. The program reads the list of participants from an online form (you can create one with Google Forms or MS Forms, for example), either 
#directly or via a downloaded (.csv) file of responses. The form asks for name and e-mail address. If you like, you can include additional fields.

#2. The set of signed-up participants can change in every round. Therefore the list of participants is read from the source again every time.

#%%
#3. The assignment of people into pairs or groups is random.

#4. The group size is configurable. The program is not only able to generate pairs, but also groups of 3, 4, 5, … people. You may set an upper limit.

#5. If the number of participants is not a multiple of the group size, the program distributes some participants differently (for example 
#by making some groups smaller or larger). It does not happen that a participant is not matched with anyone.



print("Welcome to the group randomizer! All people that signed up via the online form will be assigned to different groups. ")

#ask for what group size the user wants the groups to be with a maximum of 6 group members.
groupsize = int(input("What groupsize do you want the groups to be (minimun groupsize = 2 and maximum groupsize = 6)? "))

#if indicated groupsize is greater than 6 or less than 2, the question will be asked again to assign a groupsize between 2 and 6 using a while-loop
while groupsize <= 1 or groupsize >= 7:
    print("Please enter a groupsize between 2 and 6 people. ")
    groupsize = int(input("What groupsize do you want the groups to be? "))
    
print(f"Okay! The group randomizer will make groups with a groupsize of {groupsize}.")




#randomize participants into groups
import random

#create function that assigns people from list into random pairs or groups
def random_pairing(participants, groupsize):
    
    #shuffle participants in list
    random.shuffle(participants)
    
    #make random groups from shuffled participants 
    assigned_groups = []                                #list of groups
    for index in range(groupsize):                                             #COPIED THIS FROM INTERNET, DOES IT WORK? CAN WE MAKE IT BETTER?
        group = participants[index::groupsize]
        assigned_groups.appand(group)                   #change assigned_groups variable with new made group
    
    #display groups
    for index, group in enumerate(assigned_groups):                            #COPIED THIS FROM INTERNET, DOES IT WORK? CAN WE MAKE IT BETTER?
        print(f"Group {index+1} : {' / '.join(group)}")
        

#randomly assign the participants to groups with an indicated groupsize
random_pairing(participants, groupsize)
    































