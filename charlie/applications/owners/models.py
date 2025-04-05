from pymongo import IndexModel

from owners.schemas import UserIn


class OwnerDAO(UserIn):
    # TBD
    pass

    @classmethod
    def indexes(cls):
        [IndexModel("email", unique=True)]
