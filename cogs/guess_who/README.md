# Guess Who

Status: first version in `interface.py`. Start a round with `/guesswho play`.

## Concept

A game where the bot picks a message that a random server member sent earlier and posts it in the channel. Players then guess **who** wrote it.

## Rough flow

1. Someone starts a round with a command.
2. The bot picks a random past message (with real text in it) from a random member.
3. The bot posts the message without its author's name.
4. Players submit guesses.
5. The bot reveals who wrote it, and maybe a link to the original message, and says who guessed right.
