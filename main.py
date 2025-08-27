import random


def deal(deck, list_, dict_):
    for player in list_:
        hand = [random.choice(deck), random.choice(deck)]
        dict_[player] = hand


def play(c, h, d, u, d2, b_l):
    global go_on
    global bets
    if c == "stay":
        go_on = True
    elif c == "pull":
        h.append(random.choice(d))
        print(h)
    elif c == "double":
        if d2:
            bets[u] *= 2
            h.append(random.choice(d))
            print(h)
            go_on = True
        else:
            c2 = input("Sorry, you don't have enough money to double, please make another choice: ")
            play(c2, h, d, u, d2, b_l)
    elif c == "split":
        return
    elif c == "bank":
        print(b_l[u])
    else:
        c3 = input("You made an invalid comment, please try again: ")
        play(c3, h, d, u, d2, b_l)


def check_21(hand):
    total = 0
    ace = 0
    for i in hand:
        total += i
        if i == 11:
            ace += 1
    if total > 21 and ace == 0:
        return False
    elif total > 21 and ace > 0:
        while not ace == 0:
            for i in hand:
                if i == 11:
                    hand.remove(i)
                    hand.append(1)
                    ace -= 1
                    total_2 = 0
                    for j in hand:
                        total_2 += j
                    if total_2 <= 21:
                        return True
        total_3 = 0
        for i in hand:
            total_3 += i
        if total_3 <= 21:
            return True
    else:
        return True


def bet(account, u):
    b = 0
    global double
    checkpoint = False
    while not checkpoint:
        b = int(input(f"How much you want to bet {u}: "))
        if account < b:
            print(f"You can't bet that much, you only have {account}")
        elif b * 2 <= account:
            double = True
            checkpoint = True
        else:
            checkpoint = True
    return b


def compare(h, ch):
    users_total = 0
    computers_total = 0
    for i in h:
        users_total += i
    for i in ch:
        computers_total += i
    if computers_total < users_total < 22 or users_total < 22 < computers_total:
        return "win"
    elif users_total == computers_total and users_total < 22:
        return "draw"
    else:
        return "lose"


def check_16(comp_hand, deck):
    total = 0
    for i in comp_hand:
        total += i
    while total < 17:
        a = random.choice(deck)
        comp_hand.append(a)
        total += a
    check_21(comp_hand)


def blackjack(hand):
    if len(hand) != 2:
        return False
    else:
        if hand[0] != 10 and hand[1] != 10:
            return False
        elif hand[0] != 11 and hand[1] != 11:
            return False
        else:
            return True


the_deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

the_game_is_on = True

print("Welcome to the Blackjack Game!\n")
user_number = int(input("How many players are going to play: "))
user_list = []

for user in range(user_number):
    user_x = user + 1
    user_list.append(f"player_{user_x}")

bank = {}
for user in user_list:
    bank[user] = 100


print("Each player will start with 100 dollars cash.")
while the_game_is_on:

    hands = {}
    bets = {}
    computers_hand = [random.choice(the_deck), random.choice(the_deck)]
    deal(the_deck, user_list, hands)
    print(f"Computer's first card is; {computers_hand[0]}")

    for user in hands:
        go_on = False
        double = False
        bets[user] = bet(bank[user], user)
        while not go_on:
            print(f"{user} your cards are; {hands[user]}")
            command = input("Please write one of the following commands: 'Stay', 'Pull', 'Double', 'Split'\n\n").lower()
            if blackjack(hands[user]):
                print("Wow, you have a blackjack!")
                bets[user] *= 1.5
            else:
                play(command, hands[user], the_deck, user, double, bets)
            if not check_21(hands[user]):
                print(f"{hands[user]}\nYour hand is over 21! You lost this round.")
                bank[user] -= bets[user]
                go_on = True

    print(f"\nComputer's hand is: {computers_hand}")
    if not check_16(computers_hand, the_deck):
        print("Oops, computer's hand is over 21!")
    for user in hands:
        if compare(hands[user], computers_hand) == "win":
            print(f"{user} you have won this round.")
            bank[user] += bets[user]
        elif compare(hands[user], computers_hand) == "draw":
            print(f"{user} you have drawn this round.")
        else:
            print(f"{user} you have lost this round")
            if check_21(hands[user]):
                bank[user] -= bets[user]
            if bank[user] == 0:
                print("Unfortunately you have lost all of your money, maybe this time you learn gambling is bad.")
                del bank[user]
                user_list.remove(user)
