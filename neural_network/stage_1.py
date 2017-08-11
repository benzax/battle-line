import pickle

def process(inputs, label):
    print("processing")
    print(inputs)
    print(label)
    for datum in inputs:
        values = []
        for column in datum:
            for side in column:
                for card in side:
                    values.extend(vectorize(card))
                values += [-1]*(6 - 2*len(side))
    print(" ".join(str(v) for v in values) + " " + str(label))

# convert card names to 2D vectors
# set of colors is rogbpy, convert that to 0-5
# for example, "0y" => (0, 5)
#
def vectorize(card):
    return [int(card[0]), 'rogbpy'.find(card[1])]

with open("raw_data.pickle",'rb') as input:
    data = []
    while True:
        try:
             line = pickle.load(input)
        except EOFError:
            break
        data = line['rounds']
        flags = line['flags']
        winner = line['winner']
        #print("line: ", line)
        process(data, winner)
            


