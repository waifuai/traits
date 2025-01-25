import populate_traits_db
from trait_dao import TraitDAO

if __name__ == '__main__':
    trait_db = TraitDAO()
    trait_db.reset_database()
    populate_traits_db.populate_traits_db()