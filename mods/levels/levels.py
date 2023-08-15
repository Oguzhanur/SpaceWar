# level/levels.py

def get_json_path(level):
    json_paths = {
        "main1": 'assets//levels//level1.json',
        "main2": 'assets//levels//level2.json',
        "main3": 'assets//levels//level3.json',
        "main4": 'assets//levels//level4.json',
        "main5": 'assets//levels//level5.json',
        1: 'mods//levels//level.json'
    }
    
    return json_paths.get(level)