import random

def roll(QuantityDSides):
    Divider = 0 #sets a divider for the letter d in 2d6, for example
    i = 0
    while i < len(QuantityDSides):
        letter = QuantityDSides[i] #pick a letter 
        if letter == "D" or letter == "d": #checks if it's the d OwO
            Divider = i  #the d has been found, recording location
        i = i + 1  #d was not found, go to the next letter and loop back

    Invalid = False
    if Divider == 0:  #if the divider was 0, it means it couldn't find the d >_<
        Invalid = True
    Quantity = 0  #finds the number of dice to be rolled by using everything in the message before the d
    Sides = 0  #finds the number of sides on the dice to be rolled by using everything after the d

    try: #okay so right now it's testing if Quantity and Sides are actually numbers and not people trying to hurt senpai
        Quantity = int(QuantityDSides[:Divider])		#Identify Quantity
    except ValueError:
        Invalid = True

    try:
        Sides = int(QuantityDSides[Divider+1:])	#Identify Sides
    except ValueError:
        Invalid = True

    if Invalid: #this should only come up if the numbers might actually hurt senpai (or if there is no d)
        return str("'{}'? You are objectively wrong. Use '!roll xDy'. \n x = Number of dice, \n y = Dice sides. \n ie: '!roll 2d6'.".format(QuantityDSides))

        #cool features including but not limited to:
        #    - less than infinity dice
        #    - sassy responses in chat
        #    - automatically exits the loop so you don't have to
        #    - only exits the loop when it's supposed to
    if Quantity > 10000:
        return str("I'm not rolling that many dice, it would take *forever*.")
        #return

    #actually roll the dice
    #await channel.send("Rolling " + str(Quantity)+ " " +str(Sides) + " sided dice.")
    print("Rolling " + str(Quantity)+ " " +str(Sides) + " sided dice.")
    Total = 0
    i = 0
    while i < Quantity:
        #there needs to be a way to use "client.process_commands()" to prevent this from freezing the bot on large rolls
        Roll = random.randint(1,Sides)
        print("Rolled " + str(Roll) + ".")
        Total += Roll
        i = i + 1

    #Here's the result UwU
    print("Total is " + str(Total))
    return str("Rolled a " + str(Total))