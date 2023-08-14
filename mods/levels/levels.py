# level/levels.py

def get_json_path(level):
    json_paths = {
        1: 'mods//levels//level1.json',
        2: 'mods//levels//level2.json',
        3: 'mods//levels//level3.json',
        4: 'mods//levels//level4.json',
        5: 'mods//levels//level5.json'
    }
    
    return json_paths.get(level)
