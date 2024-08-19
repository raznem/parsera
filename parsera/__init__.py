from parsera.main import Parsera

__all__ = ["Parsera", "ParseraHuggingFace"]

def __getattr__(name):
    if name == "ParseraHuggingFace":
        from parsera.main import ParseraHuggingFace
        return ParseraHuggingFace
    raise AttributeError(f"module 'parsera' has no attribute '{name}'")