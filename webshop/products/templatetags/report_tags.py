from django import template
from products.models import ReportedReview
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def unresolved_reports_count():
    count = ReportedReview.objects.filter(resolved=False).count()
    if count > 0:
        html_string = format_html('<span class="position-absolute top-10 start-100 translate-middle badge rounded-pill bg-danger">{}<span class="visually-hidden">Items</span></span>', count)
    else:
        html_string = format_html('')
    return html_string