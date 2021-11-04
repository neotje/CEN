import os

UIU_DEBUG = "UIU_DEBUG"
UIU_WITHOUT_UI = "UIU_DISABLE_UI"
UIU_UI_SERVER = "UIU_UI_SERVER_ADDR"
UIU_FULLSCREEN = "UIU_FULLSCREEN"

def setup():
    os.environ.setdefault(UIU_DEBUG, str(False))
    os.environ.setdefault(UIU_WITHOUT_UI, str(False))
    os.environ.setdefault(UIU_UI_SERVER, "")
    os.environ.setdefault(UIU_FULLSCREEN, str(True))

def getBool(key: str) -> bool:
    value = os.environ.get(key)

    if value is None:
        return False
    
    return value.lower() in ['true', '1', '']

def getStr(key: str) -> str:
    return os.environ.get(key)