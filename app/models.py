from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    @staticmethod
    def foo():
        return "bar"


class OrdersUploads(models.Model):


    amazonorderid = models.CharField(db_column='AmazonOrderId', max_length=19, primary_key=True)  # Field name made lowercase.
    asin = models.CharField(db_column='ASIN', max_length=10)  # Field name made lowercase.
    sellersku = models.CharField(db_column='SellerSKU', max_length=50)  # Field name made lowercase.
    md5 = models.CharField(db_column='Content-MD5', max_length=19)  # Field name made lowercase.
    itemprice = models.TextField(db_column='ItemPrice')  # Field name made lowercase. This field type is a guess.
    purchasedate = models.DateTimeField(db_column='PurchaseDate')  # Field name made lowercase.
    file = models.CharField(max_length=50)

    class Meta:
     managed = False
     db_table = 'app_orders_uploads_view'


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

    amazonorderid = models.CharField(db_column='AmazonOrderId', max_length=19, primary_key=True)  # Field name made lowercase.
    # get() returned more than one Uploads -- it returned 2! Maybe because I uploaded 2 times as result of first wrong upload
    # amazonorderid = models.OneToOneField(Uploads, db_column='AmazonOrderId', on_delete=models.CASCADE, primary_key=True)
    amazonorderid = models.ForeignKey(Uploads, on_delete=models.PROTECT, db_column='AmazonOrderId', max_length=19)
    buyerinfo = models.CharField(db_column='BuyerInfo', max_length=125)  # Field name made lowercase.
    asin = models.CharField(db_column='ASIN', max_length=10)  # Field name made lowercase.
    orderitemid = models.CharField(db_column='OrderItemId', max_length=14)  # Field name made lowercase.
    sellersku = models.CharField(db_column='SellerSKU', max_length=50)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200)  # Field name made lowercase.
    quantityordered = models.IntegerField(db_column='QuantityOrdered')  # Field name made lowercase.
    quantityshipped = models.IntegerField(db_column='QuantityShipped')  # Field name made lowercase.
    productinfo = models.CharField(db_column='ProductInfo', max_length=22)  # Field name made lowercase.
    itemprice = models.TextField(db_column='ItemPrice')  # Field name made lowercase. This field type is a guess.
    shippingprice = models.CharField(db_column='ShippingPrice', max_length=55, blank=True, null=True)  # Field name made lowercase.
    itemtax = models.CharField(db_column='ItemTax', max_length=55)  # Field name made lowercase.
    shippingtax = models.CharField(db_column='ShippingTax', max_length=55, blank=True, null=True)  # Field name made lowercase.
    shippingdiscount = models.CharField(db_column='ShippingDiscount', max_length=55, blank=True, null=True)  # Field name made lowercase.
    shippingdiscounttax = models.CharField(db_column='ShippingDiscountTax', max_length=55, blank=True, null=True)  # Field name made lowercase.
    promotiondiscount = models.CharField(db_column='PromotionDiscount', max_length=55)  # Field name made lowercase.
    promotiondiscounttax = models.CharField(db_column='PromotionDiscountTax', max_length=55)  # Field name made lowercase.
    promotionids = models.CharField(db_column='PromotionIds', max_length=65, blank=True, null=True)  # Field name made lowercase.
    isgift = models.CharField(db_column='IsGift', max_length=5)  # Field name made lowercase.
    pricedesignation = models.CharField(db_column='PriceDesignation', max_length=55, blank=True, null=True)  # Field name made lowercase.
    conditionid = models.CharField(db_column='ConditionId', max_length=25, blank=True, null=True)  # Field name made lowercase.
    conditionsubtypeid = models.CharField(db_column='ConditionSubtypeId', max_length=25, blank=True, null=True)  # Field name made lowercase.
    istransparency = models.IntegerField(db_column='IsTransparency')  # Field name made lowercase.
    deemedresellercategory = models.CharField(db_column='DeemedResellerCategory', max_length=5, blank=True, null=True)  # Field name made lowercase.
    purchasedate = models.DateTimeField(db_column='PurchaseDate')  # Field name made lowercase.
    iossnumber = models.CharField(db_column='IossNumber', max_length=12, blank=True, null=True)  # Field name made lowercase.

    @staticmethod
    def foo():
        return "bar"

    class Meta:
        managed = False
