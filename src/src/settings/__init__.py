from .production import *  #на сервере загрузятся production настройки
try:
    from .local_settings import *  #на локальном компьютере загрузятся local_settings
except ImportError:
    pass