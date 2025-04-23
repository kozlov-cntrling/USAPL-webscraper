import unittest
from unittest.mock import patch

class TestWebscraperDBSys(unittest.TestCase):
    def setUp(self):
        self.teams_inserted = {}

    @patch('builtins.print')
    def test_team_insert_new_team(self, mock_print):
        team_id = "123"
        team_name = "Team Alpha"
        if team_id not in self.teams_inserted:
            if team_id == "NULL":
                team_id = "NULL"
                team_name = "NULL"
            self.teams_inserted[team_id] = team_name
            team_insert = f"VALUES ({team_id}, '{team_name}')"
            if team_id != list(self.teams_inserted.keys())[-1]:
                team_insert += ","
            print(team_insert)

        mock_print.assert_called_once_with("VALUES (123, 'Team Alpha')")

    @patch('builtins.print')
    def test_team_insert_existing_team(self, mock_print):
        self.teams_inserted = {"123": "Team Alpha"}
        team_id = "123"
        team_name = "Team Alpha"
        if team_id not in self.teams_inserted:
            if team_id == "NULL":
                team_id = "NULL"
                team_name = "NULL"
            self.teams_inserted[team_id] = team_name
            team_insert = f"VALUES ({team_id}, '{team_name}')"
            if team_id != list(self.teams_inserted.keys())[-1]:
                team_insert += ","
            print(team_insert)

        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_team_insert_null_team(self, mock_print):
        team_id = "NULL"
        team_name = "NULL"
        if team_id not in self.teams_inserted:
            if team_id == "NULL":
                team_id = "NULL"
                team_name = "NULL"
            self.teams_inserted[team_id] = team_name
            team_insert = f"VALUES ({team_id}, '{team_name}')"
            if team_id != list(self.teams_inserted.keys())[-1]:
                team_insert += ","
            print(team_insert)

        mock_print.assert_called_once_with("VALUES (NULL, 'NULL')")

if __name__ == '__main__':
    unittest.main()