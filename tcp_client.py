import socket
import struct
from shared import *

from tcp_server import buffer

app_server_ip =  "10.0.2.15"




def client_handle_request(client_socket):
    while True:
        print(f"Select an option from the list (by number) and then press enter.")

        while True:
            print(
                f" 1.Get all player.\n 2.Insert player. \n 3.Delete player\n 4.Update player's goals\n 5.Update player's "
                f"assists\n 6.Find player by ID"
                f"\n 7.Transfer player\n 8.Get player's total goals involvement.\n 9.Get national squad.\n 10.Get team "
                f"squad.\n 11.Check if 2 players playing together. \n 12.Get all players by position.\n 13. Get all players with more then X goals. \n \n To close the connection please enter 20")

            choice = int(input())
            if choice==1:
                s = "get_all_players"
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==2:
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
                print(result)
            elif choice==3:
                s="delete_player-"
                print("Enter player's name to be deleted:")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==4:
                s="update_goals-"
                print("Please enter the player name")
                s+=input()+"-"
                print("Please enter new goals count")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==5:
                s="update_assists-"
                print("Please enter player's name.")
                s+=input()+"-"
                print("Please enter new assists count.")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==6:
                s="find_player-"
                print("Please enter player's ID")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==7:
                s="transfer_player-"
                print("Please enter player's name.")
                s+=input()+"-"
                print("Please enter the player's new team.")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==8:
                s="goals_involvement-"
                print("Please enter player's name.")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==9:
                s="get_squad_national-"
                print("Enter the nation of the squad you wish.")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==10:
                s="get_squad_team-"
                print("Enter team name")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==11:
                s="playing_together-"
                print("Please enter player1 name")
                s+=input()+"-"
                print("Please enter player2 name")
                s += input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==12:
                s="get_all_players_by_position-"
                print("Please enter the position")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==13:
                s="get_players_by_goals-"
                print("Enter number of goals:")
                s+=input()
                client_socket.send(s.encode())
                result = receive_share(client_socket)
                print(result)
            elif choice==20 :
                print("Thank you for using our program :)")
                client_socket.close()
                return
            else:
                print("Invalid input, please try again.\n")


def connect_client():
    global app_server_ip
    client_socket = socket.socket()
    client_socket.connect((app_server_ip, 30247))
    client_handle_request(client_socket)
    # client_socket.close()

if __name__ == '__main__':
    connect_client()
