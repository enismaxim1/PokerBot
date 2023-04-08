
import random
from network import Network
from player import Player
from poker_game_view import PokerGameView
from poker_ui import PokerUI
import threading

class PokerClient:

    def __init__(self, name, stack):
        self.network = Network()
        self.player = Player(name, stack, self.network.id)

    def run(self):
        self.ui = self.join_game()
        self.listener_thread = threading.Thread(target=self.listen_for_updates)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        self.ui.run()

    def join_game(self):
        reply = self.network.send({'join': Player.to_dict(self.player)})
        print("reply:", reply)
        return PokerUI(self.network, PokerGameView(reply))

    def listen_for_updates(self):
        while True:
            try:
                print("attempting to send data")
                update = self.network.receive()
                print('update:', update)
                print("response received!")
                self.ui.update_queue.put(PokerGameView(update))
            except Exception as e:
                print("Alert! Error receiving updates:", e)

client = PokerClient(str(random.randrange(100)), 2000)
client.run()