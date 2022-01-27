from midiutil import MIDIFile
import os
import glob

# get the PGN file
path = os.getcwd()
file = glob.glob(os.path.join(path, "*.pgn"))[0]
name = file.split("\\")[-1]
with open(name) as f:
    PGN = f.read()

# main function
def pgn_to_midi(PGN: str, separate: bool, tempo: float):
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(0, 0, tempo)
    moves = pgn_parse(PGN)
    print(moves)
    time = 0
    for i in range(1, len(moves)+1):
        ply_to_note(moves[i]["white"], time, MyMIDI)
        time += separate
        try:
            ply_to_note(moves[i]["black"], time, MyMIDI)
            time += 1
        except:
            continue
    with open("chess music.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

# helper functions
def pgn_parse(pgn: str) -> str:
    game = pgn.split("]")[-1]
    moves = {}
    i = 0
    white = False
    for move in game.split():
        if "." in move:
            i += 1
            moves[i] = {}
            white = True
        elif white:
            moves[i]["white"] = move
            white = False
        else:
            moves[i]["black"] = move
    return moves

def ply_to_note(ply: str, time: int, midi: MIDIFile):
    if not "O" in ply:
        instrument = piece_to_instrument(get_piece(ply))
        volume = rank_to_volume(get_rank(ply))
        pitch = add_accidental(file_to_pitch(get_file(ply)), ply)
        # add notes
        midi.addProgramChange(0, 0, time, instrument)
        midi.addNote(0, 0, pitch, time, 1, volume)
    else:
        midi.addProgramChange(0, 0, time, 1)
        midi.addNote(0, 0, 0, time, 1, 0)

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
    if pitch > 0:
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
pgn_to_midi(PGN, False, 120)