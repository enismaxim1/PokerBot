import json
import socket
from _thread import *
import sys
import uuid
from player import Player
from time import time
from poker_game import Era, PokerGame

IP = '127.0.0.1'
PORT = 5555
COOLDOWN_MAP = {Era.WAITING: 0, Era.BEGINNING: 1.5, Era.PREFLOP: 1, Era.FLOP: 2, Era.TURN: 2, Era.RIVER: 2, Era.PAYOUT: 2}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((IP, PORT))
except socket.error as e:
    str(e)

s.listen(10)
print("Waiting for a connection, Server Started")

poker_game = PokerGame([], 5, 10)
print("Poker game created")

def game_progression():
    last = time()
    while True:
        if poker_game.action_finished and len(poker_game.players) > 1:
            now = time()
            if now - last > COOLDOWN_MAP[poker_game.current_era]:
                last = now
                print(f"Moving to next era from {poker_game.current_era}")
                poker_game.next_action()
                for conn, client_id in clients:
                    print("sending data")
                    conn.sendall((poker_game.get_game_state(client_id)).encode())

def threaded_client(conn, client_id):
    conn.send(json.dumps(client_id).encode())
    reply = ""

    while True:
        try:
            data = conn.recv(20000)
            if not data:
                print("Disconnected")
                break

            # print("Received data:", data)
            # decoded_data = json.loads(data.decode("utf-8"))
            # print("Decoded data:", decoded_data)
            print(data)
            reply = poker_game.process_client_input(client_id, data)
            encoded_reply = reply.encode()
            conn.sendall(encoded_reply)
        except Exception as e:
            print("Error:", e)
            break

        except:
            break

    print("Lost connection")
    conn.close()

clients = []
start_new_thread(game_progression, ())
while True:
    conn, addr = s.accept()
    client_id = str(uuid.uuid4())
    print("Connected to:", addr)
    clients.append((conn, client_id))
    start_new_thread(threaded_client, (conn, client_id))