from typing import Dict, Callable

class Router:
    """
    Класс для более комфортного контроля сообщений
    """
    
    def __init__(self):
        self.routes: Dict[str, Callable] = {}

    def handle(self, text: str):
        def get_func(func: Callable):
            async def none_wrapper():
                return None
            self.routes.update(
                {text: func}
            )
            return none_wrapper
        return get_func

    async def check(self, message):
        func = self.routes.get(message.text.lower())
        if func is not None:
            await func(message)
