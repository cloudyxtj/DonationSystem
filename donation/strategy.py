from abc import ABC, abstractmethod

class FilterStrategy(ABC):
    @abstractmethod
    def filter(self, queryset):
        pass

class ExpiryDateFilter(FilterStrategy):
    def filter(self, queryset):
        return queryset.order_by('expiry_date')

class QuantityFilter(FilterStrategy):
    def filter(self, queryset):
        return queryset.order_by('-quantity') # descending order

# class CategoryFilter(FilterStrategy):
#     def __init__(self, category):
#         self.category = category

#     def filter(self, donations):
#         return donations.filter(category=self.category)
    
class FilterContext:
    def __init__(self, strategy: FilterStrategy):
        self.strategy = strategy

    def apply_filter(self, queryset):
        return self.strategy.filter(queryset)