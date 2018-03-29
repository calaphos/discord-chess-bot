import discord
from coordinates import Coordinate as C
from chessboard import ChessBoard, InvalidMoveException
client = discord.Client()
chessGame = None

token = "NDI3MDkxNDI0Mzg3OTIzOTY4.DZ14nQ.Y_RWIzJNgYv4DfPg9isO2siPpuY"


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def parse_move_commands(msg:str) -> (C,C):
    msg = msg.replace("!chess move", "", 1)
    print("move commands: {}".format(msg))
    if len(msg.split()) != 2:
        raise Exception("to many or few coordinates")
    origin, destination = msg.split()
    if origin[0] not in "abcdefgh" or origin[1] not in "12345678":
        raise Exception("Invalid Origin Coordinates")
    if destination[0] not in "abcdefgh" or destination[1] not in "12345678":
        raise Exception("Invalid Destination Coordinates")
    return C(ord(origin[0])-97, int(origin[1])-1), C(ord(destination[0])-97, int(destination[1])-1)


@client.event
async def on_message(message: discord.message.Message):
    if message.content.startswith("!chess start"):
        startmsg = await client.send_message(message.channel, "Starting a new chess game.")
        global chessGame
        chessGame = ChessBoard()
        await client.edit_message(startmsg, "{}\n{}".format(startmsg.content, chessGame.show_board()))

    if message.content.startswith("!chess move") and chessGame is not None:
        try:
            origin, destination = parse_move_commands(message.content)
            print("moving from {} to {}".format(origin, destination))
            msg = chessGame.move(origin, destination)
        except InvalidMoveException:
            msg = "You cant move that piece there"
        except:
            msg = "Invalid command. Usage: !chess move origin destination where origin and destination" \
                  " are in chess notation. E.g. a1"
        await client.send_message(message.channel, msg)

client.run(token)