import json 

# def parse_cors(cors_str:str | list[str]):
def parse_cors(cors:str )->str | list[str]:
    if isinstance(cors,str) and not cors.startswith("["):
        return [cor.strip() for cor in cors.split(",") ] 
    elif isinstance(cors , str | list):
        return cors
        
    raise ValueError(f"{cors}")    
    