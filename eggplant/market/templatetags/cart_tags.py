from django import template
from django.core.urlresolvers import reverse
from django.template.base import TemplateSyntaxError

register = template.Library()


@register.simple_tag(takes_context=True)
def cart_action(context, action, product_id=None, quantity=None,
                delivery_date=None):
    btn_css_classes = 'btn btn-sm '
    if action == 'remove':
        url = reverse('eggplant:market:remove_from_cart')
        btn_css_classes += 'btn-danger'
        delivery_date_field = '<input name="delivery_date" type="hidden" ' +\
            'value="{}"/>'.format(delivery_date or '')
    elif action == 'add':
        action = 'Add to cart'
        url = reverse('eggplant:market:add_to_cart')
        btn_css_classes += 'btn-success btn-sm'
        delivery_date_field = '''
        <div class="input-group input-group-sm">
            <input class="datepicker form-control"
                placeholder="delivery date" name="delivery_date"
                type="text" value=""/>
            <div class="input-group-addon">&#x25BC;</div>
        </div>
        '''
    else:
        raise TemplateSyntaxError("action `{}` not supported".format(action))
    quantity = quantity or 1
    fmt = {
        'action': action,
        'action_url': url,
        'btn_css_classes': btn_css_classes,
        'product_id': int(product_id),
        'quantity': int(quantity),
        'csrf_token': context['csrf_token'],
    }
    html = ('''
    <form action="{action_url}" method="POST">
        ''' + delivery_date_field + '''
        <input name="product" type="hidden" value="{product_id}"/>
        <input name="quantity" type="hidden" value="{quantity}"/>
        <input name="csrfmiddlewaretoken" type="hidden" value="{csrf_token}" />
        <p class="pull-right">
        <button type="submit"
            class="{btn_css_classes}"
            role="button" >{action}</button>
        </p>
    </form>''').format(**fmt)
    return html
