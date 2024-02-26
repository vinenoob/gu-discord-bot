from logging import lastResort
import openai
import random
from typing import List

with open('smartBot/gpt3_key.txt') as keyFile:
    key = keyFile.read()
    key = key.replace('\n', "")
    openai.api_key = key

random_sentences = ["Written warnings in instruction manuals are worthless since rabbits can't read.", 'The memory we used to share is no longer coherent.', 'He excelled at firing people nicely.', "That must be the tenth time I've been arrested for selling deep-fried cigars.", 'I am happy to take your donation; any amount will be greatly appreciated.', 'With a single flip of the coin, his life changed forever.', 'Siri became confused when we reused to follow her directions.', "Homesickness became contagious in the young campers' cabin.", 'She was too busy always talking about what she wanted to do to actually do any of it.', 'The beauty of the African sunset disguised the danger lurking nearby.', 'He wondered if she would appreciate his toenail collection.', 'When nobody is around, the trees gossip about the people who have walked under them.', 'Andy loved to sleep on a bed of nails.', 'The tattered work gloves speak of the many hours of hard labor he endured throughout his life.', 'He had concluded that pigs must be able to fly in Hog Heaven.', 'Be careful with that butter knife.', 'She was the type of girl who wanted to live in a pink house.', "Dolores wouldn't have eaten the meal if she had known what it actually was.", 'The teenage boy was accused of breaking his arm simply to get out of the test.', 'Poison ivy grew through the fence they said was impenetrable.', 'They throw cabbage that turns your brain into emotional baggage.', 'Patricia loves the sound of nails strongly pressed against the chalkboard.', 'The murder hornet was disappointed by the preconceived ideas people had of him.', "You've been eyeing me all day and waiting for your move like a lion stalking a gazelle in a savannah.", 'His mind was blown that there was nothing in space except space itself.', 'I had a friend in high school named Rick Shaw, but he was fairly useless as a mode of transport.', 'He wondered if it could be called a beach if there was no sand.', 'Flesh-colored yoga pants were far worse than even he feared.', 'When he asked her favorite number, she answered without hesitation that it was diamonds.', "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.", 'There was no telling what thoughts would come from the machine.', "It's never comforting to know that your fate depends on something as unpredictable as the popping of corn.", 'Erin accidentally created a new universe.', "Honestly, I didn't care much for the first season, so I didn't bother with the second.", 'The estate agent quickly marked out his territory on the dance floor.', 'Three years later, the coffin was still full of Jello.', 'Before he moved to the inner city, he had always believed that security complexes were psychological.', "She thought there'd be sufficient time if she hid her watch.", 'This is the last random sentence I will be writing and I am going to stop mid-sent', 'He appeared to be confusingly perplexed.', 'There was coal in his stocking and he was thrilled.', 'The two walked down the slot canyon oblivious to the sound of thunder in the distance.', 'Grape jelly was leaking out the hole in the roof.', "It's always a good idea to seek shelter from the evil gaze of the sun.", 'Peter found road kill an excellent way to save money on dinner.', 'He poured rocks in the dungeon of his mind.', 'Nothing is as cautiously cuddly as a pet porcupine.', "It would have been a better night if the guys next to us weren't in the splash zone.", 'No matter how beautiful the sunset, it saddened her knowing she was one day older.', "Weather is not trivial - it's especially important when you're standing in it."]

messages=[]


def _getResponse(input: str) -> str:
    messages.append({"role": "user", "content": f"answer using the previously provided chats: {input}"})
    response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
    messages.append({"role": "system", "content": response.choices[0].message.content})
    return response.choices[0].message.content

def createImage(input: str) -> str:
    client = openai.OpenAI()
    try:
        imageResponseJSON: openai = client.images.generate(
            prompt= input,
            n=1,
            size="256x256"
        )
        return imageResponseJSON["data"][0]["url"]
    except:
        return "this image was censored"

def generateOutput(input: str):
    while (lastResponse := _getResponse(input)) == "":
        lastResponse = _getResponse(random.choice(random_sentences))

    return lastResponse

def loadMessages(messages_to_load: List[str]):
    global messages
    messages.clear()
    messages=[
    {"role": "system", "content": """
    you are an assistant in a discord server. you specialize in summarizing the history of chats.
    you will be passed a list of messages with who sent them, when, and the content of the message.
    """},
    ]
    for message in messages_to_load:
        messages.append({"role": "user", "content": message})