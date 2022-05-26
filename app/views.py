from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from datetime import datetime
import json
from django.http import JsonResponse

import logging
from .models import UploadsBestQ
from .models import ItemsBestQ
from .models import Person

logger = logging.getLogger(__name__)

from .models import Person

# Create your views here.

from sp_api.api import Catalog
from sp_api.base import SellingApiBadRequestException, SellingApiException, Marketplaces


class GetItem(View):

    def get(self, request, asin):
        logger.warning(asin)
        # logger.warning(Person.objects.get(id=1))

        try:
            result = Catalog(account="bestq", marketplace=Marketplaces.ES).get_item(
                asin=asin,
            )
        except SellingApiException as ae:
            logging.error(ae)

        except SellingApiBadRequestException as br:
            logging.error(br)



        return JsonResponse(result.payload)


class SingleOrder(View):

    def get(self, request, order_id):
        logger.warning(order_id)

        item = ItemsBestQ.objects.get(amazonorderid=order_id)
        logger.warning(item)

        context = {
            "item": item,
        }
        return render(request, "item.html", context)


class SingleItem(View):

    def get(self, request, person_id):
        logger.warning(person_id)
        # logger.warning(Person.objects.get(id=1))

        item = Person.objects.get(id=person_id)
        logger.warning(item)

        data = {
            'first_name': item.first_name,
            'last_name': item.last_name,
        }

        return JsonResponse(data)

class AllItems(View):

    def get(self, request):
        items_count = Person.objects.count()
        items = Person.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                'first_name': item.first_name,
                'last_name': item.last_name,
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)

class TemplateView(TemplateView):
    # b = Refund(AmazonOrderId='402-5116043-9822739', SellerSKU='AMZLC-C02A016A02FBAGMwXr5')
    print(TemplateView);
    template_name = "index.html"  # your_template


class ItemsUploadViews(View):

    def get(self, request):

        qs = UploadsBestQ.objects.filter(x_amz_algorithm__isnull=True)
        # logger.warning(qs.query)


        items_count = UploadsBestQ.objects.count()
        items = UploadsBestQ.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                'amazonorderid': item.amazonorderid,
                'submissiondate': item.submissiondate,
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)


class ItemsView(ListView):
    template_name = 'list.html'
    # queryset = ItemsBestQ.objects.all()
    # queryset = ItemsBestQ.objects.filter(purchasedate__range=["2022-01-01", "2022-01-02"])
    # queryset = ItemsBestQ.objects.filter(purchasedate__year='2022', purchasedate__month='01')
    # queryset = ItemsBestQ.objects.filter(purchasedate__gte=datetime(2022, 1, 1, 12, 0, 0), purchasedate__lte=datetime(2022, 1, 3, 23, 59, 59))
    # context_object_name = 'page_obj'
    paginate_by = 10
    model = ItemsBestQ
    ordering = ['-purchasedate']

    '''
    # Set a query set function and obtain <QueryDict: {'asin': ['B08X2Q2X4B']}>
    def get_queryset(self):
        logger.warning(self.request.GET)
        logger.warning(self.request.GET.__getitem__("asin"))
        return ItemsBestQ.objects.filter(asin=self.request.GET.__getitem__("asin"))
    '''

'''
class ItemsView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemsView, self).get_context_data(*args, **kwargs)
        context['codes'] = ItemsBestQ.objects.all()
        return context
'''
'''
class ItemsView(View):

    def get(self, request, *args, **kwargs):
        codes = ItemsBestQ.objects.all()
        context = {'codes': codes}
        return render(request, "list.html", context=context)
'''
class RenderView(View):

    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        logger.warning(args)
        logger.warning(kwargs)
        # logger.warning(Person.object.all())

        my_dict = {
            "segment": "query",
            "reportDate": "20211109",
            "metrics": "impressions,clicks"
        }
        my_array = [1, 2, 3]

        # Person.objects.create(first_name="Ringo", last_name="Starr")
        # Person.objects.create(first_name="Paul", last_name="McCartney")

        logger.warning(Person.objects.all())

        logger.warning(Person.objects.order_by("last_name"))
        logger.warning(Person.objects.filter(first_name = "Paul"))
        logger.warning(Person.objects.get(first_name="Paul"))
        logger.warning(Person.objects.get(id=1))

        person = Person.objects.get(first_name="Paul")
        logger.warning(person.first_name)

        context = {
            "first_name": "Naveen",
            "last_name": "Arora",
            "my_array": my_array,
            "my_dict": my_dict,
            "my_person": Person.objects.all()
        }
        return render(request, "render.html", context)