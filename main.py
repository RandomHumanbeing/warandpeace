import discord
import random
from discord.ext import (
    commands,
    tasks
)
import sqlite3

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
        if op == "*": return eval("num1*num2")
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

token = "your trash"

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

Wars:
[warstat]: Shows war statuses for countries.
[declare]: Starts a war with another country.
[assassinate]: Attempts an assassination on a country.

Allies:
[allystat]: Shows ally statuses for countries.
[ally]: Allies a country.
```"""

    finish = "Operation Completed."

    shop = """```ini
[Black Leaf 40] : $400
[Cyanide] : $300
[Arsenic] : $700
[Deather Stalker Sting] : $1,000
[Polonium] : $10,000```"""

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

        chance = int(grab_budget(countryassassinate))/int(round(generate()))
        price = int("1" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        if chance <= 100:
            price = int("175" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        if chance <= 50:
            price = int("5" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        if chance <= 10:
            price = int("75" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        num = random.uniform(1,chance)
        if int(round(num)) == 2:
            newbudget = str(int(grab_budget(country))+price)
            conn,c = DatabaseFunctions.connect()
            c.execute("UPDATE AgencyBudgets SET budget = ? WHERE country=?", (newbudget, country,))
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
            if term[0] == product: return product[1]






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
            await ctx.channel.send(str(DatabaseFunctions.ally(countryally, country_)))

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
        if str(role) in countries:
            country = str(role)
    for country_ in countries:
        if country_.lower() == countryenmity.lower():
            await ctx.channel.send(str(DatabaseFunctions.enmity(country, countryenmity)))

@wap.command()
async def shop(ctx):
    await ctx.channel.send(Messages.shop)







wap.run(token)
