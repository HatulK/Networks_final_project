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
        while True:
            message = client_sock.recv(buffer)
            print(message.decode())
            handle_request(client_sock, message)


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

    c1 = Players(name="Oscar Gluch", team="Rbz", league="Austria BL", national="Israel", position="CAM",
                 goals=6,
                 assists=4)
    db_session.add(c1)
    db_session.commit()

    db_session.add_all(
        [
            Players(name="Eran Zahavi", team="Maccabi Tel aviv", league="La liga", national="Israel", position="ST",
                    goals=15,
                    assists=4),
            Players(name="Dor Perez", team="Maccabi Tel aviv", league="La liga", national="Israel", position="CAM",
                    goals=2,
                    assists=3),
            Players(name="Lionel Messi", team="Paris Saint-Germain", league="Ligue 1", national="Argentina",
                    position="FW", goals=18, assists=8),
            Players(name="Cristiano Ronaldo", team="Manchester United", league="Premier League",
                    national="Portugal", position="FW", goals=13, assists=4),
            Players(name="Kylian Mbappe", team="Paris Saint-Germain", league="Ligue 1", national="France",
                    position="FW", goals=17, assists=8),
            Players(name="Robert Lewandowski", team="Bayern Munich", league="Bundesliga", national="Poland",
                    position="FW", goals=27, assists=6),
            Players(name="Erling Haaland", team="Borussia Dortmund", league="Bundesliga", national="Norway",
                    position="FW", goals=19, assists=5),
            Players(name="Kevin De Bruyne", team="Manchester City", league="Premier League", national="Belgium",
                    position="MF", goals=5, assists=11),
            Players(name="N'Golo Kante", team="Chelsea", league="Premier League", national="France",
                    position="MF", goals=1, assists=2),
            Players(name="Karim Benzema", team="Real Madrid", league="La Liga", national="France",
                    position="FW", goals=17, assists=7),
            Players(name="Mohamed Salah", team="Liverpool", league="Premier League", national="Egypt",
                    position="FW", goals=16, assists=4),
            Players(name="Sadio Mane", team="Liverpool", league="Premier League", national="Senegal",
                    position="FW", goals=8, assists=3),
            Players(name="Gareth Bale", team="Tottenham Hotspur", league="Premier League", national="Wales",
                    position="FW", goals=7, assists=2),
            Players(name="Son Heung-min", team="Tottenham Hotspur", league="Premier League",
                    national="South Korea", position="FW", goals=12, assists=5),
            Players(name="Virgil van Dijk", team="Liverpool", league="Premier League", national="Netherlands",
                    position="DF", goals=0, assists=0),
            Players(name="Ruben Dias", team="Manchester City", league="Premier League", national="Portugal",
                    position="DF", goals=1, assists=0),
            Players(name="Jan Oblak", team="Atletico Madrid", league="La Liga", national="France", position="GK",
                    goals=0, assists=0),

            Players(name="Serge Gnabry", team="Bayern Munich", league="Bundesliga", national="Germany", position="RW",
                    goals=5, assists=2),
            Players(name="Lautaro Martinez", team="Inter Milan", league="Serie A", national="Argentina", position="ST",
                    goals=13, assists=3),
            Players(name="Pierre-Emerick Aubameyang", team="Arsenal", league="Premier League", national="Gabon",
                    position="ST", goals=7, assists=1)

        ]
    )


def get_all():
    result = db_session.query(Players).all()
    return result


def insert_player(name, team, league, national, position, goals, assists):
    global db_session
    new_player = Players(name=name, team=team, league=league, national=national, position=position, goals=goals,
                         assists=assists)
    db_session.add(new_player)
    db_session.commit()
    print(f"Player {name} added to the database with ID {id}")


def delete_player_by_name(name):
    engine = create_engine('sqlite:///tcp.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    player = session.query(Players).filter_by(name=name).first()
    if player:
        session.delete(player)
        session.commit()
        print(f"Player {name} deleted successfully.")
    else:
        print(f"Player {name} not found in the database.")


# update the number of assists for the player
def update_player_goals(name, new_goals):
    global db_session
    player = db_session.query(Players).filter_by(name=name).first()
    if player:
        player.goals = new_goals
        db_session.commit()
        print(f"Goals for player {name} updated to {new_goals}")
    else:
        print(f"Player {name} not found in the database")


# update the number of asists for the player
def update_player_assists(name, new_assists):
    global db_session
    player = db_session.query(Players).filter_by(name=name).first()
    if player:
        player.assists = new_assists
        db_session.commit()
        print(f"Assists for player {name} updated to {new_assists}")
    else:
        print(f"Player {name} not found in the database")


# find player by id
def get_player_by_id(player_id):
    global db_session
    player = db_session.query(Players).filter_by(id=player_id).first()
    if player:
        print(f"Player {player.name} found in the database")
    else:
        print(f"Player with ID {player_id} not found in the database")
    return player


# check the current team of the player
def transfer_player(name, new_team):
    global db_session
    player = db_session.query(Players).filter_by(name=name).first()
    if player:
        player.team = new_team
        db_session.commit()
        print(f"Player {name} has been transferred to {new_team}")
    else:
        print(f"Player {name} not found in the database")


# return the number of the times that the player was invoved in goal
def get_goals_involvement(player1_id):
    player = get_player_by_id(player1_id)
    sum = player.goals + player.assists
    return sum


# return the full squad of every national team
def get_squad_national(national):
    global db_session
    players = db_session.query(Players).filter_by(national=national).all()
    return players


# return the full squad of every  team
def get_squad_team(team):
    global db_session
    players = db_session.query(Players).filter_by(team=team).all()
    return players


# chack if this two players  play together
def playing_together(player1_id, player2_id):
    player1 = get_player_by_id(player1_id)
    player2 = get_player_by_id(player2_id)
    if player1.team == player2.team:
        return True
    return False


def handle_request(client_sock, message):
    request = message.decode('utf-8').strip()
    # Get all players
    if request == "get_all_players":
        result = get_all()
        response = ""
        for player in result:
            response += str(player) + "\n"
        client_sock.send(response.encode())

    # Insert a new player
    elif request.startswith("insert_player"):
        try:
            _, name, team, league, national, position, goals, assists = request.split("-")
            print(name,team,league,national,position,goals,assists)
            insert_player(name, team, league, national, position, goals, assists)
            response = f"Player {name} added to the database with ID {id}"

        except:
            response = "Invalid input. Please provide all player details separated by -."
        client_sock.send(response.encode('utf-8'))

    # Delete a player by name
    elif request.startswith("delete_player"):
        try:
            _, name = request.split("-")
            delete_player_by_name(name)
            response = f"Player {name} deleted successfully."
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
            _, player1_id = request.split(" ")
            sum = get_goals_involvement(player1_id)
            response = f"Player with ID {player1_id} was involved in {sum} goals"
        except:
            response = "Invalid input. Please provide the ID of the player."
        client_sock.send(response.encode('utf-8'))
    elif request.startswith("get_squad_national"):
        try:
            _,nation = request.split("-")
            response = get_squad_national(nation)
        except:
            response="No such nation"
        client_sock.send(response.encode('utf-8'))
    elif request.startswith("get_squad_team"):
        try:
            _,team = request.split("-")
            response = get_squad_team(team)
        except:
            response="No such team"
        client_sock.send(response.encode('utf-8'))
    elif request.startswith("playing_together"):
        try:
            _,p1,p2 = request.split("-")
            response = playing_together(p1,p2)
        except:
            response="No such player"
        client_sock.send(response.encode('utf-8'))

if __name__ == '__main__':
    cdb()
    start_server()