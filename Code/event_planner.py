"""
event_planner.py

Includes the bruteForce, dynamic and greedyHeuristic algorithms along with eventPlanner and printFormat
"""

import time

def bruteForce(file_path):
    """
    Reads the input file and take out the useful data,
    Uses a for loop and format() to iterate through binary numbers representing each combination of events,
    For each combination of events, calculates the total time used, the total budget used and total enjoyment value.
    If the total time and/or total budget are within the decided constraints, and the enjoyment value is larger than 
    the other enjoyment values of legal combinations of events, the current combination is set as the best combination.
    Once all combinations have been iterated through, the best combination is returned.
    
    :param file_path: the file_path to the file containing the activities the society are deciding between
    """
    start = time.time()
    timeout = False

    # opens the file inputed and stores all the necessary infomation in variables
    with open(file_path, "r") as file:
        i = 0
        events = []
        for line in file:
            components = line.split()
            if i==0:
                num_activities = components[0]
            elif i==1:
                available_t = int(components[0])
                available_b = int(components[1])
            else:
                events.append([components[0],int(components[1]),int(components[2]),int(components[3])])
            i += 1

    # uses binary numbers from 0 to 2^(number of events) to iterate through each subset of events
    weekend_schedule = []
    best_ev = 0
    for i in range(2**int(num_activities)):
        t_used = 0
        b_used = 0
        total_ev = 0
        binary = format(i, f'0{num_activities}b')
        events_combination = []
        # computes the sum of: time used, monetary cost, total enjoyment and adds each event in a subset to a list
        for j in range(len(binary)):
            b = binary[j]
            if b == "1":
                t_used += events[j][1]
                b_used += events[j][2]
                total_ev += events[j][3]
                events_combination.append(events[j])
        # if the combination of events is within the constraints, and results in best enjoyment so far, it is set as the best subset of events
        # "if t_used <= available_t and b_used <= available_b and total_ev >= best_ev:" can be used if both time and budget need to be considered
        if t_used <= available_t and total_ev >= best_ev:
            best_ev = total_ev
            best_t = t_used
            best_b = b_used
            weekend_schedule = events_combination
        
        # if time limit is reached, the best subset is returned along with "timeout = True"
        check = time.time()
        if check - start > 600:
            weekend_schedule.sort(key=lambda x: x[0])
            timeout = True
            end = time.time()
            time_taken = end - start 
            return weekend_schedule, available_t, available_b, timeout, best_ev, best_t, best_b, time_taken
    weekend_schedule.sort(key=lambda x: x[0])
    end = time.time()
    time_taken = end - start
    # if time limit is not reached, the best subset is returned and "timeout = False"
    return weekend_schedule, available_t, available_b, timeout, best_ev, best_t, best_b, time_taken


def dynamic(file_path):
    '''
    Docstring for dynamic
    
    :param file_path: the file_path to the file containing the activities the society are deciding between
    '''
    start = time.time()
    timeout = False
    file = open(file_path,"r",encoding="utf-8") 
    content = file.read() 
    contentSplit = content.split("\n") 
    
    #Splits the text file into components
    numberOfEvents = int(contentSplit[0]) 
    timeLimit, budget = (contentSplit[1].split(" "))
    
    #Obtains all the events, then puts in events list variable 
    events = [] 
    for x in range(-numberOfEvents -1 ,-1): 
        events.append(contentSplit[x]) 

    #Sorts attributes out of the activities 
    times = [] 
    ev = [] # enjoyment value 
    for event in events:
        components = event.split()
        t, enjoyment = components[1], components[3] 
        times.append(int(t)) 
        ev.append(int(enjoyment)) 

    timeLimit = int(timeLimit) 

    #Empty space for the algorithm
    totalNumberOfItems = len(times) 
    dp = [[0] * (timeLimit+1) for _ in range(totalNumberOfItems+1)] 

    for x in range(1,totalNumberOfItems+1): 
        for y in range(timeLimit+1): 
            if times[x-1] > y: 
                dp[x][y] = dp[x-1][y] 
            else: 
                # decides the include the activity in the knapsack 
                dp[x][y] = max(dp[x-1][y], ev[x-1] + dp[x-1][y-times[x-1]]) 
    t = timeLimit 
    items = [] 
    for i in range(totalNumberOfItems,0,-1): 
        if dp[i][t] != dp[i-1][t]: #if value has changed the item is included 
            items.append(i-1) # stores that items itotalNumberOfItemsex 
            t -= times[i-1] 
    weekend_schedule  = []
    for i in items:
        weekend_schedule.append(events[i].split())
    weekend_schedule.sort(key=lambda x: x[0])
    best_ev = sum(int(element[3]) for element in weekend_schedule)
    best_t = sum(int(element[1]) for element in weekend_schedule)
    best_b = sum(int(element[2]) for element in weekend_schedule)
    end = time.time()
    time_taken = end-start
    return weekend_schedule, timeout, best_ev, best_t, best_b, time_taken

def greedyHeuristic(file_path):
    '''
    Reads the input file and take out the useful data.
    Sorts the events in descending order, based on the ratio of enjoyment to time.
    Uses a for loop to iterate through each event, in descending order of ratio.
    For each event adds it to the schedule if the time it requires is within the remaining time.
    And finally, returns the schedule.
    
    :param file_path: the file_path to the file containing the activities the society are deciding between
    '''
    start = time.time()
    timeout = False

    # opens the file input and stores all the necessary infomation in variables along with ratio of EV/time
    with open(file_path, "r") as file:
        i = 0
        events = []
        for line in file:
            components = line.split()
            if i==0:
                num_activities = components[0]
            elif i==1:
                available_t = int(components[0])
                available_b = int(components[1])
            else:
                events.append([components[0],int(components[1]),int(components[2]),int(components[3]),int(components[3])/int(components[1])])
            i += 1

    # sorts the events from greatest to lowest ratio EV/time
    events.sort(key=lambda x: x[4], reverse = True)
    weekend_schedule = []
    remaining_t = available_t
    best_ev = 0
    best_t = 0
    best_b = 0

    # go through events in new order and if the time required is less than the remaining, time and budget, then the event is added to the schedule
    for event in events:
        if event[1] <= remaining_t:
            weekend_schedule.append(event)
            remaining_t -= event[1]
            best_ev += event[3]
            best_t += event[1]
            best_b += event[2]

        # if time limit is reached, the best subset is returned along with "timeout = True"
        check = time.time()
        if check - start > 300:
            weekend_schedule.sort(key=lambda x: x[0])
            timeout = True
            end = time.time()
            time_taken = end - start
            return weekend_schedule, timeout, best_ev, best_t, best_b, time_taken
    weekend_schedule.sort(key=lambda x: x[0])
    end = time.time()
    time_taken = end - start
    # if time limit is not reached, the best subset is returned and "timeout = False"
    return weekend_schedule, timeout, best_ev, best_t, best_b, time_taken

def eventPlanner(file_path):
    '''
    Uses print_format() to print the schedule and data for all algorithms in the correct format
    
    :param file_path: the file_path to the file containing the activities the society are deciding between
    '''
    # runs bruteForce function for the input file
    weekend_schedule, available_t, available_b, timeout, best_ev, best_t, best_b, time_taken = bruteForce(file_path)

    # if all events exceed the constraint, then a message is printed explaining such. Otherwise the input and constraints are printed
    if weekend_schedule == []:
        print("No feasible solution exists. All activities exceed the constraint.")
    else:
        print("="*50)
        print("EVENT PLANNER - RESULTS")
        print("="*50)
        print(f"\nInput File: {file_path}")
        print(f"Available Time: {available_t} hours")
        print(f"Available Budget: £{available_b}")
        print("\n\n--- BRUTE FORCE ALGORITHM ---") 

        # weekend schedule for bruteForce is printed
        printFormat(weekend_schedule, timeout, best_ev, best_t, best_b, time_taken)

        # # runs dynamic function for input file and prints weekend schedule
        print("\n\n--- DYNAMIC PROGRAMMING ALGORITHM ---")
        printFormat(*dynamic(file_path))

        # # runs greedyHeuristic function for input file and prints weekend schedule
        print("\n\n--- Greedy Heuristic ALGORITHM ---")
        printFormat(*greedyHeuristic(file_path))

def printFormat(weekend_schedule, timeout, best_ev, best_t, best_b, time_taken):
    '''
    Prints the schedule and data for one of the algorithms in the correct format.
    If time constraint is met, a message is printed displaying the combination.
    
    :param weekend_schedule: a list of all events in the best combination of events
    :param timeout: True or False depending on if the time limit was reached (5 minutes)
    :param best_ev: total ev for best combination
    :param best_t: total time for best combination
    :param best_b: total monatery cost for best combination
    :param time_taken: length of time in seconds algorith ran for
    '''
    if timeout == True:
        print("Timeout reached, best combination of events checked:")
    print("Selected Activities:")
    for i in range(len(weekend_schedule)):
        print(f"   - {weekend_schedule[i][0]} ({weekend_schedule[i][1]} hours, £{weekend_schedule[i][2]}, enjoyment {weekend_schedule[i][3]})")
    print(f"\nTotal Enjoyment: {best_ev}")
    print(f"Total Time Used: {best_t} hours")
    print(f"Total Cost: £{best_b}")
    print(f"\nExecution Time: {round(time_taken, 7)} seconds")

eventPlanner(input("name of input file:"))
