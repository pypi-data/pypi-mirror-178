class BasicEntity:
    def __init__(self, **kw) -> None: ...

class ComparableMixin:
    def __ne__(self, other): ...
    def __eq__(self, other): ...

class ComparableEntity(ComparableMixin, BasicEntity):
    def __hash__(self) -> int: ...
