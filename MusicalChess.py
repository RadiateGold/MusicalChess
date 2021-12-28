from midiutil import MIDIFile
from pgn_parser import parser, pgn

# set up pgn
game = parser.parse("1. e4 e5", actions=pgn.Actions())
print(game.move(1))

# set up midi
track      = 0
channel    = 0
time       = 0   # In beats
duration   = 1   # In beats
tempo      = 60  # In BPM
volume     = 100 # 0-127, as per the MIDI standard
pitch      = 60
instrument = 46

MyMIDI = MIDIFile(2)
MyMIDI.addTempo(track, time, tempo)

#create music
MyMIDI.addProgramChange(0, 0, 0, instrument)
MyMIDI.addNote(track, channel, pitch, time, duration, volume)
time = time + 1



# main function
def ply_to_note(ply: str, time: int):
    instrument = piece_to_instrument(get_piece(ply))
    volume = rank_to_volume(get_rank(ply))
    pitch = file_to_pitch(get_file(ply))
    MyMIDI.addProgramChange(0, 0, 0, instrument)
    MyMIDI.addNote(0, 0, pitch, time, 1, volume)

# helper functions
def get_ply(move: str, color: str) -> str:
    spaces = []
    index = 0
    for char in move:
        if char == " ":
            spaces.append(index)
        index += 1
    if color == "white":
        return move[spaces[0]:spaces[1]]
    elif color == "black":
        return move[spaces[1]:]
    
def get_piece(ply: str) -> str:
    if ply[0] in ["N", "B", "R", "Q", "K"]:
        return ply[0]
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
    else:
        return 41        
    
def rank_to_volume(rank: str) -> int:
    # between 42 and 98
    return int(rank)*8+34

def file_to_pitch(file: str) -> int:
    if file == "A":
        return 45
    elif file == "B":
        return 47
    elif file == "C":
        return 48
    elif file == "D":
        return 50
    elif file == "E":
        return 52
    elif file == "F":
        return 53
    elif file == "G":
        return 55
    else:
        return 0
    
def add_accidental(pitch: int, move: str) -> int:
    if "x" in move:
        pitch -= 1
    elif "+" in move:
        pitch += 1
    elif "#" in move:
        pitch += 2
    return pitch

# testing
ply_to_note("Ba1", 0)
with open("test.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)