from main.models import Seller
from main.models import Tag
from main.models import Category
from main.models import Good


seller1 = Seller(name='МакроТехноПарк')
seller1.save()

seller2 = Seller(name='Микротехника')
seller2.save()

tag1 = Tag(name='для дома')
tag1.save()

tag2 = Tag(name='габаритная')
tag2.save()


category1 = Category.objects.create(name='Холодильники')
category2 = Category.objects.create(name='Утюги')


good1 = Good()
good1.name = 'LG'
good1.description = 'Холодильник LG'
good1.category = category2
good1.seller = seller1
good1.price = 25000
good1.save()

good1.tags.add(tag1, tag2)

good2 = Good.objects.create(name='Bosh', description='Утюг Bosh',
                            category=category2, seller=seller2,
                            price=5000)

good2.tags.add(tag1)


tag1.goods.all()
tag2.goods.all()


category1.goods.all()
good1.category = category1
good1.save()
category1.goods.all()


Good.objects.filter(category_id=category1.id)
Good.objects.filter(price__gte=1000)
Good.objects.filter(price__gte=20000)
