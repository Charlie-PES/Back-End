from pymongo import IndexModel

from owners.schemas import OwnerIn


class OwnerDAO(OwnerIn):
    # TBD
    pass

    @classmethod
    def indexes(cls):
        [IndexModel("email", unique=True)]
