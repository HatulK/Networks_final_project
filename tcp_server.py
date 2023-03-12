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

# Define a function named "cdb"
def cdb():
    # Use the global keyword to reference the global variable "db_session"
    global db_session
    # Create a database engine and connect to the database "tcp.db"
    engine = create_engine('sqlite:///tcp.db', echo=False)
    # Create all the tables defined in the Base class, if they don't already exist
    Base.metadata.create_all(engine)
    # Create a session object that will be used to interact with the database
    session = sessionmaker(bind=engine)
    db_session = session()

    db_session.query(Players).delete()
    # Create a new player record and add it to the "Players" table
    c1 = Players(name="Oscar Gluch", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                 goals=6,
                 assists=4)
    db_session.add(c1)
    # Commit the changes made to the "Players" table
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

# Insert a new player into the database
def insert_player(name, team, league, national, position, goals, assists):
    global db_session
    new_player = Players(name=name, team=team, league=league, national=national, position=position, goals=goals,
                         assists=assists)
    db_session.add(new_player)
    db_session.commit()
    print(f"Player {name} added to the database")
    return new_player

# Delete a player from the database by their name
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
        print(f"Player {player.name} found in the database\n")
        return player
    else:
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
        return f"Player do not exist."


# return the number of the times that the player was involved in goal
def get_goals_involvement(name):
    global db_session
    player = db_session.query(Players).filter(Players.name.like(f'{name}%')).first()
    if player:
        sum = player.goals + player.assists
        return sum
    else:
        return "Player not exist."


# return the full squad of every national team
def get_squad_national(national):
    global db_session
    players = db_session.query(Players).filter(Players.national.like(f'{national}%')).all()
    if players:
        return players
    else:
        return "Nation not exist"


# return the full squad of every  team
def get_squad_team(team):
    global db_session
    players = db_session.query(Players).filter(Players.team.like(f'{team}%')).all()
    if players:
        return players
    else:
        return "Team not exist"


# chack if this two players  play together
def playing_together(p1, p2):
    player1=player = db_session.query(Players).filter(Players.name.like(f'{p1}%')).first()
    player2 = player = db_session.query(Players).filter(Players.name.like(f'{p2}%')).first()
    if player1 and player2:
        if player1.team == player2.team:
            return "They are playing together\n"
        return "They are not playing together\n"
    else:
        return "Player 1 or/and 2 do not exist."

# This function returns all the players in the database who play in a certain position
def get_all_players_by_position(position):
    global db_session
    players = db_session.query(Players).filter(Players.position.like(f'{position}%')).all()
    if players:
        return players
    else:
        return "There is no such position"

# This function returns all the players in the database who have scored more than a certain number of goals
def get_players_by_goals(number):
    global db_session
    players = db_session.query(Players).filter(Players.goals>=number).all()
    if players:
        return players
    else:
        return None


def handle_request(client_sock):
    while True:
        message = client_sock.recv(buffer)
        print(message.decode())
        request = message.decode('utf-8').strip()
        # Get all players
        if request == "get_all_players":
            result = get_all()
            response1 = ""
            for player in result:
                response1 += str(player)
            client_sock.send(response1.encode())
        # Insert a new player
        elif request.startswith("insert_player"):
            try:
                _, name, team, league, national, position, goals, assists = request.split("-")
                response2 = insert_player(name, team, league, national, position, goals, assists)
                response2=response2.__str__()
            except:
                response2 = "Invalid input. Please provide all player details separated by -."
            client_sock.send(response2.encode('utf-8'))
        # Delete a player by name
        elif request.startswith("delete_player"):
            try:
                _, name = request.split("-")
                response3 = delete_player_by_name(name)
            except:
                response3 = "Invalid input. Please provide the name of the player to delete."
            client_sock.send(response3.encode('utf-8'))
        # Update player's goals
        elif request.startswith("update_goals"):
            try:
                _, name, new_goals = request.split("-")

                response4 =update_player_goals(name, new_goals)
            except:
                response4 = "Invalid input. Please provide the name of the player and the new number of goals."
            client_sock.send(response4.encode('utf-8'))
        # Update player's assists
        elif request.startswith("update_assists"):
            try:
                _, name, new_assists = request.split("-")
                response5 = update_player_assists(name, new_assists)
            except:
                response5 = "Invalid input. Please provide the name of the player and the new number of assists."
            client_sock.send(response5.encode('utf-8'))
        # Find player by ID
        elif request.startswith("find_player"):
            try:
                _, player_id = request.split("-")
                player = get_player_by_id(player_id)
                if player:
                    response6 = f"Player {player.name} found in the database"
                else:
                    response6 = f"Player with ID {player_id} not found in the database"
            except:
                response6 = "Invalid input. Please provide the ID of the player to find."
            client_sock.send(response6.encode('utf-8'))
        # Transfer player to new team
        elif request.startswith("transfer_player"):
            try:
                _, name, new_team = request.split("-")
                response7 = transfer_player(name, new_team)
            except:
                response7 = "Invalid input. Please provide the name of the player and the name of the new team."
            client_sock.send(response7.encode('utf-8'))
        # Get total goals involvement of a player
        elif request.startswith("goals_involvement"):
            try:
                _, name = request.split("-")
                sum = get_goals_involvement(name)
                response8 = f"{name} is involved in {sum} goals"
            except:
                response8 = "Invalid input. Please provide the ID of the player."
            client_sock.send(response8.encode('utf-8'))
        #Get all players belong to this national
        elif request.startswith("get_squad_national"):
            response9=None
            try:
                _,nation = request.split("-")
                result = get_squad_national(nation)
                if result=="Nation not exist":
                    result=result+"\n"
                    client_sock.send(result.encode('utf-8'))
                else:
                    response9 = ""
                    for player in result:
                        response9 += str(player) + "\n"
            except:
                response9="No such nation"
            if response9:
                client_sock.send(response9.encode('utf-8'))
        #Get all players from the team
        elif request.startswith("get_squad_team"):
            response10=None
            try:
                _,team = request.split("-")
                result = get_squad_team(team)
                if result=="Team not exist":
                    client_sock.send(result.encode('utf-8'))
                else:
                    response10 = ""
                    for player in result:
                        response10 += str(player) + "\n"
            except:
                response10="No such team"
            if response10:
                client_sock.send(response10.encode('utf-8'))
        #Check if two players playing in the same team
        elif request.startswith("playing_together"):
            try:
                _,p1,p2 = request.split("-")
                response11 = playing_together(p1,p2)
            except:
                response11="No such player\s"
            client_sock.send(response11.encode('utf-8'))
        #Get all players by position
        elif request.startswith("get_all_players_by_position"):
            response12=None
            try:
                _, pos = request.split("-")
                result = get_all_players_by_position(pos)
                if result=="There is no such position":
                    client_sock.send(result.encode('utf-8'))
                else:
                    response12 = ""
                    for player in result:
                        response12 += str(player) + "\n"
            except:
                response12 = "No such position"
            if response12:
                client_sock.send(response12.encode('utf-8'))
        #Get all players with more than X goals.
        elif request.startswith("get_players_by_goals"):
            try:
                _, num = request.split("-")
                result = get_players_by_goals(num)
                if result:
                    response13 = ""
                    for player in result:
                        response13 += str(player) + "\n"
                else:
                    response13 = "No such players"
            except:
                response13 = "No such players"
            client_sock.send(response13.encode('utf-8'))
        elif request.startswith("exit"):
            print("TCP Server is disconnecting from the client")
            client_sock.close()
            break

if __name__ == '__main__':
    cdb()
    start_server()