"""Library of generic functions to make writing AI players easier.

Feel free to add to this file.  If a function is so specific that only one bot
will use it, however, then it doesn't belong here."""

from bl_classes import * # Need to import?  Do it in bl_classes.py.

def possible_straights(cards, formationSize=FORMATION_SIZE):
        """Return a seq of conceivable straight continuations."""
        minVal, maxVal = int(TROOP_CONTENTS[0]), int(TROOP_CONTENTS[-1])
        allStraights = [range(i, i + formationSize)
                        for i in range(minVal, maxVal - formationSize + 2)]

        cardValues = [int(card[0]) for card in cards]

        out = []
        for straight in allStraights:
            for value in cardValues:
                if value not in straight:
                    break
            else:
                possibleStraight = list(straight)
                for value in set(cardValues): # Skip already played cards.
                    possibleStraight.remove(value)
                out.append(list(map(str, possibleStraight)))

        return list(reversed(out)) # Strongest first

def check_formation_components(cards, formationSize=FORMATION_SIZE):
        straight, triple, flush = False, False, False

        l = len(cards)
        if l > 1:
            values, suits = [c[0] for c in cards], [c[1] for c in cards]
            values.sort()

            spacing = [int(values[i+1]) - int(values[i]) for i in range(l-1)]
            if spacing.count(0) == l-1:
                triple = True
            elif 0 not in spacing and sum(spacing) <= formationSize - 1:
                straight = True

            if suits.count(suits[0]) == l:
                flush = True

            return straight, triple, flush

        else: # With 0 or 1 cards played, all formations are still conceivable.
            return True, True, True

def detect_formation(cards): # Assume wilds pre-specified
        l = len(cards)
        assert 3 <= l <= 4 # Allow for Mud.

        straight, triple, flush = check_formation_components(cards, len(cards))

        if straight and flush:
            fType = 'straight flush'
        elif triple:
            fType = 'triple'
        elif flush:
            fType = 'flush'
        elif straight:
            fType = 'straight'
        else:
            fType = 'sum'

        return {'cards':cards,
                'type':fType,
                'strength':sum([int(c[0]) for c in cards])}

def compare_formations(formations, whoseTurn):
        ranks = [POKER_HIERARCHY.index(f['type']) for f in formations]
        if ranks[0] != ranks[1]:
            return ranks.index(min(ranks))
        else: # Same formation type
            strengths = [f['strength'] for f in formations]
            if strengths[0] != strengths[1]:
                return strengths.index(max(strengths))
            else: # Identical formations, but current player finished 2nd
                return 1 - whoseTurn

def is_playable(r, tacticsCard):
    if tacticsCard in ('Fo', 'Mu'):
        return True

    if tacticsCard == 'Sc':
        return len(r.decks['troop']) + len(r.decks['tactics']) >= 3

    if tacticsCard in ('Al', 'Da'):
        if r.playedLeader == r.whoseTurn:
            return False

    me = r.whoseTurn
    myEmpty = [i for i, f in enumerate(r.flags)
               if f.winner == None and len(f.played[me]) < 3]

    if tacticsCard in ('Al', 'Da', 'Sh', 'Co'):
        return myEmpty != []

    yourFull = [i for i, f in enumerate(r.flags)
                if f.winner == None and len(f.played[1 - me]) > 0]
    
    if tacticsCard == 'De':
        return yourFull != []

    if tacticsCard == 'Tr':
        return yourFull != [] and myEmpty != []

    myFull = [i for i, f in enumerate(r.flags)
              if f.winner == None and len(f.played[me]) > 0]

    if tacticsCard == 'Re':
        return myFull != []
