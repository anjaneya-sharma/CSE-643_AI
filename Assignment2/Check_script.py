
import pandas as pd

import csv

from collections import deque


df  = pd.read_csv('Road_Distance.csv')

cities = set()




def Return_Adj():
    with open('Road_Distance.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        
        for i in range (1,len(data)):
            cities.add(data[i][0])
        

    adjacency_list = {city: {} for city in cities}

    for i in range(1, len(data)):
        current_city = data[i][0]
        for j in range(1, len(data[i])):
            if  data[i][j] != "-":
                adjacent_city = data[0][j]
                distance = int(data[i][j])
                adjacency_list[current_city][adjacent_city] = distance
                adjacency_list[adjacent_city][current_city] = distance

    
    
    return adjacency_list

Open = [] 
Close = []

# f_val={}
# h_val={}
# g_val={}

def calculate_heuristic( start, end, adj_lst, ind):
    if start == end:
        return 0

    visited = set()
    queue = deque([(start, 0)])
    while queue:
        current, distance = queue.popleft()
        if current == end and ind == 0:
            return 0
        elif current == end and ind == 1:
            return distance - 190
        elif current == end and ind == 2:
            return distance + 100000
        visited.add(current)
        for neighbor, cost in adj_lst[current].items():
            if neighbor not in visited:
                queue.append((neighbor, distance + cost))
    return float('inf')  # If no path is found




def Astar( start, end  ,  adj_lst, heur):
    open_list = [start]
    closed_list = []
    g_values = {start: 0}
    parents = {start: None}
    current = None

    while open_list:
        if heur == 1:
            current = min(open_list, key=lambda city: g_values[city] + calculate_heuristic( city, end,adj_lst,1))
        elif heur == 2:
            current = min(open_list, key=lambda city: g_values[city] + calculate_heuristic( city, end,adj_lst,2))
        elif heur == 0 :
            current = min(open_list, key=lambda city: g_values[city] + 0)
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            path.reverse()
            return path

        open_list.remove(current)
        closed_list.append(current)

        for neighbor, cost in adj_lst[current].items():
            if neighbor in closed_list:
                continue

            tentative_g = g_values[current] + cost
            if neighbor not in open_list or tentative_g < g_values[neighbor]:
                open_list.append(neighbor)
                parents[neighbor] = current
                g_values[neighbor] = tentative_g

    return None

adj_lst = Return_Adj()

cities = list(cities)

for i in range(len(cities)-1):
    for j in range(i+1,len(cities)):
        path_Astar_admissible = Astar(cities[i],cities[j],adj_lst,0)
        path_Astar_inadmissible = Astar(cities[i],cities[j],adj_lst,1)
        path_Astar_ucs = Astar(cities[i],cities[j],adj_lst,2)
        
        if path_Astar_admissible == path_Astar_inadmissible :
            continue
        else :
            print("Paths not matching here")
            print("path_Astar_admissible",path_Astar_admissible)
            print("path_Astar_inadmissible",path_Astar_inadmissible)
            # print("path_Astar_ucs",path_Astar_ucs)
            
            
            
            
            