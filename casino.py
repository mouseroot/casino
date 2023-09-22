import random
import json
import time
import os.path

bank_account = {
    "bucks": 0,
    "coins": 0,
    "limecoins": 0
}

save_data = {
    "name": "",
    "wins": 0,
    "losses": 0,
    "win_sum": 0,
    "loss_sum": 0,
    "days": 0,
    "hours": 0,
    "bank": bank_account,
    "balance": bank_account.copy()
}


def save_game(sv_fname, data):
    json.dump(data, open(sv_fname,"w"),indent=4)
    print(f"💾 Game was saved")

def load_game(ld_fname):
    print(f"💿 Game Loaded")
    return json.load(open(ld_fname,"r"))

def clearscr():
    #print(chr(27) + "[2J")
    print()
    print()

def increase_time():
    global save_data
    save_data['hours'] += 1
    if save_data['hours'] >= 24:
        save_data['days'] += 1
        save_data['hours'] = 0

def stats(data):
    print(f"Name: 🧑 {data['name']}")
    print(f"Wins: ✔ {data['wins']}")
    print(f"Losses: ❌ {data['losses']}")
    print(f"Total Winnings: 💵 {data['win_sum']}")
    print(f"Total Losses: 💵 {data['loss_sum']}")
    print(f"Days passed: 📅 {data['days']}")
    print(f"Hours passed: ⌚ {data['hours']}")


def header(data):
    balance = data['balance']
    print("-"*50)
    print(f"Name: {data['name']} ✔ {data['wins']} / ❌ {data['losses']}")
    print(f"Time: ⌚ {data['hours']} Hours / 📅 {data['days']} Days")
    print(f"Balance: 💵 ${balance['bucks']} / 🔘 {balance['coins']} Coins / 🟡 {balance['limecoins']} Limecoins")
    print(f"-"*50)

def is_broke(data):
    balance = data['balance']
    return balance['bucks'] > 0 and balance['coins'] > 0 and balance['limecoins']

# select_bet - Show the select bet menu, returns (bet_type, ammount)
def select_bet(data):
    while 1:
        balance = data['balance']
        print(random.choice(["Cmon, place ya bets","Care to make a wager?"]))
        bet_type = False
        print(f"1. 💵 Use Bucks (${balance['bucks']})")
        print(f"2. 🔘 Use Coins ({balance['coins']} Coins)")
        print(f"3. 🟡 Use Limecoins ({balance['limecoins']})")
        print("4. ❌ Cancel Bet")
        try:
            bet_select = int(input("Bet with? "))
            if bet_select in range(1,5):
                if bet_select == 1:
                    if balance['bucks'] <= 0:
                        print(f"You dont got enough dosh.")
                        break
                    else:
                        print(f"Alright, your using cold cash, the good stuff.")
                        bet_type = "bucks"
                elif bet_select == 2:
                    if balance['coins'] <= 0:
                        print(f"Not enough coins...")
                        break
                        
                    else:
                        print(f"Using coins, good at any casino")
                        bet_type = "coins"
                elif bet_select == 3:
                    if balance['limecoins'] <= 0:
                        print(f"Get more limecoin, and come back")
                        break
                        
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
                if int(balance[bet_type]) >= amt:
                    print(f"Alright thats {amt} {bet_type}")
                    return (bet_type, amt)
                else:
                    continue
        except KeyboardInterrupt:
            return False

#beg - random chance to get some coins.
def beg(data):
    increase_time()
    balance = data['balance']
    print("You beg")
    beg_chance = random.randint(1,6)
    if beg_chance >= 4:
        r_ammount = random.randint(1,10)
        print(f"👍 A kind stranger hands you {r_ammount} coins")
        balance['coins'] += r_ammount
    else:
        print(f"👎 Many pass by, but nobody gives you anything")

#explore - explore around the casino
def explore(data):
    while 1:
        increase_time()
        balance = data['balance']
        print("You explore around")
        print("1. 🙌 Beg on the streets")
        print("2. 👞 Walk around")
        print("3. ❌ Go Back")
        sel = int(input("?"))
        if sel in range(1,4):
            if sel == 1:
                beg(data)
            elif sel == 2:
                print("You wander around...")
            elif sel == 3:
                break

#get_value(char) - returns the number value of special chars like K,Q,J,A and wild chars
def get_value(item):
        if item == 'A':
            return 10
        elif item == 'J':
            return 7
        elif item == 'K':
            return 9
        elif item == 'Q':
            return 9
        elif item == '♥':
            return 5
        elif item == '♦':
            return 5
        elif item == '♠':
            return 5
        elif item == '♣':
            return 5
        else:
            return int(item)


#slots game - place bets, spin 5 slots, each match is a win
def slots(data):
    global save_data
    while 1:
        balance = data['balance']
        if not is_broke(data):
            my_bet = select_bet(data)
            if my_bet:
                if my_bet[0] == "bucks":
                    print(f"You wagered 💵 ${my_bet[1]}")
                elif my_bet[0] == "coins":
                    print(f"You wagered 🔘 {my_bet[1]} Coins")
                elif my_bet[0] == "limecoins":
                    print(f"You wagered 🟡 {my_bet[1]} Limecoins")
            else:
                break
            #remove money from account.
            balance[my_bet[0]] -= my_bet[1]
            increase_time()
            roll = "1,2,3,4,5,6,7,8,9,A,J,K,Q,♥,♦,♠,♣".split(",")
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
                    print(f"💲💲💲 WIN! WIN! WIN! {rolls[0]}x3 -> {get_value(rolls[0]) * 3}")
                    data['wins'] += 1
                elif rolls[0] == rolls[1]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[0]) * 2)
                    print(f"💲 WIN! {rolls[0]}x2 -> {get_value(rolls[0]) * 2}")
                    data['wins'] += 1
                elif rolls[1] == rolls[2]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[1]) * 2)
                    print(f"💲 WIN! {rolls[1]}x2 -> {get_value(rolls[1]) * 2}")
                    data['wins'] += 1
                elif rolls[0] == rolls[2]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[1]) * 2)
                    print(f"💲 WIN! {rolls[1]}x2 -> {get_value(rolls[1]) * 2}")
                    data['wins'] += 1
                time.sleep(4)
            if did_win:
                print(f"💲💲💲 You Won { winning } {my_bet[0]}")
                balance[my_bet[0]] += int(winning)
                data['win_sum'] += int(winning)
            else:
                print(f"👎 You lost {my_bet[1]} {my_bet[0]}")
                data['losses'] += 1
        else:
            print("❌ Your broke chum!")
        save_data = data

def computer():
    global save_data
    print("1. ✉ Check Email")
    print("2. 🌐 Browse Web")
    print("3. 💾 Hack Servers")



def home(data):
    increase_time()
    print("Welcome home")
    print("1. 🪑 Relax")
    print("2. 🛏 Sleep")
    print("3. 📺 Watch TV")
    print("4. 🖱 Use Computer")
    print("5. ❌ Leave")
    sel = get_input("? ")
    if sel in range(1,6):
        if sel == 1:
            print("You sit down and relax")
        elif sel == 2:
            print("You sleep in your own bed")
        elif sel == 3:
            print("You watch some t.v")
        elif sel == 4:
            print("You turn on your PC")
            computer()

def go_bank(bank):
    increase_time()
    print("Save your assets")

def xchange(bank):
    increase_time()
    print("Convert your coins into bucks")
    print("1. 🔘 -> 💵 (Coins to Bucks)")

def airport(bank):
    increase_time()
    increase_time()
    print("Fly to different places")

def docks(bank):
    increase_time()
    increase_time()
    print("Float to different places")

#travel to different areas
def travel(bank):
    increase_time()
    print("Travel To Where")
    print("1. 🏠 Home")
    print("2. 🏦 Bank")
    print("3. 🏛  Currency Exchange")
    print("4. ✈  Airport")
    print("5. 🚢 Docks")
    sel = get_input("? ")
    if sel in range(1,6):
        if sel == 1:
            home(bank)
        elif sel == 2:
            go_bank(bank)
        elif sel == 3:
            xchange(bank)
        elif sel == 4:
            airport(bank)
        elif sel == 5:
            docks(bank)




#roullete - gonna use cos to generate an angle, and dot product to gestimate its closeness
def roullete(bank):
    pass

#casino menu
def casino(data):
    while 1:
        clearscr()
        header(data)
        print("💰💰 Casino 💰💰")
        print("1.🎰 Play Slots")
        print("2.🎡 Play Roullette")
        print("3.🌐 Explore around")
        print("4.❌ Exit")
        try:
            sel = int(input("?"))
        except KeyboardInterrupt:
            break
        except ValueError:
            continue
        if sel in range(1,4):
            if sel == 1:
                slots(data)
            elif sel == 2:
                roullete(data)
            elif sel == 3:
                explore(data)
            elif sel == 4:
                main(data)


#sanitized input
def get_input(prompt):
    while 1:
        try:
            return int(input(prompt))
        except KeyboardInterrupt:
            return False
        except ValueError:
            continue


#new_game - start a new game
def new_game(data):
    data["name"] = input("✏  What is your Name? ")
    save_game("save.json",data)
    main(data)



#game start menu (1st menu)
def bootup(data):
    global save_data
    while 1:
        print("Welcome to Casino")
        print("1. 💲 Start new game")
        print("2. ⏩ Continue")
        print("3. ❌ Quit")
        sel = get_input("?")
        if sel in range(1,4):
            if sel == 1:
                new_game(data)
                break
            elif sel == 2:
                save_data = load_game("save.json")
                main(save_data)
                break
            elif sel == 3:
                break

#main game loop
def main(data):
    
    while 1:
        balance = data['balance']
        clearscr()
        header(data)
        print("1.💰 Visit Casino")
        print("2.🌐 Travel")
        print("3.💾 Save")
        #print(f"4.💸 Resume ({'File Found' if os.path.exists('save.json') else 'No Save'})")
        print("4.❌ Quit")
        try:
            sel = int(input("?"))
        except KeyboardInterrupt:
            return
        if sel in range(1,5):
            if sel == 1:
                casino(data)
            elif sel == 2:
                travel(data)
            elif sel == 3:
                if is_broke(data):
                    print("💲 Zero Balance, cant save (did you mean to load a save?)")
                else:
                    save_game("save.json", data)
            elif sel == 4:
                return


# Main
bootup(save_data)