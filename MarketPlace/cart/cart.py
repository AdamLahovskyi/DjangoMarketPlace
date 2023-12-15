from item.models import Item

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, item, quantity):
        product_id = str(item.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(item.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        items = Item.objects.filter(id__in=product_ids)

        return items

    def get_quants(self):
        quantities = self.cart

        return quantities

    def update(self, product, quantity):
        product_id =str(product)
        product_qty = int(quantity)

        outcart = self.cart

        outcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing
