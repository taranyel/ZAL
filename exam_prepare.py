import random
from enum import Enum


class Strategy(Enum):
    CAUTIOUS = 'Cautious'
    BOLD = 'Bold'
    HUMAN = 'Human'


class Dealer:

    def __init__(self):
        self.deck = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        self.values = [7, 8, 9, 10, 1, 1, 1, 11]
        self.players = []

    def copy_deck(self, temp, tempValues):
        for i in range(len(self.deck)):
            temp.append(self.deck[i])
            tempValues.append(self.values[i])

    def exists(self, n):
        for i in self.deck:
            if i == n:
                return True
        return False

    def shuffle(self):
        if not self.deck:
            return

        temp = []
        tempValues = []
        self.copy_deck(temp, tempValues)

        self.deck.clear()
        self.values.clear()

        i = 0
        while i < len(temp):
            randomDigit = random.randint(0, len(temp) - 1)

            if not self.exists(temp[randomDigit]):
                self.deck.append(temp[randomDigit])
                self.values.append(tempValues[randomDigit])
                i += 1
            else:
                continue

    def deal(self, n):
        if not self.deck:
            return []

        result = []
        i = 0

        while self.deck and i < n:
            result.append(self.deck[0])
            del self.deck[0]
            i += 1
        return result

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        for i in self.players:
            if i == player:
                del i
                return

    def start_round(self):
        stack = self.deal(len(self.players))

        for player in self.players:
            player.accept_card(stack[0])
            del stack[0]

        flag = True

        while flag:
            for player in self.players:
                if player.needs_card() and self.deck:
                    flag = True
                    if not stack:
                        stack = self.deal(len(self.players))

                    player.accept_card(stack[0])
                    del stack[0]
                else:
                    flag = False

        print(self.announce_winner().name + "is winner!")

    def announce_winner(self):
        maximum = 0
        winner = None

        for player in self.players:
            if (player.get_hand_value() > maximum) and (player.get_hand_value() < 21):
                maximum = player.get_hand_value
                winner = player
        return winner


class Player:

    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.hand = []
        self.handValues = []

    def get_hand_value(self):
        summa = 0
        for i in self.handValues:
            summa += i
        return summa

    def needs_card(self):
        if self.strategy == "Cautious" and self.get_hand_value() <= 10:
            return True
        elif self.strategy == "Bold" and self.get_hand_value() <= 15:
            return True
        else:
            print()
            print(self.name + " cards")
            print(self.hand)
            print("next? (Y/N)")
            response = input()
            if response == "Y":
                return True

        return False

    def accept_card(self, cards):
        self.hand.append(cards)
        print(self.name + " hand:")
        print(self.hand)


dealer = Dealer()
player1 = Player('Liza', 'Human')
player2 = Player('Maxim', 'Cautious')
player3 = Player('Lena', 'Bold')
dealer.add_player(player1)
dealer.add_player(player2)
dealer.add_player(player3)
dealer.shuffle()
dealer.start_round()