#Lay out the type of suits and names of poker cards
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
names = ['Two', 'Three', 'Four', 'Five', 'Six','Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four': 4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen': 10, 'King':10, 'Ace':11}
import random
playing = True

#create the card class for an individual poker card
class Card:
    def __init__(self, suit, name):
        self.suit = suit
        self.name = name

    def __repr__(self):
        return self.name + ' of ' + self.suit

#create a deck class for an individual deck of cards
class Deck:
    #create a standard deck of cards
    deck = []
    def __init__(self):
        for suit in suits:
            for name in names:
               self.deck.append(Card(suit, name))

    def __repr__(self):
        deck_content = ''
        for card in self.deck:
            deck_content+= card.name + ' of '+card.suit+'\n'
        return deck_content


    #shuffle the sequence of the cards
    def shuffle(self):
        random.shuffle(self.deck)

    #deal a card from the deck
    def deal(self):
        card_drawn = self.deck.pop()
        return card_drawn

#create a class for a hand that is going to be held by the player or the computer
class Hand:
    #cretae a hand list that will containt the cards dealt to players
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    #when a card added to the hand, append the list, and adjust the value of the hand
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.name]
        if card.name == 'Ace':
            self.aces +=1

    #when value blow up, count Ace's value as 1 instead of 11
    def ace_adjust(self):
        if self.value >21 and self.aces:
            self.value -= 10
            self.aces -= 1

#create a chip class to keep track of chips for the player and how much was bet with each round of game
class Chips:
    #create the total chips varaible and bet chips variable
    def __init__(self):
        self.total = 100
        self.bet = 0
    
    # add bet chips to total when win
    def win_bet(self):
        self.total += self.bet

    # deduct bet chips to total when lost
    def lose_bet(self):
        self.total -= self.bet

#cretae a function to take in player's bet
def take_bet(chips, player_name):
    while True:
        try:
            chips.bet = int(input('{}, please input how many chips you would like to bet in this round? '.format(player_name)))
        except ValueError:
            print('You must enter an integer value!')
        else:
            if chips.bet > chips.total:
                print('You can not excced the maximum chip on hand: '+ str(chips.total) +'!')
            else:
                break

#create a function to hit a card

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.ace_adjust()

#create a function to determine whether hit or stand
def hit_or_stand(deck, hand):
    global playing
    while True:
        h_or_s = input('\nPlease enter h for hit and s for stand: ')

        if h_or_s[0].lower() == 'h':
            hit(deck, hand)

        elif h_or_s[0].lower() == 's':
            print("Player stands. Dealer's turn")
            playing = False
                
        else:
            print('Please enter h or s to hit or stand.')
            continue
        break

#create a function to display hand of each player with dealer's first card hidden
def display_hand_start(player_hand,dealer_hand):
    print("\nDealer's hand:")
    print('<Hidden Card for dealer>')
    print(dealer_hand.cards[1])
    print("\nPlayer's hand:", *player_hand.cards, sep = '\n')

#create a function to display hand of each player with all cards revealed
def display_hand_end(player_hand, dealer_hand):
    print("Dealer's hand:", *dealer_hand.cards, sep = '\n')
    print("Dealer's hand total is", dealer_hand.value)
    print("\nPlayer's hand:", *player_hand.cards, sep = '\n')
    print("Player's hand total is", player_hand.value)
    
#create five functions to process chips for each of the five scenarios:
def player_busts(chips):
    print('\nPlayer busts!')
    chips.lose_bet()

def dealer_busts(chips):
    print('\nDealer busts!')
    chips.win_bet()

def player_wins(chips):
    print('\nPlayer wins!')
    chips.win_bet()

def dealer_wins(chips):
    print('\nDealer wins!')
    chips.lose_bet()

def ties():
    print('Player and dealer ties!')

#Body of the Game Execution
#Game introduction
print('Welcome to the BlackJack Game!')
print('Get to 21 as close as possible without going over!\nDealer hits once reaches 17.\nAce count as 1 or 11.')
player = input('Please enter your name: ')

#set up the deck and deal two cards to each of player and dealer
game_deck = Deck()
game_deck.shuffle()

player_hand = Hand()
player_hand.add_card(game_deck.deal())
player_hand.add_card(game_deck.deal())

dealer_hand = Hand()
dealer_hand.add_card(game_deck.deal())
dealer_hand.add_card(game_deck.deal())

#let player bet chips to the round and display the cards for both player and dealer with dealer's first card hidden.
player_chips = Chips()
take_bet(player_chips, player)

display_hand_start(player_hand, dealer_hand)

while True:
#Ask player hit or stand and display the cards after the hit_or_stand execution, until player stands or player busts.
    while playing:
        hit_or_stand(game_deck, player_hand)
        display_hand_start(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_chips)
            break

#let the dealer hit until it goes to 17, and determine other outcomes of the game.
    if player_hand.value <=21:
        while dealer_hand.value <17:
            hit(game_deck,dealer_hand)
        print('\n')
        display_hand_end(player_hand, dealer_hand)
        if dealer_hand.value >21:
            dealer_busts(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value == player_hand.value:
            ties()

    print(player,', your remaining chips is: ',player_chips.total)

    #Ask the player to play again.
    game_again = input('Do you want to play the game again? Enter Y to play again. ')

    if game_again[0].lower() == 'y':
        playing = True
        continue

    else: 
        print('Thanks for playing!')
        break
        













