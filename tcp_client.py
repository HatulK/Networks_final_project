import socket
import struct
from shared import *

from tcp_server import buffer

app_server_ip =  "10.0.2.15"




def client_handle_request(client_socket):
    while True:
        print(f"Select an option from the next list (by number) and then press enter.")
        print(f"1.Get all player.\n 2.Insert player. \n 3.Delete player\n 4.Update player's goals\n 5.Update player's "
              f"assists\n 6.Find player"
              f"\n 7.Transfer player\n 8.Get player's total goals involvement.\n 9.Get national squad.\n 10.Get team "
              f"squad.\n 11.Check if 2 players playing together ")
        choice = input()
        if choice==1:
            s = "get_all_players"
            client_socket.send(s.encode())
        if choice==2:
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
            s += input() + "-"
            client_socket.send(s.encode())
        if choice==3:
            s="delete_player-"
            print("Enter player's name to be deleted:")
            s+=input()
            client_socket.send(s.encode())
        if choice==4:
            s="update_goals-"
            print("Please enter the player name")
            s+=input()+"-"
            print("Please enter new goals count")
            s+=input()
            client_socket.send(s.encode())
        if choice==5:
            s="update_assists-"
            print("Please enter player's name.")
            s+=input()+"-"
            print("Please enter new assists count.")
            s+=input()
            client_socket.send(s.encode())
        if choice==6:
            s="find_player-"
            print("Please enter player's name")
            s+=input()+"-"
            client_socket.send(s.encode())
        if choice==7:
            s="transfer_player-"
            print("Please enter player's name.")
            s+=input()+"-"
            print("Please enter the player's new team.")
            s+=input()
            client_socket.send(s.encode())
        if choice==8:
            s="goals_involvement-"
            print("Please enter player's name.")
            s+=input()+"-"



        result = receive_share(client_socket)
        print(result)
def connect_client():
    global app_server_ip
    client_socket = socket.socket()
    client_socket.connect((app_server_ip, 30247))
    client_handle_request(client_socket)
    client_socket.close()

if __name__ == '__main__':
    connect_client()
