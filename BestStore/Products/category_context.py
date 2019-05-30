from .models import CATEGORY_CHOICES, SUB_CATEGORY_CHOICES


def add_category_context(request):
    """Gives the context for categories to display on every page"""

    return {'category_choices': CATEGORY_CHOICES,
            'sub_category_choices': SUB_CATEGORY_CHOICES}
