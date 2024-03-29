import json

CONFIG_PATH = 'config.json'

class Config:
    _data = None

    def __init__(self):
        if Config._data == None:
            Config.reload()

    @staticmethod
    def reload():
        with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
            Config._data = json.load(f)
        
    def get(self, *keys):
        result = Config._data
        for key in keys:
            result = result[key]
            if result is None:
                return None

        return result

    def get_system_interface(self, *keys):
        return self.get('system', 'interface', *keys)
    
    def get_system_module(self, *keys):
        return self.get('system', 'module', *keys)
    
    def get_use_interface(self, *keys):
        return self.get('use', 'interface', *keys)
    
    def get_use_module(self, *keys):
        return self.get('use', 'module', *keys)
        


config = Config()