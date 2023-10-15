from abc import ABC, abstractmethod


class UITextElement(ABC):
    
    @abstractmethod
    def terminal_representation(self)->str:
        pass

    @abstractmethod
    def terminal_representation_length(self)->int:
        pass
