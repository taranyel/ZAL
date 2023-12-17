import random

class Dealer:

    def __init__(self):
        self.deck = [
            '♥A', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
            '♦A', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K',
            '♣A', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
            '♠A', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K'
        ]
        self.players = []

    def copy_deck(self, temp):
        for i in range(len(self.deck)):
            temp.append(self.deck[i])

    def exists(self, n):
        for i in self.deck:
            if i == n:
                return True
        return False

    def shuffle(self):
        if not self.deck:
            return

        temp = []
        self.copy_deck(temp)

        self.deck.clear()

        while temp:
            randomDigit = random.randint(0, len(temp) - 1)

            self.deck.append(temp[randomDigit])

            del temp[randomDigit]

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

        while self.deck and flag:
            flag = False
            for player in self.players:
                print(player.name + " hand: ", player.hand)
                if player.needs_card() and self.deck:
                    flag = True
                    if not stack:
                        stack = self.deal(len(self.players))

                    player.accept_card(stack[0])
                    del stack[0]
            print()

        winner = self.announce_winner()
        print()
        print(winner.name + " is winner!")
        print("His/her hand: ", winner.hand)

    def announce_winner(self):
        maximum = 0
        winner = None

        for player in self.players:
            summa = player.get_hand_value()
            if (summa > maximum) and (summa <= 21):
                maximum = summa
                winner = player
        return winner


class Player:

    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.hand = []

    def get_hand_value(self):
        summa = 0
        for card in self.hand:
            card = card[1:len(card)]
            try:
                digit = int(card)
                summa += digit
            except:
                if (card == 'J') or (card == 'Q') or (card == 'K'):
                    summa += 1
                elif card == 'A':
                    summa += 11
        return summa

    def needs_card(self):
        value = self.get_hand_value()
        if self.strategy == "Cautious" and value <= 10:
            return True
        elif self.strategy == "Bold" and value <= 15:
            return True
        elif self.strategy == 'Human':
            print("Add card? (Y/N)")
            response = input()
            if response == "Y":
                return True

        return False

    def accept_card(self, cards):
        self.hand.append(cards)


def validate_strategy(newStrategy):
    if (newStrategy != "Cautious") and (newStrategy != "Human") and (newStrategy != "Bold"):
        print("You enter was wrong! You can enter only 'Cautious', 'Human' or 'Bold' strategies!")
        return False
    return True


def validate_name(newName):
    if (len(newName) < 1) or (len(newName) > 50):
        print("You enter was wrong! Your name length must be between 1 and 50 characters!")
        return False
    return True


if __name__ == '__main__':
    dealer = Dealer()
    while True:
        print("Enter your command:")

        userInput = input()
        if userInput.lower() == "add player":

            while True:
                print("Enter player name:")
                player_name = input()
                if validate_name(player_name):
                    break

            while True:
                print("Enter player strategy:")
                player_strategy = input()
                if validate_strategy(player_strategy):
                    break

            new_player = Player(player_name, player_strategy)
            dealer.add_player(new_player)
            print("Player was successfully added!")
            print()

        elif userInput.lower() == "start game":
            if len(dealer.players) < 2:
                print("You can start game at least with two players!")
                print()
                continue

            print()
            dealer.shuffle()
            dealer.start_round()
            print()

        elif userInput.lower() == "exit":
            break
        else:
            print("Your command was wrong! You can enter only 'Add player', 'Start game', or 'Exit' commands!")
