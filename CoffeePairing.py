## project2-group17


############ imports section ###############
import pandas as pd
import csv
import random
import copy
import os
import math #for calculating the max number of group combinations 


###################  Load Files Section (requirments 1,2) ###############
# path to the CSV files with participant data
participants_csv = "Coffee Partner Lottery participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

# path to TXT file that stores the pairings of this round
new_groups_txt = "Coffee Partner Lottery new groups.txt"

# path to CSV file that stores the groups of this round
new_groups_csv = "Coffee Partner Lottery new groups.csv"

# path to CSV file that stores all gropus (to avoid repetition)
all_groups_csv = "Coffee Partner Lottery all groups.csv"


############################## Group selection (requirements 3,4,5,6) ##########################

# initial set of old groups 
ogroups = set()

DELIMITER=','

# load all previous groups (to avoid redundancies)
if os.path.exists(all_groups_csv):
    with open(all_groups_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            ogroups.add(tuple(group))

#create a participants list from the csv file
participants_list = pd.read_csv(participants_csv)["Your name:"].tolist()

# Calculate the number of participants
num_participants = len(participants_list)

# Randomly determine the number of groups
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
    # Clear the new_groups set
    new_groups.clear()
    
    # Make random groups from shuffled participants
    for index in range(num_groups):
        group = participants_list[index::num_groups]
        new_groups.add(tuple(group))

    # Check if all new groups are indeed new, else reset
    new_groups_found = True
    for new_group in new_groups:
      if new_group in ogroups:
        new_groups_found = False
        break
    if new_groups_found:
      break
    else:
      tries+=1
      if tries>=tries_limit:
          ogroups.clear()        
          print("No new groups found. Participants may have been assigned to the same groups")
          open(all_groups_csv, 'w').close()   # Clear the contents of the all_groups_csv file
          break
      random.shuffle(participants_list)

# Display groups
for index, group in enumerate(new_groups):
   print(f"Group {index + 1}: {', '.join(group)}")
   
# append groups to history file
if os.path.exists(all_groups_csv):
    mode = "a"
else:
    mode = "w"

with open(all_groups_csv, mode) as file:
    for group in new_groups:
        group = list(group)
        for i in range(0,len(group)):
            if i < len(group)-1:
                file.write(group[i] + DELIMITER)
            else:
                file.write(group[i] + "\n")



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
  while True:
    random_index = random.randint(0, len(conv_starters) - 1)
    random_starter = conv_starters.iloc[random_index]
    # Check if all starters have been used
    if len(stored_starters_list) == len(conv_starters):
        # Open the CSV file in write mode to clear its contents
        with open(stored_starters, 'w') as file:
              file.write(header_starters)          
        break
    # Check if the selected starter is already in stored_starters
    if random_starter.values[0] not in stored_starters_list:
        # Add the selected starter to stored_starters
        stored_starters_list.append(random_starter.values[0])
        #list stored to the CSV file again
        pd.DataFrame({"used starters": stored_starters_list}).to_csv(stored_starters, header=True, index=False)
        break  # Exit the loop if a unique starter is found
  return random_starter

# find conversation starter
con_starter = conv_starters_selection()
print(con_starter)


#########################  Generate messages to groups (requirement 8) ############################# 
# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)
individual_message_txt = "Individual Messages.txt"

# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

for group in new_groups:
    output_string += "* "
    for name in group:
        # Find the corresponding email address in formdata based on the name
        email = formdata.loc[formdata[header_name] == name, header_email].iloc[0]
        # Append name and email pair to the output string
        output_string += f"{name} ({email})"
        # Add comma if it's not the last member of the group
        if name != group[-1]:
            output_string += ", "
    output_string += "\n"
# write output to console
print(output_string)

# write output into text file for later use
with open(new_groups_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# peronalized messages for each group member printed in a new file
with open(individual_message_txt, "w") as file:
    for group in new_groups:
        group = list(group)
        group_n_email = ''
        for i in range(0,len(group)):
            n_email = f"{formdata[formdata[header_email] == group[i]].iloc[0][header_name]} ({group[i]})"
            if i < len(group)-1:
                group_n_email += n_email + ", "
            else:
                group_n_email += n_email
        
        for i in range(0,len(group)):
            message = f'''
Dear {formdata[formdata[header_email] == group[i]].iloc[0][header_name]},

You signed up for the Coffee Pairing this week! Great!

Your group for this week is: 
    {group_names_emails}

The conversation starter this week is: 
    {con_starter}

Have fun on your coffee date!
\n \n \n'''
            file.write(message)
    
# append groups to history file
if os.path.exists(all_groups_csv):
    mode = "a"
else:
    mode = "w"

with open(all_groups_csv, mode) as file:
    for group in new_groups:
        group = list(group)
        for i in range(0,len(group)):
            if i < len(group)-1:
                file.write(group[i] + DELIMITER)
            else:
                file.write(group[i] + "\n")


             
# print finishing message
print()
print("Job done.")
