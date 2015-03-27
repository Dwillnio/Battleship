from random import randint
from copy import deepcopy,copy



def print_board(board): #prints board/list with format [[a1,b1,c1..],[a2,b2,c2..],[..]...]
    for row in board: print (" ".join(row))


def gen_board(length): #generates board/list with format [[O,O,O..],[O,O,O..],[..]...] with len board == len board[0]
    board = []
    for x in range(length): board.append(["O"] * length)
    return board


def check_if_ship_ocean(ship,board): #checks if any ship tile is outside map
    for x in ship[0]:
        if x < 0 or x > (len(board)): return False
    for x in ship[1]:
        if x < 0 or x > (len(board)): return False
    return True
                                       #ship = [[x,y,..],[a,b,..]]


def check_ship_collisions(ship,ships): #checks if ship collides with preexisting ships
    for z in range(len(ship[0])):      #ships = [[x,y,...],[a,b,...]] #for each coordinate
        for y in range(len(ships[0])):
            if ship[0][z] == ships[0][y] and ship[1][z] == ships[1][y]: return False
    return True


def gen_ship(board, ships_n_l): #generates a ship with certain criterias(length, in map, direction...)
    ship_len = 0
    ship_direc = randint(1, 4)  #assigns random direction 1:up 2:right 3:down 4:left
    coor = [[], []] #ship coordinates container
    for x in enumerate(ships_n_l):  # determines which ship length to generate
        if x[1] != 0:      #takes the next lowest length
            ship_len = x[0]+1
            break
    else:
        print ("error")  # should quit generation bcs no ships left -> should never happen
    coor[0].append(randint(0, len(board) - 1))     # creates first part of the ship
    coor[1].append(randint(0, len(board[0]) - 1))
    ref_coor = [coor[0][0], coor[1][0]] #if shiplength > 1 this coordinate will always be used as reference
    ship_len -= 1
    while True:
        if ship_len <= 0: break
        if ship_direc == 1:                 #adds a shiptile on the top of refcoor
            coor[0].append(ref_coor[0])     #
            coor[1].append(ref_coor[1] + 1) #
            ref_coor[1] += 1                #changes refcoor
        elif ship_direc == 2:               #same
            coor[0].append(ref_coor[0] + 1)
            coor[1].append(ref_coor[1])
            ref_coor[0] += 1
        elif ship_direc == 3:              #same
            coor[0].append(ref_coor[0])
            coor[1].append(ref_coor[1] - 1)
            ref_coor[1] -= 1
        elif ship_direc == 4:              #same
            coor[0].append(ref_coor[0] - 1)
            coor[1].append(ref_coor[1])
            ref_coor[0] -= 1
        ship_len -= 1 #reduces shiplength
    return coor #returns the ship coordinates


def check_if_stacked(ship): #checks if shiptiles of same ship are on top of eachother ship = [[a1,b1,c1..],[a2,b2,c2..]]
    for x in enumerate(ship[0]):
        for y in enumerate(ship[0]):
            if x[1] == y[1] and ship[1][x[0]] == ship[1][y[0]] and x[0] != y[0]: return False
    return True


def check_if_ship_line(ship): #checks if ship max coor diff is smaller than length||ship = [[a1,b1,c1...],[a2,b2,c2...]]
    counter = 0
    for x in range(len(ship[0])):
        for y in range(len(ship[0])):
            if abs(ship[0][x] - ship[0][y]) > len(ship[0])-1: counter +=1
    for x in range(len(ship[1])):
        for y in range(len(ship[1])):
            if abs(ship[1][x] - ship[1][y]) > len(ship[0])-1: counter += 1
    if counter >= 1: return False
    else: return True


def gen_ships_final(board,ships_n_l): #"main function" for ship generation
    ships = [[],[]]
    c_ship_n_l = ships_n_l[:] #ship_n_l format: [num 1b ships,num 2b ships...,num 5b ships]
    hold_gen = [[],[]]
    count = 0
    while sum(ships_n_l) > 0:
        count +=1
        hold_gen = gen_ship(board, ships_n_l)
        if check_if_ship_ocean(hold_gen,board) == True and check_ship_collisions(hold_gen,ships) == True:
            for x in hold_gen[0]:
                ships[0].append(x)
            for y in hold_gen[1]:
                ships[1].append(y)
            ships_n_l[len(hold_gen[0])-1] -= 1
        if count > 400:
            ships = [[],[]]
            count = 0
            ships_n_l = c_ship_n_l[:]
    return ships


def check_guess(guess,ships):  #checks if guess hits a shiptile
    for x in enumerate(ships[0]):
        if ships[0][x[0]] == guess[0] and ships[1][x[0]] == guess[1]: return True
    return False


def get_hit_index(guess,ships): #returns the index of a shiptile hit
    for x in enumerate(ships[0]):
        if ships[0][x[0]] == guess[0] and ships[1][x[0]] == guess[1]: return x[0]
    return False


def get_ships_loc(board,ships): #returns a board with all locations of a list ships marked as "X"
    print (ships)
    new_board = deepcopy(board)            #new_board format: [["0","0","0"],["0","0","0"],["0","0","0"],...
    for x in enumerate(ships[0]):
        new_board[x[1]][ships[1][x[0]]] = "X"
    return new_board


def check_if_ship_straight(ship): #checks if ship is straight / a line
    if len(ship[0]) == 1: return True
    counter = 0
    for x in ship[0]:
        if x == ship[0][0]: counter += 1
        else: break
    if counter == len(ship[0]): return True
    else:
        counter = 0
        for x in ship[1]:
            if x == ship[1][0]: counter += 1
            else: break
        if counter == len(ship[1]): return True
        else: return False


def user_gen_ships(board,ships_n_l):  #lets user generate a certain ships -> determined by ships_n_l
    ships = [[],[]]  #container that gets returned || contains all user ships
    c_ships_n_l = copy(ships_n_l)  #incase of user errors
    while sum(ships_n_l) > 0:
        ship = [[],[]]  #container for a user ship || gets checked for certain conditions and if ok added to ships
        print ("You have to set: " + str(ships_n_l))
        dec = int(input("Which length do you want to set: "))
        if dec > len(ships_n_l) or ships_n_l[dec-1] <= 0 or dec == 0:
            print ("ERROR")
            ships = [[],[]]
            ships_n_l = copy(c_ships_n_l)
        else:
            for x in range(dec):
                ship[1].append(int(input("X: "))-1)
                ship[0].append(int(input("Y: "))-1)
            if check_if_ship_straight(ship) and check_if_ship_ocean(ship,board) and check_ship_collisions(ship,ships) and check_if_stacked(ship) and check_if_ship_line(ship):
                ships_n_l[dec-1] -= 1
                for x in ship[0]: ships[0].append(x)
                for x in ship[1]: ships[1].append(x)
            else:
                print (str(check_if_ship_straight(ship)) + str(check_if_ship_ocean(ship,board)) + str(check_ship_collisions(ship,ships)))
                print (str(check_if_stacked(ship)) + str(check_if_ship_line(ship)))
                print ("ERROR")
                ships = [[],[]]
                ships_n_l = copy(c_ships_n_l)
    return ships


def user_gen_ships_final(board,ships_n_l):  #"main function" for user ship generating process
    user_board = deepcopy(board)
    c_ships_n_l = deepcopy(ships_n_l)
    ships = user_gen_ships(user_board,c_ships_n_l)
    ships_loc = get_ships_loc(user_board,ships)
    print_board(ships_loc)
    if input("Is this okay?(y/n): ") == "y": return ships
    else:
        user_gen_ships_final(board,ships_n_l)


def KI_guess(board):  #Makes a random guess || to be improved
    guess = [0,0]
    while True:
        guess[0] = randint(0,len(board)-1) #Indexformat
        guess[1] = randint(0,len(board)-1) #Indexformat
        if board[guess[0]][guess[1]] != "X" and board[guess[0]][guess[1]] != "H": return guess


def count_ship_b(ships_n_l):  #counts the total of shiptiles given by a ships_n_l-format list
    multiplyer = 1
    total = 0
    for x in ships_n_l:
        total += x * multiplyer
        multiplyer += 1
    return total


def init_game_KI(board,ships_n_l):  #"main function" for intiating the game with a p vs AI mode
    c_board = deepcopy(board)
    c_ships_n_l = ships_n_l[:]
    user_ships = user_gen_ships_final(c_board,c_ships_n_l)
    AI_ships = gen_ships_final(board,ships_n_l)
    return [user_ships,AI_ships]


def init_game_2P(board,ships_n_l):  #"main function" for initiating the game with a p vs p mode
    c_board = deepcopy(board)
    c_ships_n_l = ships_n_l[:]
    print ("Player 1 ship creation")
    user1_ships = user_gen_ships_final(c_board,c_ships_n_l)
    print ("Player 2 ship creation")
    user2_ships = user_gen_ships_final(board,ships_n_l)
    return [user1_ships,user2_ships]


def user_guess(board):  #lets the user guess a coordinate and checks if certain conditions are met
    while True:
        guess = [0,0]
        guess[0] = int(input("Guess Row:"))-1 #-1 to convert so col 1-5 and row 1-5 instead of 0-4
        guess[1] = int(input("Guess Col:"))-1
        if guess[0]+1 <= len(board) and guess[0]+1 <= len(board) and not guess[0] < 0 and not guess[1] < 0:
            if board[guess[0]][guess[1]]== "X" or board[guess[0]][guess[1]]== "H":
                print("Already guessed that coordinate")
            else:
                return guess
        else: print("Out of bounds")


def battleship_solo(board,turns,ships_n_l): #solo mode main function
    print ("Solo Battleship!")
    x = 0
    ship_counter = count_ship_b(ships_n_l)
    ships = gen_ships_final(board,ships_n_l)
    guess=[0,0]
    while x < turns:
        print ("-" * int(len(board)*1.9))
        print_board(board)
        print ("-" * int(len(board)*1.9))

        guess[0] = int(input("Guess Row:"))-1 #-1 to convert so col 1-5 and row 1-5 instead of 0-4
        guess[1] = int(input("Guess Col:"))-1

        if (guess[0] < 0 or guess[0]+1 > len(board)) or (guess[0] < 0 or guess[0]+1 > len(board)):
            print ("Oops, that's not even in the ocean.")
        elif(board[guess[0]][guess[1]] == "X"):
            print ("You guessed that one already.")
        elif check_guess(guess,ships) == True:
            ship_counter += -1
            if ship_counter == 0:
                print ("Congratulations you sunk all my ships")
                dec = input("Replay?(y/n): ")
                if dec == "y":
                    main(turns,ships_n_l,board)
                else:
                    break
            else:
                print ("Congratulations! You sunk a battleship!")
                board[guess[0]][guess[1]] = "H"
        else:
            x += 1
            print ("You missed my battleship!")
            board[guess[0]][guess[1]] = "X"
            if x == turns:
                print ("Out of turns")
                for x in get_ships_loc(board,ships):
                    print (" ".join(x))
                dec = input("Replay?(y/n): ")
                if dec == "y":
                    main(turns,ships_n_l,board)
                else:
                    break
        print ("%s turns left" %(turns - x))


def battleship_KI(board,ships_n_l): #P vs AI mode main function
    user_board = deepcopy(board)
    KI_board = deepcopy(board)
    KI_ship_count = count_ship_b(ships_n_l)
    user_ship_count = count_ship_b(ships_n_l)
    container = init_game_KI(board,ships_n_l)
    user_ships = container[0]
    KI_ships = container[1]
    while True:
        print ("-" * int(len(board)*1.9))
        print_board(user_board)
        print ("-" * int(len(board)*1.9))
        u_guess = user_guess(board)
        if check_guess(u_guess,KI_ships) == True:
            KI_ships[0].pop(get_hit_index(u_guess,KI_ships))
            KI_ships[1].pop(get_hit_index(u_guess,KI_ships))
            KI_ship_count -= 1
            user_board[u_guess[0]][u_guess[1]] = "H"
            print ("Hit!")
            if KI_ship_count <= 0:
                print_board(KI_board)
                print ("You won!")
                return True #True = user won
        else:
            user_board[u_guess[0]][u_guess[1]] = "X"
            print("Miss")
        K_guess = KI_guess(board)
        if check_guess(K_guess,user_ships) == True:
            user_ships[0].pop(get_hit_index(K_guess,user_ships))
            user_ships[1].pop(get_hit_index(K_guess,user_ships))
            user_ship_count -= 1
            KI_board[K_guess[0]][K_guess[1]] = "H"
            print ("Enemy hit")
            if user_ship_count <= 0:
                print_board(KI_board)
                print ("The AI won")
                return False #False = user lost
        else:
            KI_board[K_guess[0]][K_guess[1]] = "X"
            print("Enemy miss")


def battleship_2p(board,ships_n_l): #P vs P mode main function
    user1_board = deepcopy(board)
    user2_board = deepcopy(board)
    user2_ship_count = count_ship_b(ships_n_l)
    user1_ship_count = count_ship_b(ships_n_l)
    container = init_game_2P(board,ships_n_l)
    user1_ships = container[0]
    user2_ships = container[1]
    while True:
        print ("Player 1 guess")
        print_board(user1_board)
        u1_guess = user_guess(board)
        if check_guess(u1_guess,user2_ships) == True: #checks if guess hit a shiptile
            user2_ships[0].pop(get_hit_index(u1_guess,user2_ships)) #if so removes that shiptile from the list ships
            user2_ships[1].pop(get_hit_index(u1_guess,user2_ships))
            user2_ship_count -= 1
            user1_board[u1_guess[0]][u1_guess[1]] = "H"
            print ("Player1 Hit!")
            if user2_ship_count <= 0:
                print("User 1 won!")
                return True #True = user1 won
        else:
            user1_board[u1_guess[0]][u1_guess[1]] = "X"
            print("Miss")
        print ("Player 2 guess")
        print_board(user2_board)
        u2_guess = user_guess(board)
        if check_guess(u2_guess,user1_ships) == True:
            user1_ships[0].pop(get_hit_index(u2_guess,user1_ships))
            user1_ships[1].pop(get_hit_index(u2_guess,user1_ships))
            user1_ship_count -= 1
            user2_board[u2_guess[0]][u2_guess[1]] = "H"
            print ("Player2 hit!")
            if user1_ship_count <= 0:
                print("User 2 won!")
                return False #False = user2 won
        else:
            user2_board[u2_guess[0]][u2_guess[1]] = "X"
            print("Miss")


def main(turns,ships_n_l,board): #lets the user decide what he wants to play
    while True:
        dec = input("What do you want to play(1:Solo ; 2:P vs AI ; 3:P vs P): ")
        if dec == "1": battleship_solo(board,turns,ships_n_l) #starts solo mode function
        elif dec == "2": battleship_KI(board,ships_n_l) #starts P vs AI mode function
        elif dec == "3": battleship_2p(board,ships_n_l) #starts P vs P mode function
        else: break



main(15,[4,3,2,1],gen_board(8))
