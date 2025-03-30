# Import the Django template module to register custom template filters
from django import template

# Create an instance of template.Library to register custom filters
register = template.Library()


# Decorator to register the function as a custom filter in Django templates
@register.filter
def get_item(dictionary, key):
    # Return the value for the given key in the dictionary, or None if the key does not exist
    return dictionary.get(key)
