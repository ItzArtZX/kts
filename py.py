import asyncio
from kahoot import KahootClient
from kahoot.packets.impl.respond import RespondPacket
from kahoot.packets.server.game_over import GameOverPacket
from kahoot.packets.server.game_start import GameStartPacket
from kahoot.packets.server.question_end import QuestionEndPacket
from kahoot.packets.server.question_ready import QuestionReadyPacket
from kahoot.packets.server.question_start import QuestionStartPacket

def prompt_username():
    usr_temp = str(input("Enter your username (max 15 characters) > "))
    while len(usr_temp) < 1 or len(usr_temp) > 15:
        print("Sorry, the username is too short/long")
        usr_temp = str(input("Enter your username (max 15 characters) > "))
    return(usr_temp)

def prompt_pin():
    pin_temp = str(input("Enter your game's pin > "))
    return(pin_temp)

username = prompt_username()
pin = prompt_pin()

client: KahootClient = KahootClient()

async def game_start(packet: GameStartPacket):
    print(f"Game started: {packet}")

async def game_over(packet: GameOverPacket):
    print(f"Game over: {packet}")

async def question_start(packet: QuestionStartPacket):
    print(f"Question started: {packet}")
    question_number: int = packet.game_block_index
    await client.send_packet(RespondPacket(client.game_pin, 1, question_number))

async def question_end(packet: QuestionEndPacket):
    print(f"Question ended: {packet}")

async def question_ready(packet: QuestionReadyPacket):
    print(f"Question ready: {packet}")

async def main():
    # Register event handlers before joining the game
    client.on("game_start", game_start)
    client.on("game_over", game_over)
    client.on("question_start", question_start)
    client.on("question_end", question_end)
    client.on("question_ready", question_ready)

    # Join the game
    await client.join_game(pin, username)

if __name__ == "__main__":
    asyncio.run(main())