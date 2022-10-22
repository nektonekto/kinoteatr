from flask import session

def add_to_basket(item):
    basket = session.get('basket', [])
    basket.append(item)
    session['basket'] = basket


def clear_basket():
    if 'basket' in session:
        session.pop('basket')

