def cfgEntity(cfg) -> dict:
    return {
        "config_description": cfg["config_description"],
        "data": cfg["data"]
    }
    

def cfgListEntity(configs) -> dict:
    return [cfgEntity(cfg) for cfg in configs]