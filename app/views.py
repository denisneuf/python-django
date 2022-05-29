from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.core.exceptions import ValidationError

from django.db import IntegrityError


import json
from django.http import JsonResponse
from django.http import (HttpResponse, HttpResponseNotFound)

import logging
from .models import Uploads
from .models import Items
from .models import Orders
from .models import Manuals
from .models import ItemsUploads
from .models import Messages

# import posixpath
# from pathlib import Path
# from django.utils._os import safe_join
from io import BytesIO
from django.templatetags.static import static

import time
import pytz
from datetime import datetime, timedelta
from django.utils import timezone
from requests import request, exceptions

from mysql.connector import errors

logger = logging.getLogger(__name__)

# Create your views here.

from sp_api.api import Catalog
from sp_api.api import CatalogItems
from sp_api.api import Messaging
from sp_api.api import Upload
from sp_api.api import Orders as spOrders
from sp_api.base import SellingApiBadRequestException, SellingApiException, SellingApiForbiddenException, Marketplaces


from .forms import OrdersForm
from .forms import ItemsForm

import sys


class CreateConfirmOrderDetails(View):

    def get(self, request, amazon_order_id):

        message = f"Su pedido nº {amazon_order_id} se encuentra pendiente, por favor contacte con el servicio de atención al cliente de Amazon para finalizar el pedido: " \
                  "https://www.amazon.es/gp/help/customer/display.html"

        submission_date = datetime.utcnow()

        dictionary = \
            {
                "text": message
            }

        logger.warning(json.dumps(dictionary))

        return JsonResponse(json.dumps(dictionary),safe=False)


        '''

        try:

            res = Messaging(account=store, marketplace=marketplace).create_confirm_order_details(
                order_id=order,
                body=dictionary
            )
        except SellingApiException as ae:
            logging.error(ae)

        except SellingApiBadRequestException as br:
            logging.error(br)
            

        return JsonResponse(result.payload)

        '''


def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
            return func(*args, **kwargs)
        return newfn
    return decorator


class ItemDownloadView(View):

    @retry(3, exceptions=(SellingApiException, exceptions.ConnectionError))
    def load_order(self, **kwargs):
        return spOrders(account="bestq", marketplace=Marketplaces.ES).get_order_items(**kwargs)


    def post(self, request):


        logger.warning(request.POST)

        start_str = request.POST["start_date_time_field"]
        end_str = request.POST["end_date_time_field"]

        naive_start_month = datetime.strptime(start_str, "%Y-%m-%d")

        zero_naive_end_month = datetime.strptime(end_str, "%Y-%m-%d")

        delta = timedelta(hours=24)

        naive_end_month = zero_naive_end_month + delta

        start_month = naive_start_month.replace(tzinfo=pytz.UTC)
        end_month = naive_end_month.replace(tzinfo=pytz.UTC)


        # logger.warning(start_month.tzinfo)
        # logger.warning(type(start_month))
        #
        # logger.warning(end_month)
        # logger.warning(type(end_month))



        # start_month = datetime(2022, 2, 1, 0, 0, 0, tzinfo=pytz.UTC)
        # end_month = datetime(2022, 2, 28, 23, 59, 59, tzinfo=pytz.UTC)

        logging.warning(timezone.now())

        q = Orders.objects.filter(OrderStatus="shipped")
        q = q.filter(PurchaseDate__range=[start_month, end_month])

        for order in q:
            # logger.warning(order.AmazonOrderId)

            # It could face problems because some order could have +1 items and second item get discarded
            check = Items.objects.filter(AmazonOrderId=order.AmazonOrderId)
            # logger.error(check.query)
            if not check:

                items = self.load_order(order_id=order.AmazonOrderId).payload['OrderItems']

                # logging.warning(items)
                # logging.warning("---------------")
                for item in items:
                    # Items.objects.create(**item)
                    # logging.warning(item)
                    # logging.warning("---------------")

                    for k, v in item.items():
                        if (isinstance(v, dict)):
                            # logging.warning(k)
                            # logging.warning(v)
                            item[k] = json.dumps(v)

                    item["PurchaseDate"] = order.PurchaseDate
                    item["AmazonOrderId"] = order.AmazonOrderId

                    '''
                    deserialize = json.dumps(item)

                    logging.warning(deserialize)
                    logging.warning(type(deserialize))
                    serialize = json.loads(deserialize)
                    logging.warning(serialize)
                    logging.warning(type(serialize))
                    '''

                    try:
                        Items.objects.create(**item)
                    except errors.DataError as data__error:
                        logger.error(data__error)
                    except IntegrityError as integrity__error:
                        logger.error(integrity__error)
                    except TypeError as type__error:
                        logger.error(type__error)

                    logger.error(order.AmazonOrderId + " >> " + str(order.PurchaseDate))
                    time.sleep(0.5)
                    # time.sleep(float(res.rate_limit))
            else:
                logging.warning("hay chicha")




        #  Sample.objects.filter(sampledate__gte=datetime.date(2011, 1, 1),
        #                                 sampledate__lte=datetime.date(2011, 1, 31))

        logger.warning(q.query)

        queryset = ItemsUploads.objects.all()

        logger.warning(queryset)

        context = {'page_obj': queryset}

        return render(request, "items.html", context)

    def get(self, request):


        context = {}
        context['form'] = ItemsForm()
        return render(request, "sp_get_items.html", context)





class OrderDownloadView(View):

    def call_api(self, date_start: datetime, date_end: datetime):

        orders = dict()

        try:
            res = spOrders(account="bestq", marketplace=Marketplaces.ES).get_orders(
                CreatedAfter=date_start.isoformat(),
                CreatedBefore=date_end.isoformat()
            )

            orders = res.payload['Orders']
            next_token = res.next_token

            while next_token:
                extra = spOrders(account="bestq", marketplace=Marketplaces.ES).get_orders(
                    CreatedAfter=date_start.isoformat(),
                    CreatedBefore=date_end.isoformat(),
                    NextToken=next_token
                )

                extra_orders = extra.payload['Orders']

                next_token = extra.next_token

                orders = orders + extra_orders

                # sys.exit()

        except SellingApiException as ex:
            print(ex)

        # logger.warning(orders)


        for order in orders:
            # logger.warning(order)


            # record = Orders.objects.create(**order)
            # record = Orders.objects.get_or_create(**order)

            try:
                Orders.objects.update_or_create(**order)
            except errors.DataError as data__error:
                logger.error(data__error)
            except IntegrityError as integrity__error:
                logger.error(integrity__error)
            except TypeError as type__error:
                logger.error(type__error)

            logger.warning(order)
            logger.warning("---------------")

    def post(self, request):
        logger.warning(request.POST)

        # context = request.POST

        start_str = request.POST["start_date_time_field"]
        end_str = request.POST["end_date_time_field"]

        naive_start_month = datetime.strptime(start_str, "%Y-%m-%d")

        zero_naive_end_month = datetime.strptime(end_str, "%Y-%m-%d")

        delta = timedelta(hours=24)

        naive_end_month = zero_naive_end_month + delta

        start_month = naive_start_month.replace(tzinfo=pytz.UTC)
        end_month = naive_end_month.replace(tzinfo=pytz.UTC)

        # start_month = datetime(2022, 5, 27)
        # end_month = datetime(2022, 5, 27, 23, 59, 59)

        self.call_api(naive_start_month, naive_end_month)

        queryset = Orders.objects.all()
        context = {
            'page_obj': queryset
        }

        return render(request, "orders.html", context)

    def get(self, request):

        context = {}
        context['form'] = OrdersForm()
        return render(request, "sp_get_orders.html", context)

class TemplateView(TemplateView):
    # b = Refund(AmazonOrderId='402-5116043-9822739', SellerSKU='AMZLC-C02A016A02FBAGMwXr5')
    print(TemplateView);
    template_name = "index.html"  # your_template


class UploadManual(View):

    def create_legal_disclosure(self, order: str = None, destination_id: str = None, file_name: str = None):

        submission_date = datetime.utcnow()

        # cut = file_name.split("/")
        #
        # name_file = cut[1]

        dictionary = \
            {
                "attachments": [
                    {
                        "uploadDestinationId": destination_id,
                        "fileName": file_name
                    }
                ]
            }

        try:

            res = Messaging(account="bestq", marketplace=Marketplaces.ES).create_legal_disclosure(
                order_id=order,
                body=dictionary
            )

            # logging.info(res)
            # result = res.payload
            # logging.info(result)

            record = Messages.objects.create(AmazonOrderId=order, RequestId=900,
                                            submissionDate=submission_date, code=res.headers.get("x-amz-apigw-id"),
                                            message=json.dumps(dictionary))



        except SellingApiForbiddenException as fe:

            logger.error(fe)

            # logging.info("-------------------------")
            # logging.info(fe.amzn_code)
            # logging.info(fe.message)
            # logging.info(fe.error)
            # logging.info(fe.headers)
            # logging.info(type(fe))
            # logging.info(fe.headers.get("x-amzn-RequestId"))
            # logging.info("-------------------------")
            # logging.info(
            #     database.store_data_message(order, fe.headers.get("x-amzn-RequestId"), submission_date, fe.amzn_code,
            #                                 fe.message))


        except SellingApiBadRequestException as br:

            logger.error(br)

            # logging.info("-------------------------")
            # logging.info(br)
            # logging.info(
            #     database.store_data_message(order, br.headers.get("x-amzn-RequestId"), submission_date, br.amzn_code,
            #                                 br.message))
            # logging.info("-------------------------")


        except SellingApiException as ex:

            logger.error(ex)

            # logging.info("-----------&&-------------")
            # logging.info(dict(ex))
            # logging.info(type(ex))
            # logging.info(
            #     database.store_data_message(order, ex.headers.get("x-amzn-RequestId"), submission_date, ex.amzn_code,
            #                                 ex.message))
            #
            # logging.info("-----------&&------------")

    def upload_file(self, _method, _url, _pdf, _headers, _destination, _order_id):
        """
        logging.info("-------------------")
        logging.info(_headers)
        logging.info("-------------------")
        """

        document_pdf = "app/" + static("manuals/" + _pdf)

        response = request(
            _method,
            _url,
            data=open(document_pdf, 'rb'),
            headers=_headers,
        )

        logging.info(response.status_code)
        # logging.info(response.headers)

        if response.status_code == 200:

            self.create_legal_disclosure(_order_id, _destination, _pdf)
            logger.warning("create disclosure")

        else:
            logging.error(response.status_code)
            logging.error(response.response.headers)

    def create_upload_destination_for_resource(self, c_file: str = None, c_type: str = None, c_order_id: str = None):

        api_path = "messaging/v1/orders/" + c_order_id + "/messages/legalDisclosure"
        logger.warning(api_path)

        method = "PUT"

        try:

            with open(c_file, 'rb') as fh:
                buffer = BytesIO(fh.read())
                logger.warning(buffer)

        except FileNotFoundError:
            logger.warning("File not found")
            return HttpResponseNotFound("File not found")

        submission_date = datetime.utcnow()

        try:
            res = Upload(account="bestq", marketplace=Marketplaces.ES).upload_document(
                resource=api_path,
                file=buffer,
                content_type=c_type
            )

            result = res.payload
            headers = result.get("headers")
            logger.warning(result.get("uploadDestinationId"))
            logger.warning(headers.get("Content-MD5"))

            url = result.get("url")
            base_url = url[:url.rfind('?')]

            params = url[url.rfind('?') + 1:]
            collection = params.split('&')
            data = {}
            data.update({'uploaddestinationid': result.get("uploadDestinationId")})
            data.update({'submissiondate': submission_date})
            data.update({'amazonorderid': c_order_id})

            for item in collection:
                parts = item.split('=')
                value = parts[0].replace("-", "_")
                value = value.lower()

                logger.warning({value: parts[1]})
                data.update({value: parts[1]})

            c_file = c_file[c_file.rfind('/') + 1:]
            c_type = c_type[c_type.rfind('/') + 1:]

            # data.update(result.get("headers"))

            data.update({'x_amz_server_side_encryption': result.get("headers")['x-amz-server-side-encryption']})
            data.update({'content_md5': result.get("headers")['Content-MD5']})
            logger.warning("-------------------------")
            logger.warning(result.get("headers"))
            logger.warning("-------------------------")

            data.update({'file': c_file})
            data.update({'type': c_type})
            data.update({'method': method})

            # logger.warning(data)

            try:

                logger.warning("save a record")

                record = Uploads.objects.create(**data)
                # work as regular
                # record = Uploads.objects.create(amazonorderid="403-6514684-6469130", x_amz_expires=900, submissiondate=submission_date)

                # logging.warning(record)
                # record.save()

            except ValidationError as e:
                logging.error(e)


        except SellingApiException as ex:
            logging.info(ex)

        self.upload_file(method, url, c_file, headers, result.get("uploadDestinationId"), c_order_id)

    def get(self, request, amazon_order_id):

        query_asin = request.GET.get('asin')
        manual = get_object_or_404(Manuals, asin=query_asin)
        logger.warning(static("manuals/"+manual.document))
        document_static = "app/" + static("manuals/"+manual.document)

        # document_root = 'app/static/manuals'

        # path = posixpath.normpath(manual.document).lstrip('/')
        # full_path = Path(safe_join(document_root, path))

        # logger.warning(path)
        # logger.warning(full_path)

        self.create_upload_destination_for_resource(document_static, manual.file_type, amazon_order_id)



        # logger.warning(manual.asin)
        # logger.warning(manual.document)
        # logger.warning(manual.file_type)
        # logger.warning(amazon_order_id)
        now = datetime.now()
        msg = f'Today is {now} {amazon_order_id}'
        time.sleep(2)
        return HttpResponse(msg, content_type='text/plain')


class GetCatalogItem(View):

    def get(self, request, asin):

        included_data = 'identifiers,productTypes,salesRanks,summaries,variations'

        try:
            result = CatalogItems(account="bestq", marketplace=Marketplaces.ES).get_catalog_item(
                asin=asin,
                includedData=included_data
            )
        except SellingApiException as ae:
            logging.error(ae)

        except SellingApiBadRequestException as br:
            logging.error(br)



        return JsonResponse(result.payload)


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


class ItemView(View):

    def get(self, request, order_id):
        logger.warning(order_id)

        item = Items.objects.get(AmazonOrderId=order_id)
        logger.warning(item)

        context = {
            "item": item,
        }
        return render(request, "item.html", context)



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
    ordering = ['-submissiondate']


class OrdersView(ListView):

    template_name = 'orders.html'
    paginate_by = 10
    model = Orders
    ordering = ['-PurchaseDate']


class ItemsView(ListView):

    # qs = Uploads.objects.count()
    # logger.warning(qs)

    # view = OrdersUploads.objects.all()
    # for entry in view.values_list():
    #     logger.warning(entry)
    #     logger.warning("----------")

    # queryset = OrdersUploads.objects.filter(purchasedate__range=["2022-05-02", "2022-05-03"])
    queryset = ItemsUploads.objects.all()


    template_name = 'items.html'
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