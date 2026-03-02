connections = [[0 for i in range(4)] for j in range(4)]

for i in range(4):
    for j in range(4):
        connections[i][j] = 1 

for i in range(4):
    print(connections[i])