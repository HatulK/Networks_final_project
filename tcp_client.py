import socket
import struct
from shared import *

from tcp_server import buffer
# function to handle requests from client
def client_handle_request(client_socket):
    while True:
        print(f"Select an option from the list (by number) and then press enter.")

        while True:
            # Display the options to the user
            print(
                f" 1.Get all player.\n 2.Insert player. \n 3.Delete player\n 4.Update player's goals\n 5.Update player's "
                f"assists\n 6.Find player by ID"
                f"\n 7.Transfer player\n 8.Get player's total goals involvement.\n 9.Get national squad.\n 10.Get team "
                f"squad.\n 11.Check if 2 players playing together. \n 12.Get all players by position.\n 13. Get all players with more then X goals. \n \n To close the connection please enter 20")

            # Get the user's choice
            choice = int(input())
            if choice==1:
                # Check the user's choice and take the appropriate action
                s = "get_all_players"
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==2:
                # Insert a new player
                s ="insert_player-"
                print("Enter the player name and then press enter.")
                s+=input()+"-"
                print("Enter the player team and then press enter.")
                s += input() + "-"
                print("Enter the player league and then press enter.")
                s += input() + "-"
                print("Enter the player nationality and then press enter.")
                s += input() + "-"
                print("Enter the player position and then press enter.")
                s += input() + "-"
                print("Enter the player goals count and then press enter.")
                s += input() + "-"
                print("Enter the player assist count and then press enter.")
                s += input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(f"Player added.\n")
            elif choice==3:
                # Delete a player
                s="delete_player-"
                print("Enter player's name to be deleted:")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==4:
                # Update player's goals
                s="update_goals-"
                print("Please enter the player name")
                s+=input()+"-"
                print("Please enter new goals count")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==5:
                # Update player's assists
                s="update_assists-"
                print("Please enter player's name.")
                s+=input()+"-"
                print("Please enter new assists count.")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==6:
                # Find player by ID
                s="find_player-"
                print("Please enter player's ID")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==7:
                # Transfer player to another team
                s="transfer_player-"
                print("Please enter player's name.")
                # add player's name to the message
                s+=input()+"-"
                print("Please enter the player's new team.")
                s+=input()  # add player's new team to the message
                client_socket.send(s.encode())  # send the message to the server
                result = receive_share(client_socket)       # receive the result from the server
                print(result)       # print the result
            elif choice==8:

                s="goals_involvement-"  # set the action type
                print("Please enter player's name.")
                s+=input()  # add player's name to the message
                client_socket.send(s.encode())  # send the message to the server
                result = receive_share(client_socket)
                print(result)
            elif choice==9:

                s="get_squad_national-" # set the action type
                print("Enter the nation of the squad you wish.")
                s+=input()  # add the nation to the message
                client_socket.send(s.encode())      # send the message to the server
                result = receive_share(client_socket)   # receive the result from the server
                print(result)
            elif choice==10:
                s="get_squad_team-"     # set the action type
                print("Enter team name")
                s+=input()      # add the team name to the message
                client_socket.send(s.encode())   # send the message to the server
                result = receive_share(client_socket)       # receive the result from the server
                print(result)       # print the result
            elif choice==11:
                s="playing_together-"       # set the action type
                print("Please enter player1 name")
                s+=input()+"-"      # add player1's name to the message
                print("Please enter player2 name")
                s += input()           # add player2's name to the message
                client_socket.send(s.encode())      # send the message to the server
                result = receive_share(client_socket)   # receive the result from the server
                print(result)
            elif choice==12:
                s="get_all_players_by_position-"    # set the action type
                print("Please enter the position")
                s+=input()  # add the position to the message
                client_socket.send(s.encode())  # send the message to the server
                result = receive_share(client_socket)       # receive the result from the server
                print(result)
            elif choice==13:
                s="get_players_by_goals-"   # set the action type

                print("Enter number of goals:")
                s+=input()      # add the number of goals to the message
                client_socket.send(s.encode())      # send the message to the server
                result = receive_share(client_socket)        # receive the result from the server
                print(result)
            elif choice==20 :
                print("Thank you for using our program :)")
                client_socket.send("exit".encode())
                client_socket.close()           # close the client socket
                return
            else:
                print("Invalid input, please try again.\n")


def connect_client(ip):
    client_socket = socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(('',20247))
    client_socket.connect((ip, 30247))
    client_handle_request(client_socket)
    client_socket.close()
