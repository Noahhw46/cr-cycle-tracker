import json

red_cards = {'evolved_bats_star': [(150, 298), (261, 455)], 'evolved_bomber': [(404, 2209), (521, 2363)], 'elixerpump': [(397, 301), (516, 454)], 'tornado': [(1031, 2210), (1165, 2369)], 'goldenknight': [(525, 2214), (650, 2369)], 'skeletonking': [(269, 303), (390, 454)], 'evolved_skeletons': [(776, 295), (899, 455)], 'evolved_skeletons_2': [(780, 2211), (903, 2371)], 'goblindrill': [(149, 2210), (266, 2364)], 'elixergolem': [(901, 297), (1032, 459)], 'tesla': [(908, 2210), (1027, 2360)], 'arrows': [(524, 296), (649, 452)], 'poison': [(274, 2208), (396, 2362)], 'firespirit': [(654, 2205), (779, 2361)], 'nightwitch': [(654, 296), (771, 455)], 'rage': [(1032, 294), (1157, 450)]}
blue_cards = {'evolved_bats_star': [(150, 298), (261, 455)], 'evolved_bomber': [(404, 2209), (521, 2363)], 'elixerpump': [(397, 301), (516, 454)], 'tornado': [(1031, 2210), (1165, 2369)], 'goldenknight': [(525, 2214), (650, 2369)], 'skeletonking': [(269, 303), (390, 454)], 'evolved_skeletons': [(776, 295), (899, 455)], 'evolved_skeletons_2': [(780, 2211), (903, 2371)], 'goblindrill': [(149, 2210), (266, 2364)], 'elixergolem': [(901, 297), (1032, 459)], 'tesla': [(908, 2210), (1027, 2360)], 'arrows': [(524, 296), (649, 452)], 'poison': [(274, 2208), (396, 2362)], 'firespirit': [(654, 2205), (779, 2361)], 'nightwitch': [(654, 296), (771, 455)], 'rage': [(1032, 294), (1157, 450)]}

def convert_coords(cards):
    return [[tl[0], tl[1], br[0], br[1]] for tl, br in cards.values()]

red_rects = convert_coords(red_cards)
blue_rects = convert_coords(blue_cards)

final_dict = {
    "rect1": red_rects,
    "rect2": blue_rects
}


json_output = json.dumps(final_dict)

with open('goodcards.json', 'w') as f:
    f.write(json_output)
