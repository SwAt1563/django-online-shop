import redis
from django.conf import settings
from .models import Product

# connect to redis
# you should turn on redis-server first
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender(object):

    # ket format that we will use in redis
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    # to store and score the products that were bought together
    def products_bought(self, products):
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            for with_product_id in products_ids:
                if product_id != with_product_id:
                    # exp:
                    # {(product:12:purchased_with): [{1:1}, {2:1}, {4:1}, {52:1}, {8:1}]}
                    r.zincrby(self.get_product_key(product_id),
                              1,  # increment by 1
                              with_product_id)

    #  to retrieve the products that were bought together
    def suggest_products_for(self, products, max_results=6):
        products_ids = [p.id for p in products]
        if len(products_ids) == 1:
            # get the highest score suggestions products for an give product
            suggestions = r.zrange(self.get_product_key(products_ids[0]),
                                   0, -1, desc=True)[:max_results]
        else:
            # exp: there is 2 products
            # 1) {(product:12:purchased_with): [{1:1}, {2:5}, {4:1}, {52:9}, {8:1}, {16:7}]}
            # 2) {(product:16:purchased_with): [{1:9}, {2:5}, {4:1}, {52:9}, {8:2}, {12:2}]}
            # union on tmp_key-> {tmp_keys: [{1:10}, {2:10}, {4:2}, {52:18}, {8:3}, {16:7}, {12:2}]}
            # then remove the current keys:
            # {tmp_keys: [{1:10}, {2:10}, {4:2}, {52:18}, {8:3}]}
            # then make sorting
            # {tmp_keys: [{{52:18}, {1:10}, {2:10}, {8:3}, {4:2}]}
            flat_ids = "".join([str(p_id) for p_id in products_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(p_id) for p_id in products_ids]
            r.zunionstore(tmp_key, keys)  # for union all sets for each product in one set with key tmp_key
            # for remove the ids of the current products
            # (that we work for make recommendation to it) from the union set
            r.zrem(tmp_key, *products_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        # for return the previous sorted before make filtering
        suggested_products.sort(key=lambda p: suggested_products_ids.index(p.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
