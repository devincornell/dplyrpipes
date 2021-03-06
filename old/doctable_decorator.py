# I used this formula for the decorator: https://realpython.com/primer-on-python-decorators/#both-please-but-never-mind-the-bread
# outer function used to handle arguments to the decorator
# e.g. @doctable.schema(require_slots=True)
def schema(_Cls=None, *, require_slots=True, **dataclass_kwargs):

    # this is the actual decorator
    def decorator_schema(Cls):
        # creates constructor/other methods using dataclasses
        Cls = dataclasses.dataclass(Cls, **dataclass_kwargs)
        if require_slots and not hasattr(Cls, '__slots__'):
            raise SlotsRequiredError()

        # add slots
        @functools.wraps(Cls, updated=[])
        class NewClass(DocTableSchema, Cls):
            __slots__ = [f.name for f in dataclasses.fields(Cls)]
        
        return NewClass

    if _Cls is None:
        return decorator_schema
    else:
        return decorator_schema(_Cls)


if __name__ == '__main__':
    