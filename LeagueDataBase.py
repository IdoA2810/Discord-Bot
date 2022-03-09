import sqlite3
import csv

class ORM():
    def __init__(self):
        self.conn = None  # will store the DB connection
        #self.cursor = None   # will store the DB connection cursor
        self.current = None
    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('LeagueOfLegendsDB.db')
        self.current = self.conn.cursor()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_tables(self):

        self.open_DB()
        sql = "CREATE TABLE groups_stage (Team, Player, Opponent, Position, Champion, Kills, Deaths, Assists, 'Creep Score', " \
              "'Gold Earned', 'Champion Damage Share', 'Kill Participation', 'Wards Placed', 'Wards Destroyed', 'Ward Interactions', " \
              "'Dragons For', 'Dragons Against', 'Barons For', 'Barons Against', Result);"

        self.current.execute(sql)  # use your column names here

        with open('League_of_Legends_2021_World_Championship_Play-In_Groups_Statistics_-_Raw_Data.csv','r') as fin: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin) # comma is default delimiter
            to_db = [(i['Team'], i['Player'], i['Opponent'], i['Position'], i['Champion'], i['Kills'], i['Deaths'], i['Assists'],
                      i['Creep Score'], i['Gold Earned'], i['Champion Damage Share'], i['Kill Participation'], i['Wards Placed'],
                      i['Wards Destroyed'], i['Ward Interactions'], i['Dragons For'], i['Dragons Against'], i['Barons For'], i['Barons Against'], i['Result']) for i in dr]

        sql = "INSERT INTO groups_stage (Team, Player, Opponent, Position, Champion, Kills, Deaths, Assists, 'Creep Score', " \
              "'Gold Earned', 'Champion Damage Share', 'Kill Participation', 'Wards Placed', 'Wards Destroyed', 'Ward Interactions', " \
              "'Dragons For', 'Dragons Against', 'Barons For', 'Barons Against', Result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        self.current.executemany(sql, to_db)
        self.commit()
        self.close_DB()

    def get_all(self):
        self.open_DB()
        sql = "SELECT * FROM groups_stage"
        res = self.current.execute(sql)
        '''table = "(Team, Player, Opponent, Position, Champion, Kills, Deaths, Assists, Creep Score, " \
              "Gold Earned, Champion Damage Share, Kill Participation, Wards Placed, Wards Destroyed, Ward Interactions, " \
              "Dragons For, Dragons Against, Barons For, Barons Against, Result)\n"'''
        table = ""
        for ans in res:
            table += str(ans) + "\n"
        self.close_DB()
        return table

    def get_team(self, team):
        self.open_DB()
        sql = "SELECT * FROM groups_stage WHERE Team = '"+team+"'"
        res = self.current.execute(sql)
        table = ""
        for ans in res:
            table += str(ans) + "\n"
        self.close_DB()
        return table

    def get_player(self, player):
        self.open_DB()
        sql = "SELECT * FROM groups_stage WHERE Player = '"+player+"'"
        res = self.current.execute(sql)
        table = ""
        for ans in res:
            table += str(ans) + "\n"
        self.close_DB()
        return table


def main_test():
    ORM().create_tables()
    ORM().stam()



if __name__ == "__main__":
    main_test()