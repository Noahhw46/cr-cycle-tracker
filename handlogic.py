
def update_hand(prev_hand, card_played):
    #Move the played card to the end of the hand
    try:
        prev_hand.remove(card_played)
    except ValueError:
        prev_hand.remove("questionmark")
    prev_hand.append(card_played)
    return prev_hand

def init_hand():
    #Since we don't know the positions of any of the cards in the deck, we initialize the hand with question marks in all positions.
    hand = ["questionmark" for _ in range(8)]
    return hand