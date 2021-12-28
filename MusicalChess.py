from midiutil import MIDIFile
from pgn_parser import parser, pgn

# example PGN
PGN = """
1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 {This opening is called the Ruy Lopez.}
4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 e4 9. h3 Nb8 10. d4 Nbd7
11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5
Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6
23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5
hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5
35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6
Nf2 42. g4 Bd3 43. Re6 1/2-1/2
"""

# set up midi
tempo = 120
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(0, 0, tempo)

# main function
def pgn_to_midi(PGN: str, separate: bool):
    game = parser.parse(PGN, actions=pgn.Actions())
    time = 0
    for i in range(1, get_total_moves(game)+1):
        ply_to_note(str(game.move(i).white.san), time)
        time += separate
        try:
            ply_to_note(str(game.move(i).black.san), time)
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

def ply_to_note(ply: str, time: int):
    if not "O" in ply:
        instrument = piece_to_instrument(get_piece(ply))
        volume = rank_to_volume(get_rank(ply))
        pitch = add_accidental(file_to_pitch(get_file(ply)), ply)
        # add notes
        MyMIDI.addProgramChange(0, 0, time, instrument)
        MyMIDI.addNote(0, 0, pitch, time, 1, volume)
    else:
        MyMIDI.addProgramChange(0, 0, time, 1)
        MyMIDI.addNote(0, 0, 0, time, 1, 0)
    
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
pgn_to_midi(PGN, False)