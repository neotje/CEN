import os

UIU_DEBUG = "UIU_DEBUG"
UIU_WITHOUT_UI = "UIU_DISABLE_UI"
UIU_UI_SERVER = "UIU_SERVER_ADDR"
UIU_FULLSCREEN = "UIU_FULLSCREEN"

def setup():
    os.environ.setdefault(UIU_DEBUG, str(False))
    os.environ.setdefault(UIU_WITHOUT_UI, str(False))
    os.environ.setdefault(UIU_UI_SERVER, "")
    os.environ.setdefault(UIU_FULLSCREEN, str(False))

def getBool(key: str) -> bool:
    return os.environ.get(key).lower() in ['true', '1']

def getStr(key: str) -> str:
    return os.environ.get(key)