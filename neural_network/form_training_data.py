import pickle

# inputs is a list of all the states of the board during the game
# output for each play is five lists of boolean values:
# unavailable: bool[60] - cards somewhere on the board
# yours: bool[60] - what cards (up to 3) are on your side
# theirs: bool[60] - what cards (up to 3) are on the opponent's side
# hand: bool[60] - what cards are in your hand
# winner: bool - whether you won the flag
def plays_as_bitsets(boards, hands, plays, flags):
    training_data = []
    for i in range(0, len(boards)):
        playColumn = plays[i]['target']
        if flags[playColumn] == None:
            continue
        columnWinner = flags[playColumn]
        sample = {'x': []}
        sample['x'].append(board_to_bitset(boards[i]))
        sample['x'].append(hand_to_bitset(boards[i][playColumn][i%2]))
        sample['x'].append(hand_to_bitset(boards[i][playColumn][(i+1)%2]))
        sample['x'].append(hand_to_bitset(hands[i]))
        # 1 if the column winner is current player
        sample['y'] = (i + flags[playColumn] + 1)%2
        training_data.append(sample)
    return training_data

# board is a list of 9 columns,
def board_to_bitset(board):
    bitset = [0]*60
    for column in board:
        for side in column:
            for card in side:
                bitset[flat_value(vectorize(card))] = 1
    return bitset

def hand_to_bitset(hand):
    bitset = [0]*60
    for card in hand:
        try:
            bitset[flat_value(vectorize(card))] = 1
        except ValueError: # player drew tactics, ignore that card
          pass
    return bitset

# card as [0:9] x [0:6]
# return 0:59
def flat_value(card):
    return card[0] + card[1]*10

# convert card names to 2D vectors
# set of colors is rogbpy, convert that to 0-5
# for example, "0y" => (0, 5)
#
def vectorize(card):
    return [int(card[0]), 'roygbp'.find(card[1])]

# convert raw data into training samples
# training samples will be of the form
# sample = {
#   y: 0 or 1
#   x: 4x60 array of 0s and 1s
# }
#
# to run this, first run from the outer directory
#   python3 ./bl_wrapper.py ocd naive -n 10
# this will generate the raw_data.pickle file.  Then do
#   cd neural_network
#   
with open("raw_data.pickle",'rb') as input, open("training_samples.txt", 'a') as output:
    game_number = 1
    while True:
        try:
             line = pickle.load(input)
        except EOFError:
            break
        print("processing game number " + str(game_number))
        boards = line['rounds']
        hands = line['hands']
        plays = line['plays']
        flags = line['flags']
        winner = line['winner']
        #print("line: ", line)
        data = plays_as_bitsets(boards, hands, plays, flags)
        for sample in data:
          output.write(str(sample) + "\n")
        game_number += 1
