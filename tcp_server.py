import json
from shared import *
from sqlalchemy import create_engine
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker
from sql import Base
from sql import Players
import socket

buffer = 1024
def start_server():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = "10.0.2.15"
    # set a port number
    port = 30247

    # bind the socket to a public host and a port
    server_socket.bind((host, port))
    print(f"Socket bound to host {host} on port {port}")

    # listen for incoming connections
    server_socket.listen(5)
    print("Waiting for incoming connections...")

    while True:
        # accept a client connection
        client_sock, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_request(client_sock)



def ori_send_msg(client_sock, message):
    client_sock.sendall(message.encode('utf-8'))
    print(f"Sent message: {message}")


def send_Error(client_sock, error_message):
    error = "ERROR: " + error_message
    client_sock.sendall(error.encode('utf-8'))
    print(f"Sent error message: {error}")


def cdb():
    global db_session
    engine = create_engine('sqlite:///tcp.db', echo=False)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    db_session = session()

    db_session.query(Players).delete()

    c1 = Players(name="Oscar Gluch", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                 goals=6,
                 assists=4)
    db_session.add(c1)
    db_session.commit()

    db_session.add_all(
        [
            Players(name="Eran Zahavi", team="Maccabi Tel aviv", league="La liga", national="Israel", position="ATT",
                    goals=15,
                    assists=4),
            Players(name="Dor Perez", team="Maccabi Tel aviv", league="La liga", national="Israel", position="MID",
                    goals=2,
                    assists=3),
            Players(name="Lionel Messi", team="Paris Saint-Germain", league="Ligue 1", national="Argentina",
                    position="ATT", goals=18, assists=8),
            Players(name="Cristiano Ronaldo", team="Manchester United", league="Premier League",
                    national="Portugal", position="ATT", goals=13, assists=4),
            Players(name="Kylian Mbappe", team="Paris Saint-Germain", league="Ligue 1", national="France",
                    position="ATT", goals=17, assists=8),
            Players(name="Robert Lewandowski", team="Bayern Munich", league="Bundesliga", national="Poland",
                    position="ATT", goals=27, assists=6),
            Players(name="Erling Haaland", team="Borussia Dortmund", league="Bundesliga", national="Norway",
                    position="ATT", goals=19, assists=5),
            Players(name="Kevin De Bruyne", team="Manchester City", league="Premier League", national="Belgium",
                    position="MID", goals=5, assists=11),
            Players(name="N'Golo Kante", team="Chelsea", league="Premier League", national="France",
                    position="MID", goals=1, assists=2),
            Players(name="Karim Benzema", team="Real Madrid", league="La Liga", national="France",
                    position="ATT", goals=17, assists=7),
            Players(name="Mohamed Salah", team="Liverpool", league="Premier League", national="Egypt",
                    position="ATT", goals=16, assists=4),
            Players(name="Sadio Mane", team="Liverpool", league="Premier League", national="Senegal",
                    position="ATT", goals=8, assists=3),
            Players(name="Gareth Bale", team="Tottenham Hotspur", league="Premier League", national="Wales",
                    position="ATT", goals=7, assists=2),
            Players(name="Son Heung-min", team="Tottenham Hotspur", league="Premier League",
                    national="South Korea", position="ATT", goals=12, assists=5),
            Players(name="Virgil van Dijk", team="Liverpool", league="Premier League", national="Netherlands",
                    position="DEF", goals=0, assists=0),
            Players(name="Ruben Dias", team="Manchester City", league="Premier League", national="Portugal",
                    position="DEF", goals=1, assists=0),
            Players(name="Jan Oblak", team="Atletico Madrid", league="La Liga", national="France", position="GK",
                    goals=0, assists=0),
            Players(name="Serge Gnabry", team="Bayern Munich", league="Bundesliga", national="Germany", position="ATT",
                    goals=5, assists=2),
            Players(name="Lautaro Martinez", team="Inter Milan", league="Serie A", national="Argentina", position="ATT",
                    goals=13, assists=3),
            Players(name="Pierre-Emerick Aubameyang", team="Arsenal", league="Premier League", national="Gabon",
                    position="ATT", goals=7, assists=1)
        ]
    )
    return db_session


def get_all():
    result = db_session.query(Players).all()
    return result


def insert_player(name, team, league, national, position, goals, assists):
    global db_session
    new_player = Players(name=name, team=team, league=league, national=national, position=position, goals=goals,
                         assists=assists)
    db_session.add(new_player)
    db_session.commit()
    print(f"Player {name} added to the database")
    return new_player

#Delete by name
def delete_player_by_name(name):
    global db_session
    player = db_session.query(Players).filter(Players.name.like(f'{name}%')).first()
    if player:
        db_session.delete(player)
        db_session.commit()
        return f"Player {name} deleted successfully.\n"
    else:
        return "Player not found in the database.\n"


# update the number of assists for the player
def update_player_goals(name, new_goals):
    global db_session
    player = db_session.query(Players).filter(Players.name.like(f'{name}%')).first()
    if player:
        player.goals = new_goals
        db_session.commit()
        return f"Goals for player {name} updated to {new_goals}"
    else:
        return f"Player {name} not found in the database"


# update the number of asists for the player
def update_player_assists(name, new_assists):
    global db_session
    player = db_session.query(Players).filter(Players.name.like(f'{name}%')).first()
    if player:
        player.assists = new_assists
        db_session.commit()
        return f"Assists for player {name} updated to {new_assists}"
    else:
        return f"Player {name} not found in the database"


# find player by id
def get_player_by_id(player_id):
    global db_session
    player = db_session.query(Players).filter_by(id=player_id).first()
    if player:
        print(f"Player {player.name} found in the database")
        return player
    else:
        print(f"Player with ID {player_id} not found in the database")
        return None



# check the current team of the player
def transfer_player(name, new_team):
    global db_session
    player = db_session.query(Players).filter(Players.name.like(f'{name}%')).first()
    if player:
        player.team = new_team
        db_session.commit()
        return f"Player {name} has been transferred to {new_team}"
    else:
        return f"Player {name} not found in the database"


# return the number of the times that the player was involved in goal
def get_goals_involvement(name):
    global db_session
    player = db_session.query(Players).filter(Players.name.like(f'{name}%')).first()
    sum = player.goals + player.assists
    return sum


# return the full squad of every national team
def get_squad_national(national):
    global db_session
    players = db_session.query(Players).filter(Players.national.like(f'{national}%')).all()
    return players


# return the full squad of every  team
def get_squad_team(team):
    global db_session
    players = db_session.query(Players).filter(Players.team.like(f'{team}%')).all()
    return players


# chack if this two players  play together
def playing_together(p1, p2):
    player1=player = db_session.query(Players).filter(Players.name.like(f'{p1}%')).first()
    player2 = player = db_session.query(Players).filter(Players.name.like(f'{p2}%')).first()
    if player1.team == player2.team:
        return "They are playing together\n"
    return "They are not playing together\n"

def get_all_players_by_position(position):
    global db_session
    players = db_session.query(Players).filter(Players.position.like(f'{position}%')).all()
    return players

def get_players_by_goals(number):
    global db_session
    players = db_session.query(Players).filter(Players.goals>=number).all()
    return players


def handle_request(client_sock):
    while True:
        message = client_sock.recv(buffer)
        print(message.decode())
        request = message.decode('utf-8').strip()
        # Get all players
        if request == "get_all_players":
            result = get_all()
            response = ""
            for player in result:
                response += str(player)
            client_sock.send(response.encode())
        # Insert a new player
        elif request.startswith("insert_player"):
            try:
                _, name, team, league, national, position, goals, assists = request.split("-")
                response = insert_player(name, team, league, national, position, goals, assists)
                response=response.__str__()
            except:
                response = "Invalid input. Please provide all player details separated by -."
            client_sock.send(response.encode('utf-8'))
        # Delete a player by name
        elif request.startswith("delete_player"):
            try:
                _, name = request.split("-")
                response = delete_player_by_name(name)
            except:
                response = "Invalid input. Please provide the name of the player to delete."
            client_sock.send(response.encode('utf-8'))
        # Update player's goals
        elif request.startswith("update_goals"):
            try:
                _, name, new_goals = request.split("-")
                update_player_goals(name, new_goals)
                response = f"Goals for player {name} updated to {new_goals}"
            except:
                response = "Invalid input. Please provide the name of the player and the new number of goals."
            client_sock.send(response.encode('utf-8'))
        # Update player's assists
        elif request.startswith("update_assists"):
            try:
                _, name, new_assists = request.split("-")
                update_player_assists(name, new_assists)
                response = f"Assists for player {name} updated to {new_assists}"
            except:
                response = "Invalid input. Please provide the name of the player and the new number of assists."
            client_sock.send(response.encode('utf-8'))
        # Find player by ID
        elif request.startswith("find_player"):
            try:
                _, player_id = request.split("-")
                player = get_player_by_id(player_id)
                if player:
                    response = f"Player {player.name} found in the database"
                else:
                    response = f"Player with ID {player_id} not found in the database"
            except:
                response = "Invalid input. Please provide the ID of the player to find."
            client_sock.send(response.encode('utf-8'))
        # Transfer player to new team
        elif request.startswith("transfer_player"):
            try:
                _, name, new_team = request.split("-")
                transfer_player(name, new_team)
                response = f"Player {name} has been transferred to {new_team}"
            except:
                response = "Invalid input. Please provide the name of the player and the name of the new team."
            client_sock.send(response.encode('utf-8'))
        # Get total goals involvement of a player
        elif request.startswith("goals_involvement"):
            try:
                _, name = request.split("-")
                sum = get_goals_involvement(name)
                response = f"{name} is involved in {sum} goals"
            except:
                response = "Invalid input. Please provide the ID of the player."
            client_sock.send(response.encode('utf-8'))
        #Get all players belong to this national
        elif request.startswith("get_squad_national"):
            try:
                _,nation = request.split("-")
                result = get_squad_national(nation)
                response = ""
                for player in result:
                    response += str(player) + "\n"
            except:
                response="No such nation"
            client_sock.send(response.encode('utf-8'))
        #Get all players from the team
        elif request.startswith("get_squad_team"):
            try:
                _,team = request.split("-")
                result = get_squad_team(team)
                response = ""
                for player in result:
                    response += str(player) + "\n"
            except:
                response="No such team"
            client_sock.send(response.encode('utf-8'))
        #Check if two players playing in the same team
        elif request.startswith("playing_together"):
            try:
                _,p1,p2 = request.split("-")
                response = playing_together(p1,p2)
            except:
                response="No such player\s"
            client_sock.send(response.encode('utf-8'))
        #Get all players by position
        elif request.startswith("get_all_players_by_position"):
            try:
                _, pos = request.split("-")
                result = get_all_players_by_position(pos)
                response = ""
                for player in result:
                    response += str(player) + "\n"
            except:
                response = "No such position"
            client_sock.send(response.encode('utf-8'))
        #Get all players with more than X goals.
        elif request.startswith("get_players_by_goals"):
            try:
                _, num = request.split("-")
                result = get_players_by_goals(num)
                response = ""
                for player in result:
                    response += str(player) + "\n"
            except:
                response = "No such players"
            client_sock.send(response.encode('utf-8'))
        elif request.startswith("exit"):
            print("TCP Server is disconnecting from the client")
            client_sock.close()
            break

if __name__ == '__main__':
    cdb()
    start_server()