# level/levels.py

def get_json_path(level):
    json_paths = {
        1: 'assets//levels//level1.json',
        2: 'assets//levels//level2.json',
        3: 'assets//levels//level3.json',
        4: 'assets//levels//level4.json',
        5: 'assets//levels//level5.json',
        6: 'mods//levels//level.json'
    }
    
    return json_paths.get(level)
