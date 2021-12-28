from midiutil import MIDIFile
from pgn_parser import parser, pgn

# set up midi
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(0, 0, 60)

# main function
def pgn_to_midi(PGN: str):
    game = parser.parse(PGN, actions=pgn.Actions())
    time = 0
    for i in range(1, get_total_moves(game)):
        ply_to_note(get_ply(str(game.move(i)), "white"), time)
        time += 1
        try:
            ply_to_note(get_ply(str(game.move(i)), "black"), time)
            time += 1
        except:
            continue
    with open("test.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

# helper functions
def get_total_moves(game: str) -> int:
    ended = False
    move = 1
    while not ended:
        try:
            game.move(move)
        except:
            ended = True
            return move - 1
        finally:
            move = move + 1

def get_ply(move: str, color: str) -> str:
    spaces = []
    index = 0
    # find where the spaces are
    for char in move:
        if char == " ":
            spaces.append(index)
        index += 1
    # return the appropriate ply
    if color == "white":
        return move[spaces[0]:spaces[1]]
    elif color == "black":
        return move[spaces[1]:]

def ply_to_note(ply: str, time: int):
    instrument = piece_to_instrument(get_piece(ply))
    volume = rank_to_volume(get_rank(ply))
    pitch = add_accidental(file_to_pitch(get_file(ply)), ply)
    # add notes
    MyMIDI.addProgramChange(0, 0, time, instrument)
    MyMIDI.addNote(0, 0, pitch, time, 1, volume)
    
def get_piece(ply: str) -> str:
    if ply[0] in ["N", "B", "R", "Q", "K"]:
        return ply[0]
    # otherwise pawn
    else:
        return ""

def get_rank(ply: str) -> str:
    back_index = 0
    # if check or checkmate
    if "+" in ply or "#" in ply:
        back_index += 1
    # if promotion
    if "=" in ply:
        back_index += 2
    return ply[-1-back_index]

def get_file(ply: str) -> str:
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    index = 1
    # if capture
    if "x" in ply:
        index += 1
    # if pawn move
    if not ply[0] in ["N", "B", "R", "Q", "K"]:
        index -= 1
    # if disambiguating notation
    if ply[index+1] in files:
        index += 1
    return ply[index]    

def piece_to_instrument(piece: str) -> int:
    if piece == "N":
        return 109
    elif piece == "B":
        return 14
    elif piece == "R":
        return 114
    elif piece == "Q":
        return 52
    elif piece == "K":
        return 3
    # pawn
    else:
        return 41        
    
def rank_to_volume(rank: str) -> int:
    # between 50 and 106
    return int(rank)*8+42

def file_to_pitch(file: str) -> int:
    if file == "a":
        return 45
    elif file == "b":
        return 47
    elif file == "c":
        return 48
    elif file == "d":
        return 50
    elif file == "e":
        return 52
    elif file == "f":
        return 53
    elif file == "g":
        return 55
    # h file becomes rest
    else:
        return 0
    
def add_accidental(pitch: int, ply: str) -> int:
    if "x" in ply:
        pitch -= 1
    if "=" in ply:
        pitch -= 2
    if "+" in ply:
        pitch += 1
    if "#" in ply:
        pitch += 2
    return pitch

# testing
pgn_to_midi("1. e4 d5 2. Nf3 Nc6 3. Bb5 a6")