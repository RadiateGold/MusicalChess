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

with open("test.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    
# helper functions
def piece_to_track(piece: str) -> int:
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
        
    
def rank_to_pitch(rank: str) -> int:
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