import random
import json
import time

bank_account = {
    "bucks": 0,
    "coins": 0,
    "limecoins": 0
}

def save_game(sv_fname):
    json.dump(bank_account, open(sv_fname,"w"))
    print(f"💾 Game was saved")

def load_game(ld_fname):
    print(f"💿 Game Loaded")
    return json.load(open(ld_fname,"r"))

def clearscr():
    #print(chr(27) + "[2J")
    print()
    print()

def header(bank):
    print(f"Bank: ${bank['bucks']} / {bank['coins']} Coins / {bank['limecoins']} Limecoins")

def select_bet(bank):
    while 1:
        print(random.choice(["Cmon, place ya bets","Care to make a wager?"]))
        bet_type = False
        print(f"1. 💵 Use Bucks (${bank['bucks']})")
        print(f"2. 🔘 Use Coins ({bank['coins']} Coins)")
        print(f"3. 🟡 Use Limecoins ({bank['limecoins']})")
        print("4. ❌ Cancel Bet")
        try:
            bet_select = int(input("Bet with? "))
            if bet_select in range(1,5):
                if bet_select == 1:
                    if bank['bucks'] <= 0:
                        print(f"You dont got enough dosh.")
                        continue
                    else:
                        print(f"Alright, your using cold cash, the good stuff.")
                        bet_type = "bucks"
                elif bet_select == 2:
                    if bank['coins'] <= 0:
                        print(f"Not enough coins...")
                        
                    else:
                        print(f"Using coins, good at any casino")
                        bet_type = "coins"
                elif bet_select == 3:
                    if bank['limecoins'] <= 0:
                        print(f"Get more limecoin, and come back")
                        
                    else:
                        print("Limecoins, only good here.")
                        bet_type = "limecoins"
                elif bet_select == 4:
                    return False
        except KeyboardInterrupt:
            return False
        try:
            while 1:
                amt = int(input(f"How much {bet_type} you wanna wager? "))
                if int(bank[bet_type]) >= amt:
                    print(f"Alright thats {amt} {bet_type}")
                    return (bet_type, amt)
                else:
                    continue
        except KeyboardInterrupt:
            return False


def explore(bank):
    while 1:
        print("You explore around")
        print("1. Beg on the streets")
        print("2. Walk around")
        print("3. Go Back")
        sel = int(input("?"))
        if sel in range(1,4):
            if sel == 1:
                print("You beg")
                beg_chance = random.randint(1,6)
                if beg_chance >= 4:
                    r_ammount = random.randint(1,10)
                    print(f"A kind stranger hands you {r_ammount} coins")
                    bank['coins'] += r_ammount
                else:
                    print(f"Many pass by, but nobody gives you anything")
            elif sel == 2:
                print("You wander around...")
            elif sel == 3:
                break

def get_value(item):
        if item == 'A':
            return 20
        elif item == 'J':
            return 19
        elif item == 'K':
            return 18
        elif item == 'Q':
            return 17
        elif item == '#':
            return 25
        elif item == '%':
            return 30
        elif item == '&':
            return 35
        else:
            return int(item)



def slots(bank):
    while 1:
        if bank['bucks'] > 0 or bank['coins'] > 0 or bank['limecoins'] > 0:
            my_bet = select_bet(bank)
            if my_bet:
                if my_bet[0] == "bucks":
                    print(f"You wagered ${my_bet[1]}")
                elif my_bet[0] == "coins":
                    print(f"You wagered {my_bet[1]} Coins")
                elif my_bet[0] == "limecoins":
                    print(f"You wagered {my_bet[1]} Limecoins")
            else:
                break
            bank[my_bet[0]] -= my_bet[1]
            roll = "1,2,3,4,5,6,7,8,9,A,J,K,Q,#,%,&".split(",")
            rolls = []
            did_win = False
            winning = 0
            for i in range(5):
                rolls = []
                for y in range(3):
                    random.seed(None)
                    roll_i = random.choice(roll)
                    rolls.append(roll_i)
                print(f"SPIN {i}/5\t{rolls[0]}|{rolls[1]}|{rolls[2]}")
                
                
                if rolls[0] == rolls[1] == rolls[2]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[0]) * 3)
                    print(f"WIN! WIN! WIN! {rolls[0]}x3 -> {get_value(rolls[0]) * 3}")
                elif rolls[0] == rolls[1]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[0]) * 2)
                    print(f"WIN! {rolls[0]}x2 -> {get_value(rolls[0]) * 2}")
                elif rolls[1] == rolls[2]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[1]) * 2)
                    print(f"WIN! {rolls[1]}x2 -> {get_value(rolls[1]) * 2}")
                time.sleep(4)
            if did_win:
                print(f"You Won { winning } {my_bet[0]}")
                bank[my_bet[0]] += int(winning)
            else:
                print(f"You lost {my_bet[1]} {my_bet[0]}")
        else:
            print("Your broke chum!")
    
    



def roullete(bank):
    pass

def casino(bank):
    while 1:
        clearscr()
        header(bank)
        print(" 💰💰 Casino 💰💰")
        print("1.🎰 Play Slots")
        print("2.🎡 Play Roullette")
        print("3.❌ Exit")
        try:
            sel = int(input("?"))
        except KeyboardInterrupt:
            break
        except ValueError:
            continue
        if sel in range(1,4):
            if sel == 1:
                slots(bank)
            elif sel == 2:
                roullete(bank)
            elif sel == 3:
                break

import os.path

def main(bank):
    while 1:
        clearscr()
        header(bank)
        print("1.💰 Visit Casino")
        print("2.🌐 Explore")
        print("3.💾 Save")
        print(f"4.💸 Resume ({'File Found' if os.path.exists('save.json') else 'No Save'})")
        print("5.❌ Quit")
        try:
            sel = int(input("?"))
        except KeyboardInterrupt:
            break
        if sel in range(1,6):
            if sel == 1:
                casino(bank)
            elif sel == 2:
                explore(bank)
            elif sel == 3:
                if bank['bucks'] == 0 and bank['coins'] == 0 and bank['limecoins'] == 0:
                    print("💲 Zero Balance, cant save (did you mean to load a save?)")
                else:
                    save_game("save.json")
            elif sel == 4:
                bank = load_game("save.json")
            elif sel == 5:
                break


main(bank_account)