# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence


ITEM_ROCK = 'rock'
ITEM_PAPER = 'paper'
ITEM_SCISSORS = 'scissors'


RESULT_YOU_WIN = 6
RESULT_YOU_LOSE = 0
RESULT_DRAW = 3


MAP_LETTERS_TO_ITEMS = {
    'A': ITEM_ROCK,
    'B': ITEM_PAPER,
    'C': ITEM_SCISSORS,
}


MAP_LETTERS_TO_RESULT = {
    'X': RESULT_YOU_LOSE,
    'Y': RESULT_DRAW,
    'Z': RESULT_YOU_WIN,
}


YOUR_SHAPE = {
    ITEM_ROCK: 1,
    ITEM_PAPER: 2,
    ITEM_SCISSORS: 3,
}


GAME_LOGIC = {
    ITEM_ROCK: {'beats': ITEM_SCISSORS, 'defeated_by': ITEM_PAPER},
    ITEM_PAPER: {'beats': ITEM_ROCK, 'defeated_by': ITEM_SCISSORS},
    ITEM_SCISSORS: {'beats': ITEM_PAPER, 'defeated_by': ITEM_ROCK},
}


def get_plays_data(source_file):
    with open(source_file) as f:
        for line in f:
            opponents_play, play_outcome = line[0], line[2]
            yield opponents_play, play_outcome


def get_your_item(opponent_item, result):
    """Get what to play given your opponent's play to get the result"""
    if result == RESULT_DRAW:
        your_item = opponent_item
    elif result == RESULT_YOU_WIN:
        your_item = GAME_LOGIC[opponent_item]['defeated_by']
    else:  # if result == RESULT_YOU_LOSE:
        your_item = GAME_LOGIC[opponent_item]['beats']
    return your_item


def get_total_score(plays_data):
    total_score = 0
    for opponents_play, play_outcome in plays_data:
        opponent_item = MAP_LETTERS_TO_ITEMS[opponents_play]
        result = MAP_LETTERS_TO_RESULT[play_outcome]
        your_item = get_your_item(opponent_item, result)
        total_score += result + YOUR_SHAPE[your_item]
    return total_score


if __name__ == '__main__':
    print(get_total_score(get_plays_data('inputs/part_1_2.txt')))
