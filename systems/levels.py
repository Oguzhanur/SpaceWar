# systems/levels.py

def get_json_path(level):
    json_paths = {
        1: 'systems//level1.json',
        2: 'systems//level2.json',
        3: 'systems//level3.json',
        4: 'systems//level4.json',
        5: 'systems//level5.json'
    }

    return json_paths.get(level, '')
