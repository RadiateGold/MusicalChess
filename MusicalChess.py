from midiutil import MIDIFile
from pgn_parser import parser, pgn

# example PGN
PGN = """
1. e4 c6 2. d4 d5 3. Nc3 dxe4 4. Nxe4 Nf6 5. Ng3 h5 6. Be2 h4 7. Nf1 Bf5 8. Ne3
Be4 9. Nf3 h3 10. O-O hxg2 11. Nxg2 Qc7 12. Ne5 Nbd7 13. Bf4 Nxe5 14. Bxe5 Qd7
15. c3 Qh3 16. f3 Ng4 17. Bf4 Nxh2 18. fxe4 Nxf1 19. Qxf1 e6 20. Ne3 Qh1+ 21.
Kf2 Qxe4 22. Bg3 Rh6 23. Bf3 Qh7 24. Ng4 Rg6 25. Ne5 Rg5 26. Qg2 Bd6 27. Bxc6+
Ke7 28. Bxb7 Bxe5 29. dxe5 Qc2+ 30. Kg1 Qxg2+ 31. Kxg2 Rb8 32. Ba6 Rxb2+ 33. Kf3
f6 34. Bf4 Rgg2 35. Bc4 Rgc2 36. Rc1 Rxc1 37. Bxc1 Rc2 38. Ba3+ Kf7 39. Bb4 fxe5
40. Ke4 Rc1 41. Kxe5 Re1+ 42. Kd6 g5 43. Bc5 Rd1+ 44. Bd4 Kg6 45. Kxe6 Re1+ 46.
Kd6 a5 47. Kc5 g4 48. Bd3+ Kg5 49. Kb5 Ra1 50. a4 g3 51. Kxa5 g2 52. Kb5 Kf4 53.
a5 Rd1 54. Kc4 Ra1 55. Bb6 Rxa5 56. Bg1 Ra1 57. Bh2+ Ke3 58. Bg6 Rh1 59. Bd6
Rh4+ 60. Kd5 Rd4+ 0-1
"""

# main function
def pgn_to_midi(PGN: str, separate: bool, tempo: float):
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(0, 0, tempo)
    game = parser.parse(PGN, actions=pgn.Actions())
    time = 0
    for i in range(1, get_total_moves(game)+1):
        ply_to_note(str(game.move(i).white.san), time, MyMIDI)
        time += separate
        try:
            ply_to_note(str(game.move(i).black.san), time, MyMIDI)
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