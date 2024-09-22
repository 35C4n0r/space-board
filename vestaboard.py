import json
import os
import requests

VESTABOARD_API_URL = os.getenv('VESTABOARD_API_URL')
headers = {
    'X-Vestaboard-Read-Write-Key': os.getenv('VESTABOARD_API_KEY')
}

# Character mapping for Vestaboard
char_to_code = {
    ' ': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
    'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
    '1': 27, '2': 28, '3': 29, '4': 30, '5': 31, '6': 32, '7': 33, '8': 34, '9': 35, '0': 36, '!': 37, '@': 38, '#': 39,
    '$': 40, '(': 41, ')': 42, '-': 44, '+': 46, '&': 47, '=': 48, ';': 49, ':': 50, "'": 52, '"': 53, '%': 54, ',': 55,
    '.': 56, '/': 59, '?': 60, '°': 62, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
    'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23,
    'x': 24, 'y': 25, 'z': 26
}


def format_message_for_grid(content, line_lengths, max_lines=5):
    print("s", content)
    words = content.split()
    lines = []
    current_line = ""
    line_idx = 0

    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) > line_lengths[line_idx]:
            # If adding the word exceeds the current line's capacity, move to the next line
            lines.append(current_line)
            current_line = word
            line_idx += 1

            if line_idx >= max_lines:
                lines[-1] = lines[-1][:line_lengths[line_idx - 1] - 3] + '...'  # add ellipsis if it exceeds max lines
                break
        else:
            # Add the word to the current line
            if current_line:
                current_line += " " + word
            else:
                current_line = word

    if line_idx < max_lines:
        lines.append(current_line)  # append the last line if it didn't exceed

    return lines


def format_twitter_message(message):
    print(message)
    content = " ".join(format_message_for_grid(message["content"], line_lengths=[22, 22, 22, 22, 22]))
    author = message["user"]
    if len(author) > 22:
        author = author[:22 - 3] + "..."
    return {
        "components": [
            {
                "style": {
                    "justify": "center",
                    "align": "center",
                    "width": 22,
                    "height": 5
                },
                "template": f"{content}"
            },
            {
                "style": {
                    "align": "bottom",
                    "justify": "right",
                    "width": 20,
                    "height": 1
                },
                "template": f"@{author}"
            },
            {
                "style": {
                    "width": 1,
                    "height": 1,
                    "absolutePosition": {
                        "x": 21,
                        "y": 5
                    },
                },
                "template": "{67}"
            }
        ]
    }


def format_rest_message(message, color):
    content = " ".join(format_message_for_grid(message, line_lengths=[22, 22, 22, 22, 22, 20], max_lines=6))

    return {
        "components": [
            {
                "style": {
                    "justify": "center",
                    "align": "center",
                    "width": 22,
                    "height": 6
                },
                "template": f"{content}"
            },
            {
                "style": {
                    "width": 1,
                    "height": 1,
                    "absolutePosition": {
                        "x": 21,
                        "y": 5
                    },
                },
                "template": f"{{{color}}}"
            }
        ]
    }


def create_vestaboard_message(title):
    # Initialize the board with empty values
    message_layout = [[0 for _ in range(22)] for _ in range(6)]

    words = title.split(' ')
    current_row = []
    current_line_length = 0

    temp_message_layout = []

    for word in words:
        word = word.replace("’", "'")  # Replace special apostrophe with a regular one
        word_length = len(word)

        # If the word fits in the current line, add it
        if current_line_length + word_length <= 22:
            current_row.append(word)
            current_line_length += word_length + 1  # +1 for the space
        else:
            # Calculate the number of spaces needed to center-align the line
            line = ' '.join(current_row)
            if len(line) > 22:
                line = line[:22]  # Truncate if the line is too long
            num_spaces = (22 - len(line)) // 2

            # Place the current row on the temp board with centered alignment
            temp_row = [0] * 22
            start_index = num_spaces
            for i, char in enumerate(line):
                if start_index + i < 22:  # Ensure no overflow
                    temp_row[start_index + i] = char_to_code.get(char, 0)
            temp_message_layout.append(temp_row)

            # Start the new row with the current word
            current_row = [word]
            current_line_length = word_length + 1

    # Add any remaining words in the current row
    if current_row:
        line = ' '.join(current_row)
        if len(line) > 22:
            line = line[:22]  # Truncate if the line is too long
        num_spaces = (22 - len(line)) // 2
        temp_row = [0] * 22
        start_index = num_spaces
        for i, char in enumerate(line):
            if start_index + i < 22:
                temp_row[start_index + i] = char_to_code.get(char, 0)
        temp_message_layout.append(temp_row)

    # Determine the starting row based on the number of rows in temp_message_layout
    num_rows = len(temp_message_layout)
    start_row = max(0, (6 - num_rows) // 2)  # Center the text vertically

    # Copy temp_message_layout to message_layout starting from start_row
    for i in range(min(num_rows, 6)):
        message_layout[start_row + i] = temp_message_layout[i]

    # Add red tile in the bottom-right-hand corner (character code 63)
    message_layout[-1][-1] = 63

    return message_layout


def push_to_vestaboard(message, source: str):
    if source == "twitter":
        vba_data = format_twitter_message(message=message)
        print(json.dumps(vba_data))
    elif source == "aidy":
        vba_data = format_rest_message(message=message, color=64)
    elif source == "supercluster":
        vba_data = format_rest_message(message=message, color=65)
    elif source == "spacenews":
        vba_data = format_rest_message(message=message, color=63)

        print(json.dumps(vba_data))
    # return
    try:
        layout_response = requests.post('https://vbml.vestaboard.com/compose', headers=headers, json=vba_data)
        # print(layout_response.json())
        # layout_response.raise_for_status()

        vestaboard_response = requests.post('https://rw.vestaboard.com/', headers=headers, json=layout_response.json())
        print("QQ", vestaboard_response.text)
        # vestaboard_response.raise_for_status()


    except Exception as e:
        print(e)
