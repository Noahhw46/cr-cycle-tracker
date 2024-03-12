def color_print(color, text):
    if color == "red":
        print(f"\033[91m{text}\033[00m")
    elif color == "blue":
        print(f"\033[94m{text}\033[00m")

def print_template_sizes(templates):
    for template_name, template in templates.items():
        print(f"Template {template_name} has size {template.shape[0]}, {template.shape[1]}.")

def print_hand(color, hand):
    color_print(color, f"{color} players hand: {hand}")
    print()