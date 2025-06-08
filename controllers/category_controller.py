from repositories.category_repository import CategoryRepository

class CategoryController:
    def __init__(self):
        self.category_repo = CategoryRepository()

    def get_category(self):
        return self.category_repo.get_category()
    
    def create_category(self, categ_name):
        return self.category_repo.create_category(categ_name)
    
    def get_categ_by_id(self, categ_id):
        return self.category_repo.get_categ_by_id(categ_id)

    