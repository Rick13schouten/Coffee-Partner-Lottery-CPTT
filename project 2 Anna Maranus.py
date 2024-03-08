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

#import packages
import random



print("Welcome to the group randomizer! All people that signed up via the online form will be assigned to different groups of a random size. ")


participants_list = ["Anna", "Joren", "Maud", "Merel", "Sofia", "Berend", "Willem", "Jelmer", "Pieter", "Emma", "Jorien"]


#calculate amount of participants based on the length of the participants lists from the form
amount_of_participants = len(participants_list)

#create random number of groups
number_of_groups = random.randint(1, amount_of_participants//2)


#create function that assigns people from list into random pairs or groups
def random_pairing(participants, number_of_groups):
    
    #shuffle participants in list
    random.shuffle(participants)
    
    #make random groups from shuffled participants 
    assigned_groups = []                                #list of groups
    for index in range(number_of_groups):                                             #COPIED THIS FROM INTERNET, DOES IT WORK? CAN WE MAKE IT BETTER?
        group = participants[index::number_of_groups]
        assigned_groups.append(group)                   #change assigned_groups variable with new made group
    
    #display groups
    for index, group in enumerate(assigned_groups):                            #COPIED THIS FROM INTERNET, DOES IT WORK? CAN WE MAKE IT BETTER?
        print(f"Group {index + 1}: {', '.join(group)}")
        

#randomly assign the participants to groups with an indicated groupsize
random_pairing(participants_list, number_of_groups)
    































