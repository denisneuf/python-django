from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from datetime import datetime
import json
from django.http import JsonResponse
from django.http import HttpResponse

import logging
from .models import Uploads
from .models import Orders
from .models import Person
from .models import OrdersUploads

import time

logger = logging.getLogger(__name__)

# Create your views here.

from sp_api.api import Catalog
from sp_api.base import SellingApiBadRequestException, SellingApiException, Marketplaces


class TemplateView(TemplateView):
    # b = Refund(AmazonOrderId='402-5116043-9822739', SellerSKU='AMZLC-C02A016A02FBAGMwXr5')
    print(TemplateView);
    template_name = "index.html"  # your_template


class UploadManual(View):

    def get(self, request, amazon_order_id):
        asin = request.GET.get('asin')
        logger.warning(asin)
        now = datetime.now()
        msg = f'Today is {now} {amazon_order_id}'
        time.sleep(2)
        return HttpResponse(msg, content_type='text/plain')

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


class OrderView(View):

    def get(self, request, order_id):
        logger.warning(order_id)

        item = Orders.objects.get(amazonorderid=order_id)
        logger.warning(item)

        context = {
            "item": item,
        }
        return render(request, "order.html", context)



class UploadsView(ListView):
    #test = Uploads.objects.select_related('amazonorderid')
    # test = Orders.objects.filter(amazonorderid__orders__amazonorderid__isnull=True)
    # logger.warning(test.query)
    # logger.warning(test.count())
    #
    # orders_uploaded = Uploads.values_list('amazonorderid', flat=True)
    # logger.warning(orders_uploaded.count())


    # for entry in test.values_list():
    #     logger.warning(entry)
    #     logger.warning("----------")


    template_name = 'uploads.html'
    queryset = Uploads.objects.all()
    model = Uploads
    paginate_by = 10


class OrdersView(ListView):

    # qs = Uploads.objects.count()
    # logger.warning(qs)

    # view = OrdersUploads.objects.all()
    # for entry in view.values_list():
    #     logger.warning(entry)
    #     logger.warning("----------")

    # queryset = OrdersUploads.objects.filter(purchasedate__range=["2022-05-02", "2022-05-03"])
    queryset = OrdersUploads.objects.all()


    template_name = 'orders.html'
    # queryset = Orders.objects.all()
    # queryset = Orders.objects.filter(purchasedate__range=["2022-05-02", "2022-05-03"])
    # queryset = Orders.objects.select_related('amazonorderid')
    logger.warning(queryset.query)

    # this is working
    # need foreign key
    # amazonorderid = models.ForeignKey(Uploads, on_delete=models.PROTECT, db_column='AmazonOrderId', max_length=19)
    # queryset = Orders.objects.select_related('amazonorderid')


    # logger.warning(queryset.values_list())


    # for entry in queryset.values_list():
        # logger.warning(entry)
        # logger.warning("----------")



    # queryset = ItemsBestQ.objects.filter(purchasedate__year='2022', purchasedate__month='01')
    # queryset = ItemsBestQ.objects.filter(purchasedate__gte=datetime(2022, 1, 1, 12, 0, 0), purchasedate__lte=datetime(2022, 1, 3, 23, 59, 59))
    # context_object_name = 'page_obj'
    paginate_by = 10
    # model = Orders
    ordering = ['-purchasedate']

    '''
    # Set a query set function and obtain <QueryDict: {'asin': ['B08X2Q2X4B']}>
    def get_queryset(self):
        logger.warning(self.request.GET)
        logger.warning(self.request.GET.__getitem__("asin"))
        return ItemsBestQ.objects.filter(asin=self.request.GET.__getitem__("asin"))
    '''