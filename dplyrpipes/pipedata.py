
import dataclasses
from typing import Callable, Any


class out:
    '''Ends the pipeline by returning the .data property of PipeData.'''
    pass

@dataclasses.dataclass
class PipeData:
    '''Store data and overload operator to apply component functions.'''
    data: Any

    def __rshift__(self, func: Callable):
        '''Apply a callable on the right to the data.
        '''
        if isinstance(func, out):
            return self.data
        if hasattr(func, 'argdata') and hasattr(func, 'kwargdata'):
            return self.__class__(func(self.data, *func.argdata, **func.kwargdata))
        else:
            return self.__class__(func(self.data))

    