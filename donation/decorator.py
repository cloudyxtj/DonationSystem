from .strategy import FilterStrategy

class FilterDecorator(FilterStrategy):
    def __init__(self, base_filter: FilterStrategy):
        self.base_filter = base_filter

    def filter(self, donations):
        return self.base_filter.filter(donations)

class QuantityDecorator(FilterDecorator):
    def __init__(self, base_filter: FilterStrategy, min_quantity=1):
        super().__init__(base_filter)
        self.min_quantity = min_quantity

    def filter(self, donations):
        filtered = super().filter(donations)
        return filtered.filter(quantity__gte=self.min_quantity)

class CategoryDecorator(FilterDecorator):
    def __init__(self, base_filter: FilterStrategy, category):
        super().__init__(base_filter)
        self.category = category

    def filter(self, donations):
        filtered = super().filter(donations)
        return filtered.filter(category=self.category)
