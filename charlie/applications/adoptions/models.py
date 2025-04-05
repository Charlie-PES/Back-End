from pymongo import IndexModel

from schemas import AdoptionIn


class AdoptionDAO(AdoptionIn):
    # TBD
    pass

    # TBD
    @classmethod
    def indexes(cls):
        [IndexModel(...)]  # TBD
