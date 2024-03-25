import yaml

def load_config(config_path: str):
    try:
        with open(config_path, 'r') as f:
            return yaml.load(f, yaml.CLoader)
    except FileNotFoundError:
        # return 
        print(f"{config_path} not found")
        exit()

CONFIG_PATH = './config.yaml'

config = load_config(CONFIG_PATH)


def is_loaded() -> bool:
    print(config)
    return config != None
        


class LiveConfig:
    ROOM_ID = config['live']['roomId']
    
class LLMConfig:
    __LLM_CONFIG = config['module']['llm']

    __GPT_CONFIG = __LLM_CONFIG['gpt']
    
    GPT_API_KEY = __GPT_CONFIG['apiKey']
    GPT_BASE_URL = __GPT_CONFIG['url'] \
        if (__GPT_CONFIG['url']) != '' else None