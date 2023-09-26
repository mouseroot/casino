import random
import json
import time
import math
import sys
import os.path



bank_account = {
    "bucks": 0,
    "coins": 0,
    "limecoins": 0,
    "ambinar": 0,
    "gillinite": 0
}

save_data = {
    "name": "",
    "wins": 0,
    "losses": 0,
    "win_sum": 0,
    "loss_sum": 0,
    "tickets": 0,
    "energy": 100,
    "days": 0,
    "hours": 0,
    "bank": bank_account,
    "balance": bank_account.copy()
}

def format_currency(val):
    if val > 1000 and val < 1000000:
        percent = val / 1000
        return str(percent) + " K"
    elif val > 1000000 and val < 1000000000:
        percent = val / 1000000
        return str(percent) + " M"
    elif val > 1000000000:
        percent = val / 1000000000
        return str(percent) + " B"

def save_game(sv_fname, data):
    json.dump(data, open(sv_fname,"w"),indent=4)
    print(f"💾 Game was saved")

def load_game(ld_fname):
    print(f"💿 Game Loaded")
    return json.load(open(ld_fname,"r"))

def clearscr():
    print(chr(27) + "[2J")
    #print()
    #print()

def increase_time(val=1):
    global save_data
    save_data['hours'] += val
    if save_data['hours'] >= 24:
        save_data['days'] += 1
        save_data['hours'] = 0

def use_energy(amt):
    global save_data
    save_data['energy'] -= amt

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
    print(f"Balance: 💵 ${format_currency(balance['bucks'])} / 🔘 {math.ceil(balance['coins'])} Coins / 🟡 {math.ceil(balance['limecoins'])} Limecoins / 💍 {math.ceil(balance['ambinar'])} Ambinar / 💎 {math.ceil(balance['gillinite'])} Gillinite")
    print(f"Energy: ⚡ {data['energy']}\tTickets: 🎫 {data['tickets']}")
    print(f"-"*50)

def is_broke(data):
    balance = data['balance']
    return balance['bucks'] == 0 and balance['coins'] == 0 and balance['limecoins'] == 0

def do_sleep(t):
    global save_data
    for i in range(t):
        print('💤',end='')
        sys.stdout.flush()
        time.sleep(3)
    print('',end='\n')
    r_energy = random.randint(50,100)
    save_data['energy'] += r_energy
    print(f"⚡ Gained {r_energy}")


# select_bet - Show the select bet menu, returns (bet_type, ammount)
def select_bet(data):
    while 1:
        balance = data['balance']
        print(random.choice(["Cmon, place ya bets","Care to make a wager?"]))
        bet_type = False
        print(f"1. 💵 Use Bucks (${format_currency(balance['bucks'])})")
        print(f"2. 🔘 Use Coins ({math.ceil(balance['coins'])} Coins)")
        print(f"3. 🟡 Use Limecoins ({math.ceil(balance['limecoins'])})")
        print(f"4. 💍 Use Ambinar ({math.ceil(balance['ambinar'])})")
        print(f"5. 💎 Use Gillinite ({math.ceil(balance['gillinite'])})")
        print(f"6. ❌ Cancel Bet")
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
                    if balance['ambinar'] <= 0:
                        print(f"Not enough Ambinar, go mine some")
                        break
                    else:
                        print("A Rare gemstone")
                        bet_type = 'ambinar'
                    pass
                elif bet_select == 5:
                    if balance['gillinite'] <= 0:
                        print(f"Not enough Gillinite")
                        break
                    else:
                        print("Rare Form of Diamond")
                        bet_type = 'gillinite'
                    return False
                elif bet_select == 6:
                    return False
        except KeyboardInterrupt:
            return False
        try:
            while 1:
                amt = int(input(f"How much {bet_type} you wanna wager? "))
                if int(balance[bet_type]) >= amt:
                    return (bet_type, amt)
                else:
                    continue
        except KeyboardInterrupt:
            return False

#beg - random chance to get some coins.
def beg(data):
    
    #clearscr()
    header(data)
    balance = data['balance']
    if data['energy'] > 2:
        increase_time()
        use_energy(2)
        print("You beg")
        r_currencies_str = ['🔘 coins','🟡 limecoins','💵 bucks']
        r_currency = random.choice(r_currencies_str)

        beg_chance = random.randint(1,6)
        if beg_chance >= 4:
            r_ammount = random.randint(1,10)
            print(f"👍 A kind stranger hands you {r_ammount} {r_currency}")
            balance[r_currency[2:].strip()] += r_ammount
        else:
            print(f"👎 Many pass by, but nobody gives you anything")
    else:
        print("❌ Your out of energy 🏠 Go Home and Rest/Sleep")

#get_value(char) - returns the number value of special chars like K,Q,J,A and wild chars
def get_value(item):
        if item == 'A':
            return 200
        elif item == 'J':
            return 100
        elif item == 'K':
            return 100
        elif item == 'Q':
            return 100
        elif item == '♥':
            return 50
        elif item == '♦':
            return 50
        elif item == '♠':
            return 50
        elif item == '♣':
            return 50
        else:
            return int(item)*2


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
            use_energy(3)
            roll = "2,3,4,5,6,7,8,9,A,J,K,Q,♥,♦,♠,♣".split(",")
            rolls = []
            multi = 0
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
                    multi += 1
                elif rolls[0] == rolls[1]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[0]) * 2)
                    print(f"💲 WIN! {rolls[0]} x2 -> {get_value(rolls[0]) * 2}")
                    data['wins'] += 1
                    multi += 1
                elif rolls[1] == rolls[2]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[1]) * 2)
                    print(f"💲 WIN! {rolls[1]} x2 -> {get_value(rolls[1]) * 2}")
                    data['wins'] += 1
                    multi += 1
                elif rolls[0] == rolls[2]:
                    did_win = True
                    winning += (my_bet[1]) + (get_value(rolls[0]) * 2)
                    print(f"💲 WIN! {rolls[0]} x2 -> {get_value(rolls[0]) * 2}")
                    data['wins'] += 1
                    multi += 1
                time.sleep(4)
            if did_win:
                
                if multi > 1:
                    print(f"Win Multiplier x{multi}")
                    if multi > 3:
                        print(f"+ 4x Bonus +500")
                        winning += 500
                    winning *= multi
                balance[my_bet[0]] += int(winning)
                data['win_sum'] += int(winning)
                print(f"💲💲💲 You Won { winning } {my_bet[0]}")
            else:
                print(f"👎 You lost {my_bet[1]} {my_bet[0]}")
                data['losses'] += 1
        else:
            print("❌ Your broke chum!")
        save_data = data
        return

def computer():
    global save_data
    print("1. ✉  Check Email")
    print("2. 🌐 Browse Web")
    print("3. 💾 Hack Servers")
    print("4. 🖥 Open Command Line")
    sel = get_input("? ")
    if sel == 4:
        print("PC Bootup, /help for commands")
        while 1:
            try:
                command = input("> ").lower()
            except KeyboardInterrupt:
                print("❌ Goodbye")
                break
            except ValueError:
                print("❌ Invalid Input")
            if command.startswith("/cheat "):
                code = command.split("/cheat ")[1]
                if code == "casino":
                    save_data['balance']['bucks'] += 1000000
                    print("🤑 Bank Glitch: Balance + 1M")
            elif command.startswith("/exit"):
                print("❌ Goodbye")
                break
            elif command.startswith("/help"):
                print()
                print("📖 PC Command Help Page")
                print("/cheat <code>")
                print("/help")
                print("/exit")
                print("sdfs#$%e53#$%453l#$%df sdfsoe3#$%%Y")
            else:
                print()
                print("❌ Unknown Command use /help")

def home(data):
    increase_time()
    use_energy(1)
    clearscr()
    header(data)
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
            r_energy = random.randint(5,25)
            data['energy'] += r_energy
            print(f"⚡ Gained {r_energy}")
        elif sel == 2:
            print("You sleep in your own bed")
            do_sleep(5)
        elif sel == 3:
            print("You watch some t.v")
        elif sel == 4:
            print("You turn on your PC")
            computer()

def go_bank(data):
    balance = data['balance']
    bank = data['bank']
    increase_time()
    use_energy(5)
    header(data)
    print("Welcome to the Swiss Bank 🧀")
    print(f"Teller: You balance is 💵 {bank['bucks']}")
    if balance['bucks'] == 0 and bank['bucks'] == 0:
        print(f"You dont seem to have any bucks at all, hit the casino chum.")
        return
    print("1. 💵 Make a Deposit")
    print("2. 🏧 Make a Widthdrawl")
    print("3. ❌ Leave")
    sel = get_input("? ")
    if sel in range(1,4):
        if sel == 1:
            if balance['bucks'] > 0:
                print("💵 How much you depositting in?")
                amt = float(input("💵 Bucks ?"))
                if amt <= balance['bucks']:
                    bank['bucks'] += amt
                    balance['bucks'] -= amt
                    print(f"🏧 You depositted {amt} into your account")
                    print(f"🏧 Your new balance is {bank['bucks']}")
                else:
                    print("❌ Aint got enough!")
        elif sel == 2:
            if bank['bucks'] > 0:
                print(f"Alright, how much you taking out? (1alance: {bank['bucks']})")
                amt = get_input("💵 Bucks ?")
                if amt >= bank['bucks']:
                    bank['bucks'] -= amt
                    balance['bucks'] += amt
                    print(f"🏧 You Widthdrew {amt} from your account")
                    print(f"🏧 Your new balance is {balance['bucks']}")

                else:
                    print("❌ You dont have that much in your account...")

def xchange(data):
    global save_data
    balance = data['balance']
    increase_time()
    use_energy(5)
    clearscr()
    header(data)
    print("Convert your coins into bucks, and back again")
    print(f"1. 🔘 200 -> 💵 $2.25")
    print(f"2. 🔘 500 -> 💵 $5.50")
    print(f"3. 💵 $2 -> 🔘 350")
    print(f"4. 💵 $5 -> 🔘 570")
    print("5. ❌ Leave")
    sel = get_input("? ")
    if sel in range(1,6):
        if sel == 1:
            if balance['coins'] >= 200:
                balance['coins'] -= 200
                balance['bucks'] += 1
                print(f"Trading 🔘 for 💵")
            else:
                print(f"❌ Not Enough")
        elif sel == 2:
            if balance['coins'] >= 500:
                balance['coins'] -= 500
                balance['bucks'] += 5.50
            else:
                print(f"❌ Not Enough")
        elif sel == 3:
            if balance['bucks'] >= 2:
                print(f"Trading 💵 for 🔘")
                balance['bucks'] -= 2
                balance['coins'] += 350
            else:
                print(f"❌ Not Enough")

        elif sel == 4:
            if balance['bucks'] >= 5:
                print(f"Trading 💵 for 🔘")
                balance['bucks'] -= 5
                balance['coins'] += 570
            else:
                print(f"❌ Not Enough")
        else:
            pass
    save_data = data
    

def airport(data):
    use_energy(10)
    increase_time(2)
    print("✈ Fly to different places")
    if data['tickets'] >= 2:
        pass
    else:
        print("❌ Not enough tickets")

def docks(data):
    balance = data['balance']
    use_energy(10)
    increase_time(2)
    print("U.S.S 🚢 Sentinal")
    print("Capt. Waters: Ya, need tickets a plenty to afford this cruize")
    if data['tickets'] >= 10:
        pass
    else:
        print("❌ Dont have enough tickets")

def store(data):
    use_energy(5)
    increase_time(2)
    header(data)
    print(f"Welcome to the Store")
    print("1.🍬 Buy Energy Candy x2 (💵 $20)")
    print("2.🍫 Buy Bonus Chocolate x2 (💵 $70)")
    print("3.🎫 Buy Tickets x1 (💵 $1000)")
    print("3.❌ Leave")
    sel = get_input("? ")
    if sel in range(1,4):
        if sel == 1:
            pass
        elif sel == 2:
            pass
        elif sel == 3:
            return

#travel to different areas
def travel(data):
    use_energy(5)
    increase_time()
    clearscr()
    header(data)
    print("Travel To Where")
    print("1. 🏠 Home")
    print("2. 🏦 Bank")
    print("3. 💰 Casino")
    print("4. 🏛  Currency Exchange")
    print("5. 🏬 Store")
    print("6. ✈  Airport")
    print("7. 🚢 Docks")
    print("8. ❌ Cancel")
    sel = get_input("? ")
    if sel in range(1,7):
        if sel == 1:
            home(data)
        elif sel == 2:
            go_bank(data)
        elif sel == 3:
            casino(data)
        elif sel == 4:
            xchange(data)
        elif sel == 5:
            store(data)
        elif sel == 6:
            airport(data)
        elif sel == 7:
            docks(data)
        elif sel == 8:
            return

def get_value_war(val):
    if val == "A":
        return 20
    elif val in "2,3,4,5,6,7,8,9".split(","):
        return int(val)
    elif val in "K,Q,J".split(","):
        return 10

def war(data):
    balance = data['balance']
    print("🃏 Play War")
    my_bet = select_bet(data)
    if my_bet:
        currency = my_bet[0]
        bet_value = my_bet[1]
        balance[currency] -= bet_value
        cards = "A,2,3,4,5,6,7,8,9,K,Q,J".split(",")
        suits = "♥,♦,♠,♣".split(",")
        pc_sum = 0
        player_sum = 0
        for i in range(2):
            r_card = random.choice(cards)
            r_suit = random.choice(suits)
            print(f"🃏 Dealer Hand #{i+1} {r_card} {r_suit} -> {get_value_war(r_card)}")
            pc_sum += get_value_war(r_card)
        print(f"Dealer Sum is {pc_sum}")
        print("Player Draws...")
        for i in range(2):
            r_card = random.choice(cards)
            r_suit = random.choice(suits)
            print(f"🃏 Player Hand #{i+1} {r_card} {r_suit} -> {get_value_war(r_card)}")
            player_sum += get_value_war(r_card)
        print(f"Player Sum is {player_sum}")
        if player_sum > pc_sum:
            print("✔ Player Won!")
            return True
        else:
            print("❌ Dealer Won!")
            return False


#roullete - gonna use cos to generate an angle, and dot product to gestimate its closeness
def roullete(data):
    print("🎡 Play Roullete")
    print("")

#casino menu
def casino(data):
    while 1:
        header(data)
        print("💰Casino💰")
        print("1. 🎰 Play Slots")
        print("2. 🎡 Play Roullette")
        print("3. 🃏 Play War")
        print("4. 🙌 Beg on the streets")
        print("5. 👞 Walk around")
        print("6. ❌ Leave")
        try:
            sel = get_input("? ")
        except KeyboardInterrupt:
            return
        if sel in range(1,7):
            if sel == 1:
                slots(data)
            elif sel == 2:
                roullete(data)
            elif sel == 3:
                war(data)
            elif sel == 4:
                beg(data)
            elif sel == 5:
                print("You walk around...")
            elif sel == 6:
                return


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
                sys.exit(0)

#main game loop
def main(data):
    while 1:
        balance = data['balance']
        #clearscr()
        header(data)
        print("🗺   Map Screen")
        print("1. 😊 Stats")
        print("2. 🎒 Inventory")
        print("3. 🌐 Travel")
        print("4. 💾 Save")
        #print(f"4.💸 Resume ({'File Found' if os.path.exists('save.json') else 'No Save'})")
        print("5.❌ Quit")
        try:
            sel = get_input("? ")
        except KeyboardInterrupt:
            return
        if sel in range(1,6):
            if sel == 1:
                stats(data)
            elif sel == 2:
                print("Inventory")
            elif sel == 3:
                travel(data)
            elif sel == 4:
                if is_broke(data):
                    print("💲 Zero Balance, cant save (did you mean to load a save?)")
                else:
                    save_game("save.json", data)
            elif sel == 5:
                break


# Main
bootup(save_data)