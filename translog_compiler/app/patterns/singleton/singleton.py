"""Patrón Singleton: una sola instancia por clase."""


class Singleton(type):
    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instancias:
            Singleton._instancias[cls] = super().__call__(*args, **kwargs)
        return Singleton._instancias[cls]

    def reiniciar(cls):
        """Solo para pruebas: descarta la instancia actual."""
        Singleton._instancias.pop(cls, None)
