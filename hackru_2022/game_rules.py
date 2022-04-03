import time
import random
import socket
from _thread import *
import sys

tot_players = 0
members = []


def threaded_client(conn, addr):
  global tot_players, members
  conn.send(str.encode("Connected"))
  reply = ""
  while True:
      try:
          data = conn.recv(2048)
          reply = data.decode("utf-8")

          if not data:
              #print("Disconnected")
              tot_players -= 1
              temp = member(addr[0], 0, 0, addr[0], "motherfucker", ".0008", 0)
              #print(members)
              members.remove(temp)
              #print(members)
              break
          else:

              try:
                reply = reply.split(",")
                latitude = float(reply[0][2:-1])
                longitude = float(reply[1][2:-2])
                for i in range(len(members)):
                  if members[i].user_id == addr[0]:
                    members[i].latitude = latitude
                    members[i].longitude = longitude
                    members[i].disp()
                #print("Position {}, {} logged from {}".format(latitude, longitude, addr))
              except:
                pass
                #print("Loading location failed on {}".format(reply))

              #conn.sendall(str("zoinks scoob what a fucking stupid error the absense of this line caused"))
      except:
          break



  print("Lost connection")
  tot_players -= 1
  temp = member(addr[0], 0, 0, addr[0], "motherfucker", ".0008", 0)
  members.remove(temp)
  conn.close()

class member:

  def __init__(self, name, latitude, longitude, user_id, role, size, heading, game_id=0, won=False):
    self.name = name
    self.latitude = latitude
    self.longitude = longitude
    self.game_id = game_id
    self.user_id = user_id
    self.role = role
    self.size = size
    self.heading = heading
    self.won = won

  def __eq__(self, other):
    return self.user_id == other.user_id

  def disp(self):
    print(self.latitude, self.longitude)

def updatePlayerPositions():
  return

def run_game(game_id):
    GAME_LENGTH = 60*5
    print("started game")

    start_time = time.time()

    players = [player for player in members if game_id == player.game_id]
    
    num_hunters = len(players) // 5 + 1
    hunters = []
    for _ in range(num_hunters):
        hunters.append(players.pop(random.randint(0, len(players)-1)))
        hunters[-1].role = "Hunter"

    for player in players:
      player.role = "Hunter" if player in hunters else "Hider"

    hiders = [player for player in players if "Hider" == player.role]
    current_time = int(time.time() - start_time)

    print("Hiders : {}".format([hider.name for hider in hiders]))
    print("Hunter : {}".format([hunter.name for hunter in hunters]))

    #While time is still on the clock and players are still hiding
    while len(hiders) > 0 and current_time // GAME_LENGTH == 0:

        #Update time
        current_time = int(time.time() - start_time)

        #Check if hiders have been found
        for hunter in hunters:
          for hider in hiders:
              if hunter.latitude <= hider.latitude <= hunter.latitude + .00005 and hunter.longitude <= hider.longitude <= hunter.longitude + .00005:
                hider.role = "Hunter"
              if hider.latitude <= hunter.latitude <= hider.latitude + .00005 and hider.longitude <= hunter.longitude <= hider.longitude + .00005:
                hider.role = "Hunter"

        players = hiders + hunters
        hiders = [player for player in players if "Hider" == player.role]
        hunters = [player for player in players if "Hunter" == player.role]
    

    #Game has ended.
    if len(hiders) == 0:
        #Hunters Won
        print("Hunters Won!")
        pass
    else:
        print("Hiders Won")
        pass  
        #Hiders Won

    for player in players:
        player.role = "motherfucker"


    print("ended game")


if __name__ == "__main__":

  server = "172.31.39.100"
  port = 5555

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
      s.bind((server, port))
  except socket.error as e:
      str(e)

  s.listen(2)
  print("Waiting for a connection, Server Started")

  while True:
      conn, addr = s.accept()
      print("Connected to:", addr)
      tot_players += 1

      mem = member(addr[0], 0, 0, addr[0], "motherfucker", ".0008", 0)
      members.append(mem)

      start_new_thread(threaded_client, (conn,addr,))
      if tot_players % 3 == 0:
        start_new_thread(run_game, (0,))