from .schemas import Item, User


class UserDAO(User):
    # wip
    pass

    @classmethod
    def indexes(cls):
        []  # TBD

    @classmethod
    def coll_name(cls) -> str:
        return "users"


class ItemDAO(Item):
    # wip
    pass

    @classmethod
    def indexes(cls):
        []  # TBD

    @classmethod
    def coll_name(cls) -> str:
        return "items"
