
# Author : Clara Watson
# Description : final project
# File : FocusGame.py
# Date : December 3, 2020

class FocusGame: 
    def __init__(self, player1, player2):
        print("Player1 is ", player1)
        print("Player2 is ", player2)
        self._player1 = Player(player1[0].upper(), player1[1].upper())
        self._player2 = Player(player2[0].upper(), player2[1].upper())
        color1 = self._player1.get_color()
        color2 = self._player2.get_color()
        self._current_player = None
        self._board = [ [Stack(color1),Stack(color1),Stack(color2), Stack(color2), Stack(color1),Stack(color1)],
                        [Stack(color2),Stack(color2),Stack(color1), Stack(color1), Stack(color2),Stack(color2)],
                        [Stack(color1),Stack(color1),Stack(color2), Stack(color2), Stack(color1),Stack(color1)],
                        [Stack(color2),Stack(color2),Stack(color1), Stack(color1), Stack(color2),Stack(color2)],
                        [Stack(color1),Stack(color1),Stack(color2), Stack(color2), Stack(color1),Stack(color1)],
                        [Stack(color2),Stack(color2),Stack(color1), Stack(color1), Stack(color2),Stack(color2)] ]
                       
    def find_by_name(self, name): 
        """ this mrthod takes a player's name and returns which player it is """
        if name.upper() == self._player1.get_nickname():
            return self._player1
        elif name.upper() == self._player2.get_nickname():
            return self._player2
        return None

    def move_piece(self, name, start, end, number_of_peices_to_move):
        player = self.find_by_name(name)
        start_p = self.get_space(start)
        end_p = self.get_space(end)
        if not self.is_correct_turn(player):
            raise Invalid("Not your turn!")
        if self.is_valid_location(player, start, end, number_of_peices_to_move) == False:
            raise Invalid("Invalid location")
        if self.is_valid_number_peices(start_p, number_of_peices_to_move) == False:
            raise  Invalid("Invalid number of pieces")
        self.make_move(start_p, end_p, number_of_peices_to_move)
        self.check_if_over_five(end_p, player)
        if self.win(player):
            return print(name + " Wins!")
        self.change_turn(player)
        return print("Successfully moved!")

    def show_pieces(self, position):
        """ this method returns the peices in a stack at a given position """
        if not self.coordinates_exist(position):
            return None
        return self._board[position[0]][position[1]].get_stack()

    def show_reserve(self, name):
        """ this method returns the reseved peices the player has """
        player = self.find_by_name(name)
        if player:
            return player.get_reserved()
        return
    
    def show_captured(self, name):
        """ this method returns the amount of captured peices a player has """
        player = self.find_by_name(name)
        if player:
            return player.get_captured()
        return 

    def reserved_move(self, name, position):
        """ this method places the piece from the reserve to the location, reduces the reserve pieces of that player by one and makes appropriate adjustments to pieces at the location"""
        if not self.coordinates_exist(position):
            return 
        player = self.find_by_name(name)
        if not player or player.get_reserved() == 0:
            return print("No pieces in reserve.")
        end = self.get_space(position)
        end.add_peice_to_stack(player.get_color())
        player.sub_reserved()
        self.check_if_over_five(end, player)
        if self.win(player):
            return print(name + " Wins")
        self.change_turn(player)

    def change_turn(self, player):
        """ this method switches the current player to the player that did not just move """
        if player == self._player1:
            self._current_player = self._player2
        else:
            self._current_player = self._player1

    def make_move(self, start, end, number_of_peices_to_move):
        """ this method takes the amount of peices from the start coordinates and moves them to the end coordinates """
        moved = start.remove_from_top(number_of_peices_to_move)
        length = len(moved)
        for i in moved:
            end.add_peice_to_stack(str(i))

    def check_if_over_five(self, end, player):
        """ checks if the end location has more than 5 peices in the stack """
        length = end.get_length_of_stack()
        if length > 5:
            length = length - 5
            self.reserve_and_capture_pieces(end, player)
    
    def reserve_and_capture_pieces(self, end, player):
        """ this method will decide what to do with the extra peices they will either go into reserved or captured """
        extra = end.remove_from_bottom()
        for piece in extra:
            if str(piece) == str(player.get_color()):
                player.add_reserved()
            else:
                player.add_captured()

    def get_space(self, position):
        """returns the coordinate positions at a location """
        return self._board[position[0]][position[1]]
    
    def is_valid_number_peices(self, start, number_of_peices_to_move):
        """ method checks to see if a valid numnber of peices are being moved by the player and not more than they are allowed """
        if number_of_peices_to_move > start.get_length_of_stack():
            return False 
        return True

    def is_correct_turn(self, player):
        """ checks to make sure it is the right players turn """
        if self._current_player is not None and player != self._current_player:
            return False
        return True
    
    def is_valid_location(self, player, start, end, number_of_peices_to_move):
        """ checks to see if the amount of peices on one location can move to a new location without breaking any rules """
        if not self.coordinates_exist(start) or not self.coordinates_exist(end):
            return False
        pos = self.get_space(start)
        if pos.get_top_peice() != player.get_color():
            return False
        if  self.moving_invalid_direction(start, end) == False:
            return False
        if not self.space_equals_peices(start, end, number_of_peices_to_move):
            return False
        return True

    def space_equals_peices(self, start, end, number_of_peices_to_move):
        """ returns false if the number of spaces moved is not equal to the nunber of peices """
        row = end[0] - start[0]
        collum = end[1] - start[1]
        if row == 0:
            spaces= abs(collum)
        else:
            spaces = abs(row)
        if number_of_peices_to_move != spaces:
            return False
        return True

    def moving_invalid_direction(self, start, end):
        """ the player can only move left, right, up, or down so and this method will check that they are moving one of those ways and not diagnol """
        row = end[0] - start[0]
        collum = end[1] - start[1]
        if row != 0 and collum != 0:
            return False
        return True

    def coordinates_exist(self, coordinate):
        """checks to see if the coordinates are coordinates that even exist on the board and if they do return true if not return false """
        if coordinate[0] < 0:
            return False
        if coordinate[1] < 0:
            return False
        if coordinate[1] > 5: 
            return False
        if coordinate[1] > 5:
            return False
        return True
    
    def win(self, player):
        """ checks if the player has captured 5 peices because that is how many you need to win """
        if player.get_captured() >= 6:
            return True
        return False

class Stack:
    def __init__(self,first):
        if not first:
            self._stack = []
        else:
            self._stack = [first.upper()]

    def add_peice_to_stack(self,peice):
        """ adds a peice to the top of the stack """
        self._stack.append(peice)
    
    def top(self):
        """removes peice at the end of the stack list and returns it """
        length = len(self._stack)
        length = length -1 
        if not self.is_empty():
            return self._stack.pop(length)
        return None

    def get_top_peice(self):
        """ checks the color of the peice of the top of the stack """
        length = len(self._stack)
        length = length - 1
        if not self.is_empty():
            return self._stack[length]
        return None
    
    def is_empty(self):
        """ checks if stack is empty """
        length = len(self._stack)
        if length == 0:
            return True
        return False

    def get_stack(self):
        """ returns the list of peices in that stack """
        return self._stack

    def get_length(self):
        """ returns the length of the stack   """
        return len(self._stack)
    
    def get_length_of_stack(self):
        """ returns the amount of peices in the stack """
        return len(self._stack)
    
    def remove_from_bottom(self):
        """ when there are more than 5 peices in a stack the nbottom one gets removed and goes into either reserve or capture """
        peices = []
        if len(self._stack) > 5:
            extra = len(self._stack) - 5
            for i in range(extra):
                peices.append(self._stack.pop(0))
        return peices

    def remove_from_top(self, amount):
        """ when the player wants to move then you will remove the amount of peices they want to move from the top """
        moved = []
        for i in range(amount):
            moved.append(self.top())
        return moved

    

class Player: 
    def __init__(self, nickname, color):
        self._nickname = nickname
        self._color = color
        self._captured = 0
        self._reserved = 0

    def get_color(self):
        """ returns the color the player is peices are """
        return str(self._color)

    def get_nickname(self):
        """ returns the players nickname or what they want to be refered to as """
        return self._nickname

    def get_captured(self):
        """ returns how many pieces that player has captured """
        return self._captured

    def get_reserved(self):
        """returns how many pieces that player has captured  """
        return self._reserved

    def add_captured(self):
        """ adds one to the amount of captured peices that player has """
        self._captured = self._captured + 1

    def add_reserved(self):
        """ adds one to the amount of reserved peices that player has """
        self._reserved = self._reserved + 1
    
    def sub_reserved(self):
        """ subtracts one from the amount of reserved peices that player has """
        self._reserved = self._reserved - 1

class Invalid(Exception):
    pass
