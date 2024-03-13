## project2-group17

#Anna Maranus 
#Aristotelis Bilinis-Moraitis 
#Sebastian Haile 
#Rick Shouten 

############ Import Libraries Section ###############
import pandas as pd
import csv
import random
import os
import math #for calculating the max number of group combinations 


###################  Load Files Section (requirments 1,2) ###############

# Load participants data from the Google Sheets source using pandas data frame like in a local csv 
sheet_id = '15TfODshWl52QMxSAyVwrKHTpAI36YOj65qat1JohvAk'
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Extract the first column as the list of participants
participants_list = df.iloc[:, 0].tolist()

# header names in the CSV file (name and e-mail of participants)
header_name = "Name"
header_email = "E-mail adress"

# path to TXT file that stores the pairings of this round
new_groups_txt = "Coffee Partner Lottery new groups.txt"

# path to CSV file that stores the groups of this round
new_groups_csv = "Coffee Partner Lottery new groups.csv"

# path to CSV file that stores all gropus (to avoid repetition)
all_groups_csv = "Coffee Partner Lottery all groups.csv"


############################## Group selection (requirements 3,4,5,6) ##########################

# initial set of old groups 
ogroups = set()

DELIMITER=',' #to read the csv file 

# load all previous groups (to avoid redundancies)
if os.path.exists(all_groups_csv):              #checks if csv file exists in the system
    with open(all_groups_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)     #splits values of the csv file
        for row in csvreader:                     #loop that gives every different row as a list
            group = []                            #initialize the name list
            for i in range(0,len(row)):
                group.append(row[i])             #adds to group from the row taken from the csv file             
            ogroups.add(tuple(group))            #makes group to tuple and adds it to old groups set


# Calculate the number of participants
num_participants = len(participants_list)

# Randomly determine the number of groups (could be from 1 group with all participants to pairs)
num_groups = random.randint(1, num_participants // 2)

# Shuffle the list of participants
random.shuffle(participants_list)

#function to generate max possible combinations of groups according to the participants number
def total_combinations(N):
    total = 0
    for k in range(2, N + 1):
        total += math.comb(N, k)   # sum of combinations  of N objects taken k at a time 
    return total

# Initialize a set to store the new groups
new_groups = set()

# Tries to generate new groups
tries=0            #initialize number of tries to find new groups
tries_limit= total_combinations(num_participants)    #limit of tries before decide all groups have been created

# Assign people from the list into random pairs or groups
while True:
    new_groups.clear()     # Clear the new_groups set
    
    # Make random groups from shuffled participants
    for index in range(num_groups):     
        group = participants_list[index::num_groups] #every time starts from index and jumps to every element that is munber of groups far on the list 
        new_groups.add(tuple(group))          #every group formed converted to tuple and added to new groups set

    # Check if all new groups are indeed new, else reset
    new_groups_found = True
    for new_group in new_groups:
      if new_group in ogroups:
        new_groups_found = False 
        break                   #stops for loop if an old group is repeated
    if new_groups_found:
      break                     #if new groups are still true then while loop stops
    else:                       #if no new groups then we try again 
      tries+=1              
      if tries>=tries_limit:    # if the tries are most than the max then all possible groups have been formed
          ogroups.clear()       # since all groups formed we clear the old groups set
          print("No new groups found. Some participants may have been assigned to the same groups in the past")
          open(all_groups_csv, 'w').close()   # Aslo clear the contents of the all_groups_csv file
          break
      random.shuffle(participants_list)    # we suffle again the list of participants to find new groups

# Display groups after they are formed
for index, group in enumerate(new_groups):
   print(f"Group {index + 1}: {', '.join(group)}")
   
# add groups to history file
if os.path.exists(all_groups_csv):   #check if file exists to write it if not 
    mode = "a"
else:
    mode = "w"
with open(all_groups_csv, mode) as file:
    for group in new_groups:
        group = list(group)    #convert group to list
        for i in range(0,len(group)):
            if i < len(group)-1:
                file.write(group[i] + DELIMITER) #delimeter added after every element of the csv file
            else:
                file.write(group[i] + "\n")     #if its the last element it changes lines so next group will be in another one.
                



#######################  Conversation Starters Section (requirement 7)  ###########################

# # read conversation starters CSV file
conv_starters=pd.read_csv("Conversation Starters.csv")

# path to stored conversation starters
stored_starters = "Stored Starters.csv"
#create list from stored starters
stored_starters_list = pd.read_csv(stored_starters)["used starters"].tolist()
header_starters="used starters"

#function selection of new conversation starter        
def conv_starters_selection():
  while True:   #loop won't stop until new starter is found or all starters have been used already
    random_index = random.randint(0, len(conv_starters) - 1)
    random_starter = conv_starters.iloc[random_index]
    # Check if all starters have been used
    if len(stored_starters_list) == len(conv_starters):
        # Open the CSV file in write mode to clear its contents
        with open(stored_starters, 'w') as file:
              file.write(header_starters)    #just rewrite used starters which is the header and clears everything else  
        break
    # Check if the selected starter is already in stored_starters
    if random_starter.values[0] not in stored_starters_list:
        # Add the selected starter to stored_starters
        stored_starters_list.append(random_starter.values[0])
        #list stored to the CSV file again
        pd.DataFrame({"used starters": stored_starters_list}).to_csv(stored_starters, header=True, index=False)
        break        # exit the loop if a new starter is found
  return random_starter

# find conversation starter
con_starter = conv_starters_selection()
print(con_starter)


#########################  Generate messages to groups (requirement 8) ############################# 
# load participant's data
individual_message_txt = "Individual Messages.txt"

# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

g=1
for group in new_groups:
    output_string += f"GROUP {g}:  "  #gives groups number
    for name in group:
        # Find the corresponding email address in formdata based on the name
        email = df.loc[df[header_name] == name, header_email].iloc[0]
        # Append name and email pair to the output string
        output_string += f"{name} ({email})"
        # Add comma if it's not the last member of the group
        if name != group[-1]:
            output_string += ", "
    g+=1
    output_string += "\n \n"
# write output to console
print(output_string)

# write output into text file for later use
with open(new_groups_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

file.close()

# peronalized messages for each group member printed in a new file
with open(individual_message_txt, "w") as file:
    for group in new_groups:
        for member in group:
            matching_rows = df[df[header_name] == member]
            if not matching_rows.empty:
                n_email = matching_rows.iloc[0][header_email]
                name = matching_rows.iloc[0][header_name]
            else:
                print(f"No matching email found for {member}")
                continue

            message = f'''
Dear {name},

You signed up for the Coffee Pairing this week! Great!

Your group for this week is: 
    {', '.join(group)}

The conversation starter this week is: 
    {con_starter}

Have fun on your coffee date!
\n \n \n'''
            file.write(message)

         
# print finishing message
print()
print("Job done.")