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
    'X': ITEM_ROCK,
    'Y': ITEM_PAPER,
    'Z': ITEM_SCISSORS,
}


YOUR_SHAPE = {
    ITEM_ROCK: 1,
    ITEM_PAPER: 2,
    ITEM_SCISSORS: 3,
}


def get_plays_data(source_file):
    with open(source_file) as f:
        for line in f:
            opponent_play, your_play = line[0], line[2]
            yield opponent_play, your_play


def get_result(opponent_item, your_item):
    """Get the result of the interaction between opponent's and your items"""
    if opponent_item == your_item:
        result = RESULT_DRAW
    elif (
        opponent_item == ITEM_ROCK and your_item == ITEM_SCISSORS
        or opponent_item == ITEM_SCISSORS and your_item == ITEM_PAPER
        or opponent_item == ITEM_PAPER and your_item == ITEM_ROCK
    ):
        result = RESULT_YOU_LOSE
    else:
        result = RESULT_YOU_WIN
    return result


def get_total_score(plays_data):
    total_score = 0
    for opponent_play, your_play in plays_data:
        opponent_item = MAP_LETTERS_TO_ITEMS[opponent_play]
        your_item = MAP_LETTERS_TO_ITEMS[your_play]
        result = get_result(opponent_item, your_item)
        total_score += result + YOUR_SHAPE[your_item]
    return total_score


if __name__ == '__main__':
    print(get_total_score(get_plays_data('inputs/part_1_2.txt')))
