import pandas as pd
import csv
import random
import copy
import os
import math #for calculating the max number of group combinations 

# path to the CSV files with participant data
participants_csv = "Coffee Partner Lottery participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

# path to TXT file that stores the pairings of this round
new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"


#######################  Conversation Starters Section  ###########################

# # read conversation starters CSV file
# conv_starters=pd.read_csv("Conversation Starters.csv")

# # path to stored conversation starters
# stored_starters = "Stored Starters.csv"
# #create list from stored starters
# stored_starters_list = pd.read_csv(stored_starters)["used starters"].tolist()

# #function selection of new conversation starter        
# def conv_starters_selection():
#   while True:
#     random_index = random.randint(0, len(conv_starters) - 1)
#     random_starter = conv_starters.iloc[random_index]
#     # Check if all starters have been used
#     if len(stored_starters_list) == len(conv_starters):
#         stored_starters.clear()
#         break
#     # Check if the selected starter is already in stored_starters
#     if random_starter.values[0] not in stored_starters_list:
#         # Add the selected starter to stored_starters
#         stored_starters_list.append(random_starter.values[0])
#         #list stored to the CSV file again
#         pd.DataFrame({"used starters": stored_starters_list}).to_csv(stored_starters, header=True, index=False)
#         break  # Exit the loop if a unique starter is found
#   return random_starter

# # find conversation starter
# con_starter = conv_starters_selection()
# print(con_starter)


# init set of old pairs
opairs = set()

DELIMITER=','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_pairs_csv):
    with open(all_pairs_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            opairs.add(tuple(group))




### CODE ANNA

#import packages
# import random

# print("Welcome to the group randomizer! All people that signed up via the online form will be assigned to different groups of a random size. ")


# participants_list = ["Anna", "Joren", "Maud", "Merel", "Sofia", "Berend", "Willem", "Jelmer", "Pieter", "Emma", "Jorien"]


# #calculate amount of participants based on the length of the participants lists from the form
# amount_of_participants = len(participants_list)

# #create random number of groups
# number_of_groups = random.randint(1, amount_of_participants//2)


# #create function that assigns people from list into random pairs or groups
# def random_pairing(participants, number_of_groups):
    
#     #shuffle participants in list
#     random.shuffle(participants)
    
#     #make random groups from shuffled participants 
#    assigned_groups = []                                #list of groups
#     for index in range(number_of_groups):                                             #COPIED THIS FROM INTERNET, DOES IT WORK? CAN WE MAKE IT BETTER?
#         group = participants[index::number_of_groups]
#         assigned_groups.append(group)                   #change assigned_groups variable with new made group
    
#     display groups
#     for index, group in enumerate(assigned_groups):                            #COPIED THIS FROM INTERNET, DOES IT WORK? CAN WE MAKE IT BETTER?
#         print(f"Group {index + 1}: {', '.join(group)}")
        

# randomly assign the participants to groups with an indicated groupsize
# random_pairing(participants_list, number_of_groups)
    

# ###



# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

 # init set of new pairs
npairs = set()

# running set of participants
nparticipants = copy.deepcopy(participants)

# Boolean flag to check if new pairing has been found
new_pairs_found = False

# try creating new pairing until successful
while not new_pairs_found:   # to do: add a maximum number of tries
  
    # if odd number of participants, create one triple, then pairs
    if len(participants)%2 != 0:
        
        # take three random participants from list of participants
        p1 = random.choice(nparticipants)
        nparticipants.remove(p1)
    
        p2 = random.choice(nparticipants)
        nparticipants.remove(p2)
        
        p3 = random.choice(nparticipants)
        nparticipants.remove(p3)
        
        # create alphabetically sorted list of participants
        plist = [p1, p2, p3]
        plist.sort()
                        
        # add alphabetically sorted list to set of pairs
        npairs.add(tuple(plist))

  
    # while still participants left to pair...
    while len(nparticipants) > 0:

        # take two random participants from list of participants
        p1 = random.choice(nparticipants)
        nparticipants.remove(p1)
    
        p2 = random.choice(nparticipants)
        nparticipants.remove(p2)
                
        # create alphabetically sorted list of participants
        plist = [p1, p2]
        plist.sort()
                        
        # add alphabetically sorted list to set of pairs
        npairs.add(tuple(plist))

 
    # check if all new pairs are indeed new, else reset
    if npairs.isdisjoint(opairs):
        new_pairs_found = True
    else:
        npairs = set()
        nparticipants = copy.deepcopy(participants)


# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

for pair in npairs:
    pair = list(pair)
    output_string += "* "
    for i in range(0,len(pair)):
        name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
        if i < len(pair)-1:
            output_string += name_email_pair + ", "
        else:
            output_string += name_email_pair + "\n"
    
# write output to console
print(output_string)

# write output into text file for later use
with open(new_pairs_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new pairs into CSV file (for e.g. use in MailMerge)
with open(new_pairs_csv, "w") as file:
    header = ["name1", "email1", "name2", "email2", "name3", "email3"]
    file.write(DELIMITER.join(header) + "\n")
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
            if i < len(pair)-1:
                file.write(name_email_pair + DELIMITER + " ")
            else:
                file.write(name_email_pair + "\n")
                
# append pairs to history file
if os.path.exists(all_pairs_csv):
    mode = "a"
else:
    mode = "w"

with open(all_pairs_csv, mode) as file:
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            if i < len(pair)-1:
                file.write(pair[i] + DELIMITER)
            else:
                file.write(pair[i] + "\n")


             
# print finishing message
print()
print("Job done.")
