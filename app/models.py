from django.db import models

# Create your models here.


class Manuals(models.Model):
    asin = models.CharField(max_length=10)
    document = models.CharField(max_length=30)
    file_type = models.CharField(max_length=15)


class Messages(models.Model):
    AmazonOrderId = models.CharField(max_length=19)
    RequestId = models.CharField(max_length=36)
    submissionDate = models.DateTimeField(db_column='PurchaseDate')  # Field name made lowercase.
    code = models.CharField(max_length=50)
    message = models.CharField(max_length=2000)



class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    @staticmethod
    def foo():
        return "bar"


class ItemsUploads(models.Model):
    id = models.BigIntegerField(db_column='id')
    amazonorderid = models.CharField(db_column='AmazonOrderId', max_length=19, primary_key=True)  # Field name made lowercase.
    asin = models.CharField(db_column='ASIN', max_length=10)  # Field name made lowercase.
    sellersku = models.CharField(db_column='SellerSKU', max_length=50)  # Field name made lowercase.
    md5 = models.CharField(db_column='Content-MD5', max_length=19)  # Field name made lowercase.
    itemprice = models.TextField(db_column='ItemPrice')  # Field name made lowercase. This field type is a guess.
    purchasedate = models.DateTimeField(db_column='PurchaseDate')  # Field name made lowercase.
    file = models.CharField(max_length=50)

    class Meta:
     managed = False
     db_table = 'app_items_uploads_view'



class Uploads(models.Model):

    amazonorderid = models.CharField(db_column='AmazonOrderId', max_length=19, primary_key=True)  # Field name made lowercase.
    x_amz_security_token = models.CharField(db_column='X-Amz-Security-Token', max_length=1200)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x_amz_algorithm = models.CharField(db_column='X-Amz-Algorithm', max_length=16)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x_amz_date = models.CharField(db_column='X-Amz-Date', max_length=16)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x_amz_signedheaders = models.CharField(db_column='X-Amz-SignedHeaders', max_length=50)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x_amz_expires = models.IntegerField(db_column='X-Amz-Expires')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x_amz_credential = models.CharField(db_column='X-Amz-Credential', max_length=65)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x_amz_signature = models.CharField(db_column='X-Amz-Signature', max_length=65)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    submissiondate = models.DateTimeField(db_column='submissionDate')  # Field name made lowercase.
    method = models.CharField(max_length=5)
    file = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    x_amz_server_side_encryption = models.CharField(db_column='x-amz-server-side-encryption', max_length=7)  # Field renamed to remove unsuitable characters.
    content_md5 = models.CharField(db_column='Content-MD5', max_length=50)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    uploaddestinationid = models.CharField(db_column='uploadDestinationId', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False


class Orders(models.Model):
    # orders = models.Manager()
    id = models.BigIntegerField(db_column='id')
    BuyerInfo = models.CharField(db_column='BuyerInfo', max_length=55)  # Field name made lowercase.
    AmazonOrderId = models.CharField(db_column='AmazonOrderId', unique=True, primary_key=True, max_length=19)  # Field name made lowercase.
    PurchaseDate = models.DateTimeField(db_column='PurchaseDate')  # Field name made lowercase.
    ShippingAddress = models.CharField(db_column='ShippingAddress', max_length=200, blank=True, null=True)  # Field name made lowercase.
    LastUpdateDate = models.DateTimeField(db_column='LastUpdateDate')  # Field name made lowercase.
    OrderStatus = models.CharField(db_column='OrderStatus', max_length=10)  # Field name made lowercase.
    SellerOrderId = models.CharField(db_column='SellerOrderId', max_length=19, blank=True, null=True)  # Field name made lowercase.
    FulfillmentChannel = models.CharField(db_column='FulfillmentChannel', max_length=3)  # Field name made lowercase.
    SalesChannel = models.CharField(db_column='SalesChannel', max_length=9)  # Field name made lowercase.
    AutomatedShippingSettings = models.CharField(db_column='AutomatedShippingSettings', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ShipServiceLevel = models.CharField(db_column='ShipServiceLevel', max_length=25)  # Field name made lowercase.
    OrderTotal = models.CharField(db_column='OrderTotal', max_length=55, blank=True, null=True)  # Field name made lowercase.
    NumberOfItemsShipped = models.IntegerField(db_column='NumberOfItemsShipped')  # Field name made lowercase.
    NumberOfItemsUnshipped = models.IntegerField(db_column='NumberOfItemsUnshipped')  # Field name made lowercase.
    PaymentMethod = models.CharField(db_column='PaymentMethod', max_length=5, blank=True, null=True)  # Field name made lowercase.
    PaymentMethodDetails = models.CharField(db_column='PaymentMethodDetails', max_length=12)  # Field name made lowercase.
    IsReplacementOrder = models.CharField(db_column='IsReplacementOrder', max_length=5)  # Field name made lowercase.
    MarketplaceId = models.CharField(db_column='MarketplaceId', max_length=14)  # Field name made lowercase.
    ShipmentServiceLevelCategory = models.CharField(db_column='ShipmentServiceLevelCategory', max_length=14)  # Field name made lowercase.
    OrderType = models.CharField(db_column='OrderType', max_length=14)  # Field name made lowercase.
    EarliestShipDate = models.DateTimeField(db_column='EarliestShipDate')  # Field name made lowercase.
    LatestShipDate = models.DateTimeField(db_column='LatestShipDate')  # Field name made lowercase.
    EarliestDeliveryDate = models.DateTimeField(db_column='EarliestDeliveryDate', blank=True, null=True)  # Field name made lowercase.
    LatestDeliveryDate = models.DateTimeField(db_column='LatestDeliveryDate', blank=True, null=True)  # Field name made lowercase.
    IsBusinessOrder = models.IntegerField(db_column='IsBusinessOrder')  # Field name made lowercase.
    IsSoldByAB = models.IntegerField(db_column='IsSoldByAB')  # Field name made lowercase.
    IsPrime = models.IntegerField(db_column='IsPrime')  # Field name made lowercase.
    IsGlobalExpressEnabled = models.IntegerField(db_column='IsGlobalExpressEnabled')  # Field name made lowercase.
    IsPremiumOrder = models.IntegerField(db_column='IsPremiumOrder')  # Field name made lowercase.
    DefaultShipFromLocationAddress = models.CharField(db_column='DefaultShipFromLocationAddress', max_length=255, blank=True, null=True)  # Field name made lowercase.
    IsISPU = models.IntegerField(db_column='IsISPU')  # Field name made lowercase.
    HasRegulatedItems = models.IntegerField(db_column='HasRegulatedItems', blank=True, null=True)  # Field name made lowercase.
    IsAccessPointOrder = models.IntegerField(db_column='IsAccessPointOrder')  # Field name made lowercase.

    class Meta:
        managed = True


class Items(models.Model):
    '''
    amazonorderid = models.ForeignKey(
        Uploads,
        on_delete=models.CASCADE,
    )

    uploads = models.OneToOneField(
        Uploads,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    '''
    id = models.BigIntegerField(db_column='id', primary_key=True)
    AmazonOrderId = models.CharField(db_column='AmazonOrderId', max_length=19)  # Field name made lowercase.
    # get() returned more than one Uploads -- it returned 2! Maybe because I uploaded 2 times as result of first wrong upload
    # amazonorderid = models.OneToOneField(Uploads, db_column='AmazonOrderId', on_delete=models.CASCADE, primary_key=True)
    # amazonorderid = models.ForeignKey(Uploads, on_delete=models.PROTECT, db_column='AmazonOrderId', max_length=19)
    BuyerInfo = models.CharField(db_column='BuyerInfo', max_length=125)  # Field name made lowercase.
    ASIN = models.CharField(db_column='ASIN', max_length=10)  # Field name made lowercase.
    OrderItemId = models.CharField(db_column='OrderItemId', max_length=14)  # Field name made lowercase.
    SellerSKU = models.CharField(db_column='SellerSKU', max_length=50)  # Field name made lowercase.
    Title = models.CharField(db_column='Title', max_length=200)  # Field name made lowercase.
    QuantityOrdered = models.IntegerField(db_column='QuantityOrdered')  # Field name made lowercase.
    QuantityShipped = models.IntegerField(db_column='QuantityShipped')  # Field name made lowercase.
    ProductInfo = models.CharField(db_column='ProductInfo', max_length=22)  # Field name made lowercase.
    ItemPrice = models.CharField(db_column='ItemPrice', max_length=55)  # Field name made lowercase. This field type is a guess.
    ShippingPrice = models.CharField(db_column='ShippingPrice', max_length=55, blank=True, null=True)  # Field name made lowercase.
    ItemTax = models.CharField(db_column='ItemTax', max_length=55)  # Field name made lowercase.
    ShippingTax = models.CharField(db_column='ShippingTax', max_length=55, blank=True, null=True)  # Field name made lowercase.
    ShippingDiscount = models.CharField(db_column='ShippingDiscount', max_length=55, blank=True, null=True)  # Field name made lowercase.
    ShippingDiscountTax = models.CharField(db_column='ShippingDiscountTax', max_length=55, blank=True, null=True)  # Field name made lowercase.
    PromotionDiscount = models.CharField(db_column='PromotionDiscount', max_length=55)  # Field name made lowercase.
    PromotionDiscountTax = models.CharField(db_column='PromotionDiscountTax', max_length=55)  # Field name made lowercase.
    PromotionIds = models.CharField(db_column='PromotionIds', max_length=65, blank=True, null=True)  # Field name made lowercase.
    IsGift = models.CharField(db_column='IsGift', max_length=5)  # Field name made lowercase.
    PriceDesignation = models.CharField(db_column='PriceDesignation', max_length=55, blank=True, null=True)  # Field name made lowercase.
    ConditionId = models.CharField(db_column='ConditionId', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ConditionSubtypeId = models.CharField(db_column='ConditionSubtypeId', max_length=25, blank=True, null=True)  # Field name made lowercase.
    IsTransparency = models.IntegerField(db_column='IsTransparency')  # Field name made lowercase.
    DeemedResellerCategory = models.CharField(db_column='DeemedResellerCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    PurchaseDate = models.DateTimeField(db_column='PurchaseDate')  # Field name made lowercase.
    IossNumber = models.CharField(db_column='IossNumber', max_length=12, blank=True, null=True)  # Field name made lowercase.

    @staticmethod
    def foo():
        return "bar"

    class Meta:
        managed = False
