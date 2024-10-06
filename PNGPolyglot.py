import chess.pgn
from openai import OpenAI
import re

def read_config(config_file):
    # (Same as before)
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip()
    return config

def collect_comments(node, comments_list, path):
    # (Same as before)
    if node.starting_comment:
        comments_list.append({'comment': node.starting_comment, 'path': path.copy(), 'type': 'starting_comment'})
    if node.comment:
        comments_list.append({'comment': node.comment, 'path': path.copy(), 'type': 'comment'})
    for i, variation in enumerate(node.variations):
        path.append(i)
        collect_comments(variation, comments_list, path)
        path.pop()

def set_translated_comments(node, comments_list, translated_comments, index, path):
    # (Same as before)
    if index[0] >= len(translated_comments):
        # No more translations available
        return
    if node.starting_comment:
        if comments_list[index[0]]['path'] == path and comments_list[index[0]]['type'] == 'starting_comment':
            node.starting_comment = translated_comments[index[0]]
            index[0] += 1
    if node.comment:
        if comments_list[index[0]]['path'] == path and comments_list[index[0]]['type'] == 'comment':
            node.comment = translated_comments[index[0]]
            index[0] += 1
    for i, variation in enumerate(node.variations):
        path.append(i)
        set_translated_comments(variation, comments_list, translated_comments, index, path)
        path.pop()

def split_comments_into_batches(comments, max_comments_per_batch=10):
    # (Same as before)
    batches = []
    for i in range(0, len(comments), max_comments_per_batch):
        batches.append(comments[i:i + max_comments_per_batch])
    return batches

def translate_comments_batch(comments, model, target_language, client):
    """
    Translates a list of comments into the target language using the OpenAI API.
    """
    # Prepare the prompt with all comments
    comments_text = '\n\n'.join([f"{i+1}. {comment['comment']}" for i, comment in enumerate(comments)])
    prompt = f"Translate the following chess annotations from English to {target_language}. Preserve all chess notation, symbols, and formatting. Provide the translations numbered accordingly.\n\n{comments_text}"

    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates chess annotations from English to {target_language}. Ensure that each translation starts with the corresponding number and a period."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1500,
            n=1,
            temperature=0.3,
        )
        translated_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during translation API call: {e}")
        return [comment['comment'] for comment in comments]  # Return original comments

    # Parse the translated text back into a list
    translated_comments = parse_translated_text(translated_text, len(comments))

    return translated_comments

def parse_translated_text(translated_text, expected_count):
    # (Same as before)
    pattern = re.compile(r'^(\d+)\.\s*(.*)', re.MULTILINE)
    matches = pattern.findall(translated_text)
    translations = [''] * expected_count
    for num_str, text in matches:
        num = int(num_str)
        if 1 <= num <= expected_count:
            translations[num - 1] += text.strip()
        else:
            print(f"Warning: Found translation for unexpected comment number {num}.")
    # Check for missing translations
    for i in range(expected_count):
        if not translations[i]:
            print(f"Warning: Translation for comment {i+1} not found.")
            translations[i] = ''  # Or use the original comment if desired
    return translations

def process_pgn(input_pgn, output_pgn, model, target_language, client):
    with open(input_pgn, 'r', encoding='utf-8') as f_in, open(output_pgn, 'w', encoding='utf-8') as f_out:
        game_number = 0
        while True:
            game = chess.pgn.read_game(f_in)
            if game is None:
                break
            game_number += 1
            event = game.headers.get('Event', 'Unknown Event')
            site = game.headers.get('Site', 'Unknown Site')
            date = game.headers.get('Date', 'Unknown Date')
            white = game.headers.get('White', 'White')
            black = game.headers.get('Black', 'Black')
            print(f"\nProcessing Game {game_number}: {white} vs {black}, {event}, {site}, {date}")

            comments_list = []
            collect_comments(game, comments_list, [])

            if comments_list:
                print(f"Translating {len(comments_list)} comments...")
                # For games with a large number of comments, process individually
                if len(comments_list) > 50:
                    print("Large number of comments detected. Translating comments individually.")
                    translated_comments = []
                    for i, comment in enumerate(comments_list):
                        print(f"Translating comment {i+1}/{len(comments_list)}")
                        translation = translate_comments_batch([comment], model, target_language, client)
                        translated_comments.extend(translation)
                else:
                    # Split comments into batches
                    batches = split_comments_into_batches(comments_list, max_comments_per_batch=10)
                    translated_comments = []
                    for batch_num, batch in enumerate(batches):
                        print(f"Translating batch {batch_num+1}/{len(batches)} with {len(batch)} comments...")
                        batch_translations = translate_comments_batch(batch, model, target_language, client)
                        translated_comments.extend(batch_translations)
                # Set the translated comments back into the game
                index = [0]
                set_translated_comments(game, comments_list, translated_comments, index, [])
            else:
                print("No comments to translate in this game.")

            print(game, file=f_out, end="\n\n")
        print(f"\nTranslation completed. Translated PGN saved to {output_pgn}.")

def main():
    # Read configuration
    config = read_config('config.txt')
    api_key = config.get('API_KEY')
    model_version = config.get('MODEL_VERSION', 'gpt-3.5-turbo')
    target_language = config.get('TARGET_LANGUAGE', 'Russian')

    # Input and output PGN files
    input_pgn = config.get('INPUT_PGN', 'input.pgn')
    output_pgn = config.get('OUTPUT_PGN', 'output_translated.pgn')

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Process the PGN file
    process_pgn(input_pgn, output_pgn, model_version, target_language, client)

if __name__ == '__main__':
    main()