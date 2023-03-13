import unittest
from tcp_server import *


class MyTestCase(unittest.TestCase):
    db_session = None

    def setUp(self):
        global db_session
        db_session = cdb()

    def tearDown(self):
        global db_session
        db_session.rollback()
        db_session.close()

    def test_insert_player(self):
        player = insert_player(name="Oscar Gluch", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                 goals=6,
                 assists=4)
        self.assertEqual(player.name,"Oscar Gluch")
        self.assertEqual(player.team, "Rbz")
        self.assertEqual(player.league, "Austria BL")
        self.assertEqual(player.national, "Israel")
        self.assertEqual(player.position,"ATT")
        self.assertEqual(player.assists,4)
        self.assertEqual(player.goals,6)

    def test_delete_player(self):
        player = insert_player(name="Oscar Gluch1", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        x=delete_player_by_name("Oscar Gluch1")
        y=delete_player_by_name("Hatul")
        self.assertEqual(x,f"Player {player.name} deleted successfully.\n")
        self.assertEqual(y,"Player not found in the database.\n")


    def test_update_player_goals(self):
        player = insert_player(name="Oscar Gluch2", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        x=update_player_goals("Oscar Gluch2",1000)
        y=update_player_goals("Amit Kabalo",1000)
        self.assertEqual(x,f"Goals for player Oscar Gluch2 updated to 1000")
        self.assertEqual(y,"Player Amit Kabalo not found in the database")

    def test_update_player_assists(self):
        player = insert_player(name="Oscar Gluch3", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        x=update_player_assists("Oscar Gluch3",1000)
        y=update_player_assists("Amit Kabalo",1000)
        self.assertEqual(x,"Assists for player Oscar Gluch3 updated to 1000")
        self.assertEqual(y,"Player Amit Kabalo not found in the database")


    def test_get_player_by_id(self):
        db_session.query(Players).delete()
        player = insert_player(name="Oscar Gluch1", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        x=get_player_by_id(1)
        y=get_player_by_id(1000)
        self.assertEqual(x,player)
        self.assertEqual(y,None)

    def test_transfer_player(self):
        player = insert_player(name="Oscar Gluch10", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        x=transfer_player("Oscar Gluch10","Real Madrid")
        y=transfer_player("Ori","Afula")
        self.assertEqual(x,f"Player {player.name} has been transferred to Real Madrid")
        self.assertEqual(y,"Player do not exist.")

    def test_get_goals_involvement(self):
        player = insert_player(name="Oscar Gluch11", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        x=get_goals_involvement("Oscar Gluch11")
        y=get_goals_involvement("Bla Bli Blu")
        self.assertEqual(x,10)
        self.assertEqual(y,"Player not exist.")

    def test_get_squad_national(self):
        player = insert_player(name="Oscar Gluch12", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        israel=db_session.query(Players).filter(Players.national.like("Israel")).all()
        x=get_squad_national("Israel")
        y=get_squad_national("Hawaii")
        self.assertEqual(x,israel)
        self.assertEqual(y,"Nation not exist")

    def test_get_squad_team(self):
        player = insert_player(name="Oscar Gluch12", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        rbz = db_session.query(Players).filter(Players.team.like("Rbz")).all()
        x=get_squad_team("Rbz")
        y=get_squad_team("ASDFASDFASDFASDF")
        self.assertEqual(x,rbz)
        self.assertEqual(y,"Team not exist")

    def test_playing_together(self):
        player1 = insert_player(name="Oscar Gluch13", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        player2 = insert_player(name="Ori Cohen", team="Rbz", league="Austria BL", national="Israel", position="ATT",
                               goals=6,
                               assists=4)
        player3 = insert_player(name="Hole al", team="Dimona", league="Austria BL", national="Israel", position="ATT",
                                goals=6,
                                assists=4)

        x=playing_together(player2.name,player1.name)
        y=playing_together(player2.name,"Lev Levayev")
        z=playing_together(player2.name,player3.name)
        self.assertEqual(x,"They are playing together\n")
        self.assertEqual(y,"Player 1 or/and 2 do not exist.")
        self.assertEqual(z,"They are not playing together\n")

    def test_get_players_by_goals(self):
        player1 = insert_player(name="Oscar Gluch18", team="Rbz", league="Austria BL", national="Israel",
                                position="ATT",
                                goals=1000,
                                assists=4)
        players = db_session.query(Players).filter(Players.goals >= 999).all()
        x=get_players_by_goals(999)
        y=get_players_by_goals(100000000000)
        self.assertEqual(players,x)
        self.assertEqual(y,None)

    def test_get_all_players_by_position(self):
        player1 = insert_player(name="Oscar Gluch18", team="Rbz", league="Austria BL", national="Israel",
                                position="ATT",
                                goals=1000,
                                assists=4)
        players = db_session.query(Players).filter(Players.position.like("ATT")).all()
        x=get_all_players_by_position("ATT")
        y=get_all_players_by_position("ASDFASDF")
        self.assertEqual(x,players)
        self.assertEqual(y,"There is no such position")


if __name__ == '__main__':
    unittest.main()
