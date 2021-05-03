import discord
import random
from discord.ext import (
    commands,
    tasks
)
import sqlite3
import threading
import time
from datetime import datetime

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

global generate
def generate(range=150):

    def get_op():
        ops = "/m*-"
        return random.choice(ops)


    def parse_op(num1, num2, op):
        if op == "/": return eval("num1/num2")
        if op == "m": return eval("num1%num2")
        if op == "*": return eval("num1*nummoney+=round(population/2400)2")
        if op == "-": return eval("num1-num2")
        return False


    num = 0.0
    while True:
        num_gen1 = random.randint(1,range)
        num_gen2 = random.randint(1,range)
        operation = get_op()
        try:
            num_ = float(parse_op(num_gen1,num_gen2, operation))
            num += num_
            if num_gen1 == num_gen2:
                break
        except:
            pass

    num1 = num*random.randint(1,range)
    return num1*random.randint(1,range)

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

global countries
countries = open("countries.txt", "r").read().split("\n")

token = ""

prefix = "~"
wap = discord.client
wap = commands.Bot(
    command_prefix=prefix
)

class Messages:
    help = """```ini
Misc:
[help]: Displays this message.
[budget]: Shows your countries budget.
[wap]: https://www.youtube.com/watch?v=hsm4poTWjMs
[claim]: Claims the money from your population. (1 per day)

Wars:
[warstat]: Shows war statuses for countries.
[declare]: Starts a war with another country.
[assassinate]: Attempts an assassination on a country.
[peace]: Stops a war.

Allies:
[allystat]: Shows ally statuses for countries.
[ally]: Allies a country.
[enmity]: Removes ally from another country.

Items:
[shop]: Shows the shop for items that can be used in assassinations.
[buy]: Buys a product from the shop.
[inventory]: Shows the products that your country owns.

Economy:
[budget]: Shows your country's budget.
[addbudget]: Adds money to your budget taken from your money.
[removebudget]: Takes money away from your budget and adds it to your money.
[money]: Shows the money that you have that can be used for buying things.
```"""

    finish = "Operation Completed."

    shop = """```ini
[Black Leaf 40] : $400
[Cyanide] : $300
[Arsenic] : $700
[Death Stalker Sting] : $1,000
[Polonium] : $10,000```"""

    store = """```ini
[Food] : $40
[Shelter] : $5,000
[Clothing] : $24
[Cars] : $18,000
[Medicine] : $12
```"""

    production = """```ini
[Food]:
    Time       : 0.3 seconds/10,000 food
    Price      : $32
    Sell Price : $40

[Shelter]:
    Time       : 0.3 seconds/1,000
    Price      : $4000
    Sell Price : $5000

[Clothing]:
    Time       : 0.3 seconds/50,000
    Price      : $20
    Sell Price : $24

[Cars]:
    Time       : 0.3 seconds/5
    Price      : $15,000
    Sell Price : $18,000

[Medicine]:
    Time       : 0.3 seconds/2,000
    Price      : $10
    Sell Price : $12
```"""

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class DatabaseFunctions:
    def connect(database="main.db"):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        return conn,c

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def warstats():
        conn,c = DatabaseFunctions.connect()
        return_value = "```ini\n"
        for term in c.execute("SELECT * FROM Wars").fetchall():
            return_value+="[" + str(term) + "]" + "\n"
        conn.close()
        return_value = return_value.replace("(", "").replace(")", "").replace("'", "")
        return return_value + "```"

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def warcheck(country, country2):
        conn,c = DatabaseFunctions.connect()
        for term in c.execute("SELECT * FROM Wars").fetchall():
            if term[0] == country:
                if term[1] == country2: return True

            if term[0] == country2:
                if term[1] == country: return True

        return False

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def allycheck(country,country2):
        conn,c = DatabaseFunctions.connect()
        for term in c.execute("SELECT * FROM Allies").fetchall():
            if term[0] == country:
                if term[1] == country2: return True

            if term[0] == country2:
                if term[1] == country: return True

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def declare(country,country2):
        if DatabaseFunctions.allycheck(country,country2) == True:
            conn,c = DatabaseFunctions.connect()
            c.execute("DELETE FROM Allies WHERE country1=? AND country2=?", (country2,country))
            c.execute("DELETE FROM Allies WHERE country1=? AND country2=?", (country,country2))
            conn.commit()
            conn.close()
            return True
        if DatabaseFunctions.warcheck(country,country2) == False:
            conn,c = DatabaseFunctions.connect()
            c.execute("INSERT INTO Wars VALUES (?,?)", (country,country2,))
            conn.commit()
            conn.close()
            return True
        return False

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def ally(country,country2):
        if DatabaseFunctions.warcheck(country,country2) == True:
            conn,c = DatabaseFunctions.connect()
            c.execute("DELETE FROM Wars WHERE country1=? AND country2=?", (country,country2))
            c.execute("DELETE FROM Wars WHERE country1=? AND country2=?", (country2,country))
            conn.commit()
            conn.close()
        conn,c = DatabaseFunctions.connect()
        c.execute("INSERT INTO Allies VALUES (?,?)", (country,country2,))
        conn.commit()
        conn.close()
        return True

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def allystats():
        conn,c = DatabaseFunctions.connect()
        return_value = "```ini\n"
        for term in c.execute("SELECT * FROM Allies").fetchall():
            return_value+="[" + str(term) + "]" + "\n"
        conn.close()
        return_value = return_value.replace("(", "").replace(")", "").replace("'", "")
        return return_value + "```"

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def assassinate(country,countryassassinate):
        global generate
        def grab_budget(country):
            conn,c = DatabaseFunctions.connect()
            for term in c.execute("SELECT * FROM AgencyBudgets").fetchall():
                if term[0].lower() == country.lower():
                    return term[1]
            conn.close()

        num = round(generate())*round(random.randint(5000,100000))*round(generate())**random.randint(1,5)
        chance = int(grab_budget(countryassassinate)+grab_budget(country))/num
        price = int("1" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        if chance <= 100:
            price = int("175" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        if chance <= 50:
            price = int("5" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        if chance <= 10:
            price = int("75" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        num = random.uniform(1,chance)
        if int(round(num)) == 0:
            newbudget = str(int(grab_budget(country))+price)
            conn,c = DatabaseFunctions.connect()
            c.execute("UPDATE AgencyBudgets SET budget = ? WHERE country=?", (str(int(newbudget)*10), country,))
            conn.commit()
            conn.close()
            number = ('{:,}'.format(price))
            chance = round(chance)
            return "Assassinated. " + "2 in " + str(chance) + ". Gained $" + number
        else:
            conn,c = DatabaseFunctions.connect()
            cost = str(int(grab_budget(country)) - int(price))
            c.execute("UPDATE AgencyBudgets SET budget = ? WHERE country=?", (cost, country,))
            conn.commit()
            conn.close()
            number = ('{:,}'.format(price))
            chance = round(chance)
            return "Survived. " + "2 in " + str(chance) + ". Lost $" + number

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def budget(country):
        conn,c = DatabaseFunctions.connect()
        for term in c.execute("SELECT * FROM AgencyBudgets").fetchall():
            if term[0].lower() == country.lower():
                return term[1]
        conn.close()

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def money(country):
        conn,c = DatabaseFunctions.connect()
        for term in c.execute("SELECT * FROM Money").fetchall():
            if term[0].lower() == country.lower():
                return term[1]
        conn.close()

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def add_budget(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.budget(country)
        new = int(current)+int(amount)
        c.execute("UPDATE AgencyBudgets SET budget = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def remove_money(country,amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.money(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Money SET Money = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    ##################################################################################################################################################################
    ##################################################################################################################################################################

    def remove_budget(country,amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.budget(country)
        new = int(current)-int(amount)
        c.execute("UPDATE AgencyBudgets SET budget = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

        ##############################################################################################################################################################
        ##############################################################################################################################################################

    def give_money(country,amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.money(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Money SET money = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def population(country):
        conn,c = DatabaseFunctions.connect()
        for country_ in c.execute("SELECT * FROM Population").fetchall():
            if country_[0] == country:
                return country_[1]

    def peace(country,peace):
        conn,c = DatabaseFunctions.connect()
        c.execute("DELETE FROM Wars WHERE country1=? AND country2=?", (country,peace))
        c.execute("DELETE FROM Wars WHERE country1=? AND country2=?", (peace,country))
        conn.commit()
        conn.close()
        return "True"

    def enmity(country,country2):
        conn,c = DatabaseFunctions.connect()
        c.execute("DELETE FROM Allies WHERE country1=? AND country2=?", (country,country2))
        c.execute("DELETE FROM Allies WHERE country1=? AND country2=?", (country2,country))
        conn.commit()
        conn.close()
        return "True"

    def check_product_price(product):
        conn,c = DatabaseFunctions.connect()
        for term in c.execute("SELECT * FROM ProductPrice").fetchall():
            if term[0] == product: return term[1]

    def give_product(country,product,amount):
        products={'black_leaf_40' : 1,
        'cyanide' : 2,
        'death_stalker_sting' : 3,
        'arsenic' : 4,
        'polonium' : 5}
        conn,c = DatabaseFunctions.connect()
        for term in c.execute("SELECT * FROM Inventories").fetchall():
            if term[0] == country:
                amount=int(amount)
                amount+=int(term[products[product]])

        c.execute(f"UPDATE Inventories SET {product} = ? WHERE country = ?", (str(amount), country,))
        conn.commit()
        conn.close()

    def get_inventory(country):
        conn,c = DatabaseFunctions.connect()
        inventory = {}
        for product in c.execute("SELECT * FROM Inventories").fetchall():
            if product[0] == country:
                inventory["black_leaf_40"] = product[1]
                inventory["cyanide"] = product[2]
                inventory["death_stalker_sting"] = product[3]
                inventory["arsenic"] = product[4]
                inventory["polonium"] = product[5]
        return inventory

    def population(country):
        conn,c = DatabaseFunctions.connect()
        return str(list(c.execute("SELECT * FROM Population WHERE country = ?", (country,)).fetchall()[0])[1])
        conn.close()

    def food(country):
        conn,c = DatabaseFunctions.connect()
        return str(list(c.execute("SELECT * FROM Needs WHERE country = ?", (country,)).fetchall()[0])[1])
        conn.close()

    def shelter(country):
        conn,c = DatabaseFunctions.connect()
        return str(list(c.execute("SELECT * FROM Needs WHERE country = ?", (country,)).fetchall()[0])[2])
        conn.close()

    def increase_population(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.population(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Population SET population = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def decrease_population(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.population(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Population SET population = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def decrease_food(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.food(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Needs SET food = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def increase_food(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.food(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Needs SET food = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def decrease_shelter(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.shelter(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Needs SET shelter = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def increase_shelter(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.shelter(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Needs SET shelter = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def increase_medicine(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.medicine(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Needs SET medicine = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def decrease_medicine(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.medicine(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Needs SET medicine = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def increase_clothing(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.clothing(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Needs SET clothing = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def decrease_clothing(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.clothing(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Needs SET clothing = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def increase_cars(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.clothing(country)
        new = int(current)+int(amount)
        c.execute("UPDATE Needs SET cars = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def decrease_cars(country, amount):
        conn,c = DatabaseFunctions.connect()
        current = DatabaseFunctions.cars(country)
        new = int(current)-int(amount)
        c.execute("UPDATE Needs SET cars = ? WHERE country=?", (int(new), country,))
        conn.commit()
        conn.close()

    def food_threshold(country):
        conn,c = DatabaseFunctions.connect()
        threshold =  str(
list(
c.execute("SELECT * FROM Thresholds WHERE country = ?", (country,)  ).fetchall()[0]
)[1])
        conn.close()
        return threshold

    def shelter_threshold(country):
                conn,c = DatabaseFunctions.connect()
                threshold =  str(
        list(
        c.execute("SELECT * FROM Thresholds WHERE country = ?", (country,)  ).fetchall()[0]
        )[2])
                conn.close()
                return threshold


    def set_threshold(country, amount, threshold = "f"):
        conn,c = DatabaseFunctions.connect()
        if threshold == "f":
            c.execute("UPDATE Thresholds SET food = ? WHERE country=?", (int(amount), country,))
        if threshold == "s":
            c.execute("UPDATE Thresholds SET shelter = ? WHERE country=?", (int(amount), country,))
        conn.commit()
        conn.close()

    def clothing(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Needs WHERE country = ?", (country,)  ).fetchall()[0]
)[3])
        conn.close()
        return return_

    def cars(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Needs WHERE country = ?", (country,)  ).fetchall()[0]
)[4])
        conn.close()
        return return_

    def medicine(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Needs WHERE country = ?", (country,)  ).fetchall()[0]
)[5])
        conn.close()
        return return_

    def start_production(country, item, amount):
        conn,c = DatabaseFunctions.connect()
        if item == "food":
            amount = int(DatabaseFunctions.get_production_food(country)) + int(amount)
            c.execute("UPDATE Production SET food = ? WHERE country = ?", (amount,country,))
        if item == "shelter":
            amount = int(DatabaseFunctions.get_production_shelter(country)) + int(amount)
            c.execute("UPDATE Production SET shelter = ? WHERE country = ?", (amount,country,))
        if item == "clothing":
            amount = int(DatabaseFunctions.get_production_clothing(country)) + int(amount)
            c.execute("UPDATE Production SET clothing = ? WHERE country = ?", (amount,country,))
        if item == "cars":
            amount = int(DatabaseFunctions.get_production_cars(country)) + int(amount)
            c.execute("UPDATE Production SET cars = ? WHERE country = ?", (country,amount,))
        if item == "medicine":
            amount = int(DatabaseFunctions.get_production_medicine(country)) + int(amount)
            c.execute("UPDATE Production SET medicine = ? WHERE country = ?", (amount,country,))
        conn.commit()
        conn.close()

    def get_production_food(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Production WHERE country = ?", (country,)  ).fetchall()[0]
)[1])
        conn.close()
        return return_

    def get_production_shelter(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Production WHERE country = ?", (country,)  ).fetchall()[0]
)[2])
        conn.close()
        return return_

    def get_production_clothing(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Production WHERE country = ?", (country,)  ).fetchall()[0]
)[3])
        conn.close()
        return return_

    def get_production_cars(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Production WHERE country = ?", (country,)  ).fetchall()[0]
)[4])
        conn.close()
        return return_

    def get_production_medicine(country):
        conn,c = DatabaseFunctions.connect()
        return_ = str(
list(
c.execute("SELECT * FROM Production WHERE country = ?", (country,)  ).fetchall()[0]
)[5])
        conn.close()
        return return_



    def start_producing_needs(country):
        rates = {"food": "10000", "shelter": "1000", "clothing": "50000", "cars": "5", "medicine": "2000"}
        prices = {"food": "32", "shelter": "4000", "clothing": "20", "cars": "15000", "medicine": "10"}
        while True:
            food = DatabaseFunctions.get_production_food(country)
            shelter = DatabaseFunctions.get_production_shelter(country)
            clothing = DatabaseFunctions.get_production_clothing(country)
            cars = DatabaseFunctions.get_production_cars(country)
            medicine = DatabaseFunctions.get_production_medicine(country)

            if int(food)>=int(rates["food"]):
                conn,c = DatabaseFunctions.connect()
                DatabaseFunctions.increase_food(country, rates["food"])
                food = DatabaseFunctions.get_production_food(country)
                c.execute("UPDATE Production SET food = ? WHERE country = ?", (str(int(food)-int(rates["food"])),country,))
                conn.commit()
                conn.close()

            if int(shelter)>=int(rates["shelter"]):
                conn,c = DatabaseFunctions.connect()
                DatabaseFunctions.increase_shelter(country, rates["shelter"])
                shelter = DatabaseFunctions.get_production_shelter(country)
                c.execute("UPDATE Production SET shelter = ? WHERE country = ?", (str(int(shelter)-int(rates["shelter"])),country,))
                conn.commit()
                conn.close()

            if int(clothing)>=int(rates["clothing"]):
                conn,c = DatabaseFunctions.connect()
                DatabaseFunctions.increase_clothing(country, rates["clothing"])
                clothing = DatabaseFunctions.get_production_clothing(country)
                c.execute("UPDATE Production SET clothing = ? WHERE country = ?", (str(int(clothing)-int(rates["clothing"])),country,))
                conn.commit()
                conn.close()

            if True==False:
                conn,c = DatabaseFunctions.connect()
                DatabaseFunctions.increase_cars(country, rates["cars"])
                clothing = DatabaseFunctions.get_production_cars(country)
                c.execute("UPDATE Production SET cars = ? WHERE country = ?", (str(int(cars)-int(rates["cars"])),country,))
                conn.commit()
                conn.close()

            if int(medicine)>=int(rates["medicine"]):
                conn,c = DatabaseFunctions.connect()
                DatabaseFunctions.increase_medicine(country, rates["medicine"])
                medicine = DatabaseFunctions.get_production_medicine(country)
                c.execute("UPDATE Production SET medicine = ? WHERE country = ?", (str(int(medicine)-int(rates["medicine"])),country,))
                conn.commit()
                conn.close()
            time.sleep(0.3)





    def start_needs(country):
        day=0
        while True:
            food = int(DatabaseFunctions.food(country))
            medicine = int(DatabaseFunctions.medicine(country))
            cars = int(DatabaseFunctions.cars(country))
            clothing = int(DatabaseFunctions.clothing(country))
            shelter = int(DatabaseFunctions.shelter(country))
            shelter_threshold = int(DatabaseFunctions.shelter_threshold(country))
            food_threshold = int(DatabaseFunctions.food_threshold(country))
            shelter_being_used = 0
            shelter_being_used = round(shelter/shelter_threshold)
            food_being_used = 0
            food_being_used = round(food/food_threshold)
            money = int(DatabaseFunctions.money(country))
            population = int(DatabaseFunctions.population(country))
            rate = [random.randint(5,20),1]
            people_lost = 0
            print("Day " + str(day) + " IRL Time: " + str(datetime.now()) + " Running Operation for Country " + str(country).replace("_", " "))
            day+=1
            if food>=200:
                people_born = round(food_being_used/rate[0])
                food_used = round(food_being_used/rate[1])
                DatabaseFunctions.increase_population(country, people_born)
                DatabaseFunctions.decrease_food(country, food_used)
            else:
                people_lost = round(population/60)
                DatabaseFunctions.decrease_population(country, people_lost)

            if shelter>=1:
                if people_lost == 0:
                    DatabaseFunctions.decrease_shelter(country, round(shelter_being_used/5))
                    shelter-shelter_being_used/10
                    DatabaseFunctions.give_money(country,round(shelter_being_used/60)*5000)
                else:
                    DatabaseFunctions.increase_shelter(country, round(population/40))
                    DatabaseFunctions.remove_money(country,round(int(DatabaseFunctions.money(country))/120))
            if shelter<=-1:
                increase_by = int(str(shelter).replace("-", ""))
                DatabaseFunctions.increase_shelter(country, increase_by)
            if medicine<=100:
                DatabaseFunctions.decrease_population(country, round(population/240))
                DatabaseFunctions.decrease_medicine(country, round(medicine/60))
            else:
                DatabaseFunctions.increase_population(country, round(medicine/100000))
                DatabaseFunctions.decrease_medicine(country, round(medicine/60))

            if clothing<=100:
                DatabaseFunctions.decrease_population(country, round(population/480))
                DatabaseFunctions.decrease_clothing(country, round(medicine/40))
            else:
                DatabaseFunctions.decrease_clothing(country, round(medicine/40))

            if True==False:
                DatabaseFunctions.decrease_population(country, round(population/200))
                DatabaseFunctions.decrease_cars(country, round(cars/120))
            else:
                pass#DatabaseFunctions.decrease_cars(country, round(cars/120))




            time.sleep(60)



conn,c = DatabaseFunctions.connect()
for term in c.execute("SELECT * FROM Needs").fetchall():
    country = term[0]
    threading.Thread(target=DatabaseFunctions.start_needs, args=(country,)).start()
    threading.Thread(target=DatabaseFunctions.start_producing_needs, args=(country,)).start()
conn.close()





@wap.event
async def on_connect():
    print("Connected")

@wap.command()
async def help1(ctx):
    await ctx.channel.send(Messages.help)

@wap.command()
async def warstat(ctx):
    message = DatabaseFunctions.warstats()
    await ctx.channel.send(message)


@wap.command()
async def declare(ctx, countrywar:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    for country_ in countries:
        if country_.lower() == countrywar.lower():
            await ctx.channel.send(str(DatabaseFunctions.declare(country, countrywar)))

@wap.command()
async def ally(ctx, countryally:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    for country_ in countries:
        if country_.lower() == country.lower():
            await ctx.channel.send(stitemnamer(DatabaseFunctions.ally(countryally, country_)))

@wap.command()
async def allystat(ctx):
    message = DatabaseFunctions.allystats()
    await ctx.channel.send(message)

@wap.command()
async def num(ctx):
    await ctx.channel.send(str(generate()))

@commands.cooldown(1, 60, commands.BucketType.user)
@wap.command()
async def assassinate(ctx, countryassassinate:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    await ctx.channel.send(str(DatabaseFunctions.assassinate(country,countryassassinate)))

@wap.command()
async def budget(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    budget = ('{:,}'.format(int(DatabaseFunctions.budget(str(country)))))
    await ctx.channel.send(country + " Budget: $" + budget)

@wap.command()
async def wap_(ctx):
    await ctx.channel.send("https://www.youtube.com/watch?v=hsm4poTWjMs")

@wap.command()
async def money(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    money_raw =  ('{:,}'.format(int(DatabaseFunctions.money(str(country)))))
    money = country + ": $" + money_raw
    await ctx.channel.send(money)

@wap.command()
async def addbudget(ctx, amount:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    if "-" not in str(amount):
        if int(DatabaseFunctions.money(country))>=int(amount):
            DatabaseFunctions.add_budget(country, int(amount))
            DatabaseFunctions.remove_money(country, int(amount))
            budget =  ('{:,}'.format(int(DatabaseFunctions.budget(str(country)))))
            await ctx.channel.send("New Budget: " + budget)

@wap.command()
async def removebudget(ctx, amount:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    if amount<=DatabaseFunctions.budget(country):
        DatabaseFunctions.remove_budget(country,amount)
        DatabaseFunctions.give_money(country,amount)
        await ctx.channel.send("Money: " + str(DatabaseFunctions.money(country)))

@commands.cooldown(1, 86400, commands.BucketType.user)
@wap.command()
async def claim(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    money = int(DatabaseFunctions.population(country))*50
    DatabaseFunctions.give_money(country,money)
    money = ('{:,}'.format(int(money)))
    population =  ('{:,}'.format(int(DatabaseFunctions.population(str(country)))))
    await ctx.channel.send("Gained: " + str(money) + " Population: " + str(population))

@wap.command()
async def peace(ctx, countrypeace:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    for country_ in countries:
        if country_.lower() == countrypeace.lower():
            await ctx.channel.send(str(DatabaseFunctions.peace(country, countrypeace)))

@wap.command()
async def enmity(ctx, countryenmity:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:        DatabaseFunctions.remove_money(country, str(amount))
        DatabaseFunctions.give_money(countrygive, str(amount))
        country = str(role)
    for country_ in countries:
        if country_.lower() == countryenmity.lower():
            await ctx.channel.send(str(DatabaseFunctions.enmity(country, countryenmity)))

@wap.command()
async def shop(ctx):
    await ctx.channel.send(Messages.shop)
@wap.command()
async def buy(ctx, product:str, amount:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    price = int(DatabaseFunctions.check_product_price(product))*int(amount)
    if int(DatabaseFunctions.money(country))>=price:
        DatabaseFunctions.remove_money(country, str(price))
        DatabaseFunctions.give_product(country,product,amount)
        await ctx.channel.send(f"Bought {str(amount)} {str(product)} for $" + str(price))

@wap.command()
async def inventory(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    inventory = str(DatabaseFunctions.get_inventory(country)).replace("{", "").replace("}", "").replace(",", "\n").replace("'", "")
    await ctx.channel.send("```" + str(inventory) + "```")

@wap.command()
async def donate(ctx, countrygive:str, amount:int):
    if "-" not in str(amount):
        global countries
        for role in ctx.author.roles:
            if str(role) in countries:
                country = str(role)
        if int(DatabaseFunctions.money(country))>=int(amount):
            DatabaseFunctions.remove_money(country, str(amount))
            DatabaseFunctions.give_money(countrygive, str(amount))
            await ctx.channel.send("Gave $" + str(amount) + " to " + str(countrygive))

@wap.command()
async def population(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    await ctx.channel.send(country + " Population: " + str(DatabaseFunctions.population(country)))

@wap.command()
async def food(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    await ctx.channel.send(country + " Food: " + str(DatabaseFunctions.food(country)))

@wap.command()
async def shelter(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    await ctx.channel.send(country + " Shelter: " + str(DatabaseFunctions.shelter(country)))

@wap.command()
async def stats(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)
    money = DatabaseFunctions.money(country)
    population = DatabaseFunctions.population(country)
    budget = DatabaseFunctions.budget(country)
    food = DatabaseFunctions.food(country)
    shelter = DatabaseFunctions.shelter(country)
    clothing = DatabaseFunctions.clothing(country)
    cars = DatabaseFunctions.cars(country)
    medicine = DatabaseFunctions.medicine(country)

    money = ('{:,}'.format(int(money)))
    population = ('{:,}'.format(int(population)))
    budget = ('{:,}'.format(int(budget)))
    food = ('{:,}'.format(int(food)))
    shelter = ('{:,}'.format(int(shelter)))
    cars = ('{:,}'.format(int(cars)))
    clothing = ('{:,}'.format(int(clothing)))
    medicine = ('{:,}'.format(int(medicine)))

    message = f"""```ini
{country}:
    [Money]      : ${str(money)}
    [Population] : {str(population)}
    [Budget]     : ${str(budget)}
    [Food]       : {str(food)}
    [Shelter]    : {str(shelter)}
    [Cars]       : {str(cars)}
    [Clothing]   : {str(clothing)}
    [Medicine]   : {str(medicine)}
```"""
    await ctx.channel.send(message)

@wap.command()
async def store(ctx):
    await ctx.channel.send(Messages.store)

@wap.command()
async def purchase(ctx, item:str, amount:int):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)

    money = DatabaseFunctions.money(country)
    food=40
    shelter=5000
    clothing=24
    cars=18000
    medicine=12

    if item.lower() == "food":
        cost = food*amount
    if item.lower() == "shelter":
        cost = shelter*amount
    if item.lower() == "clothing":
        cost = clothing*amount
    if item.lower() == "cars":
        cost = cars*amount
    if item.lower() == "medicine":
        cost = medicine*amount

    if int(money)>=int(cost):
        DatabaseFunctions.remove_money(country, cost)
        if item.lower() == "food":
            DatabaseFunctions.increase_food(country, amount)
            tax = round(cost*0.8)
            DatabaseFunctions.give_money("Brazil", tax)
            await ctx.channel.send("Bought " + str(amount) + " food for " + str(cost) + ".")

        if item.lower() == "shelter":
            DatabaseFunctions.increase_shelter(country, amount)
            await ctx.channel.send("Bought " + str(amount) + " shelter for " + str(cost) + ".")

        if item.lower() == "clothing":
            DatabaseFunctions.increase_clothing(country, amount)
            await ctx.channel.send("Bought " + str(amount) + " clothing for " + str(cost) + ".")

        if item.lower() == "cars":
            DatabaseFunctions.increase_cars(country, amount)
            await ctx.channel.send("Bought " + str(amount) + " cars for " + str(cost) + ".")

        if item.lower() == "medicine":
            DatabaseFunctions.increase_medicine(country, amount)
            await ctx.channel.send("Bought " + str(amount) + " medicine for " + str(cost) + ".")

@wap.command()
async def sellfood(ctx, amount:int):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)

    food = DatabaseFunctions.food(country)
    if int(food)>=amount:
        gained = amount*35
        DatabaseFunctions.decrease_food(country, amount)
        DatabaseFunctions.give_money(country, gained)
        await ctx.channel.send("Sold " + str(amount) + " food for " + str(gained))

@wap.command()
async def evaluate(ctx, equation:str):
    output = eval(equation)
    output = ('{:,}'.format(output))
    await ctx.channel.send(str(output))

@wap.command()
async def production(ctx):
    await ctx.channel.send(Messages.production)

@wap.command()
async def produce(ctx, item:str, amount:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)

    produce_dict_price = {
"food": "32",
"shelter": "4000",
"clothing": "20",
"cars": "15000",
"medicine": "10"
}

    money = int(DatabaseFunctions.money(country))
    product_price = int(produce_dict_price[item.lower()])
    money_needed = int(product_price*int(amount))
    if money>=money_needed:
        DatabaseFunctions.remove_money(country, money_needed)
        DatabaseFunctions.start_production(country, item, amount)
        money_needed = ('{:,}'.format(int(money_needed)))

        await ctx.channel.send("Started production of " + str(item) + " in amounts of " + str(amount) + ". Costed $" + str(money_needed) + ".")

@wap.command()
async def producestats(ctx):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)

    food = DatabaseFunctions.get_production_food(country)
    shelter = DatabaseFunctions.get_production_shelter(country)
    clothing = DatabaseFunctions.get_production_clothing(country)
    cars = DatabaseFunctions.get_production_cars(country)
    medicine = DatabaseFunctions.get_production_medicine(country)

    medicine = ('{:,}'.format(int(medicine)))
    cars = ('{:,}'.format(int(cars)))
    clothing = ('{:,}'.format(int(clothing)))
    shelter = ('{:,}'.format(int(shelter)))
    food = ('{:,}'.format(int(food)))

    message = f"""```ini
[Food]     : {str(food)}
[Shelter]  : {str(shelter)}
[Clothing] : {str(clothing)}
[Cars]     : {str(cars)}
[Medicine] : {str(medicine)}
```"""

    await ctx.channel.send(message)

@wap.command()
async def sell(ctx, item:str, amount:str):
    global countries
    for role in ctx.author.roles:
        if str(role) in countries:
            country = str(role)

    prices = {"food": "40", "shelter": "5000", "clothing": "24", "medicine": "12"}
    cost = "0"

    item = item.lower()
    itemname = item.lower()
    if itemname == "food":
        item = DatabaseFunctions.food(country)
        if int(item)>=int(amount):
            cost = int(amount)*int(prices[itemname])
            DatabaseFunctions.decrease_food(country, amount)
            DatabaseFunctions.give_money(country, cost)

    if itemname == "shelter":
        item = DatabaseFunctions.shelter(country)
        if int(item)>=int(amount):
            cost = int(amount)*int(prices[itemname])
            DatabaseFunctions.decrease_shelter(country, amount)
            DatabaseFunctions.give_money(country, cost)

    if itemname == "clothing":
        item = DatabaseFunctions.clothing(country)
        if int(item)>=int(amount):
            cost = int(amount)*int(prices[itemname])
            DatabaseFunctions.decrease_clothing(country, amount)
            DatabaseFunctions.give_money(country, cost)

    if itemname == "medicine":
        item = DatabaseFunctions.medicine(country)
        if int(item)>=int(amount):
            cost = int(amount)*int(prices[itemname])
            DatabaseFunctions.decrease_medicine(country, amount)
            DatabaseFunctions.give_money(country, cost)

    cost = ('{:,}'.format(int(cost)))
    await ctx.channel.send("Sold " + str(amount) + " " + str(itemname) + " for $" + str(cost) + ".")














wap.run(token)
