from django import template

register = template.Library()

@register.filter
def calculate_total_price(quotation_items):
    total_price = 0
    for quotation_item in quotation_items:
        total_price += quotation_item.price * quotation_item.quantity
    return total_price