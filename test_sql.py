import unittest

from tcp_server import cdb, insert_player


class MyTestCase(unittest.TestCase):
    db_session = None

    def setUp(self):
        global db_session
        db_session = cdb()

    def tearDown(self):
        global db_session
        db_session.close()

    def test_insert_player(self):
        player = insert_player(name="Ruben Dias", team="Manchester City", league="Premier League", national="Portugal",
                    position="DEF", goals=1, assists=0)
        self.assertEqual(player.name, 'Ruben Dias')
        self.assertEqual(player.team,'Manchester City')
        self.assertEqual(player.league,'Premier League')


if __name__ == '__main__':
    unittest.main()
