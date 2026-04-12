import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "debbie" / "config.json"

def load_config():
    """
    Carga configuración del archivo.
    El campo 'language' es opcional: si está guardado se respeta;
    si no existe, debbie.py usará la detección automática de translations.py.
    """
    default_config = {
        'autostart': True,
        # 'language' no se incluye aquí a propósito: si el usuario nunca
        # eligió un idioma manualmente, translations.py detecta el del sistema.
    }
    
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                
                # Solo añadir claves faltantes del default
                for key, value in default_config.items():
                    if key not in user_config:
                        user_config[key] = value
                
                return user_config
        else:
            save_config(default_config)
            return default_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

def save_config(config_data):
    """
    Guarda configuración al archivo.
    Acepta cualquier dict (incluyendo 'language' si fue añadido por la app).
    """
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False