# Generated by Django 3.2.19 on 2023-07-11 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PurchaseInvoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditNotesAddressExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CreditNotesId', models.CharField(blank=True, max_length=5)),
                ('ShipToStreet', models.CharField(blank=True, max_length=100)),
                ('ShipToBlock', models.CharField(blank=True, max_length=100)),
                ('ShipToBuilding', models.CharField(blank=True, max_length=100)),
                ('ShipToCity', models.CharField(blank=True, max_length=100)),
                ('ShipToZipCode', models.CharField(blank=True, max_length=100)),
                ('ShipToCounty', models.CharField(blank=True, max_length=100)),
                ('ShipToState', models.CharField(blank=True, max_length=100)),
                ('ShipToCountry', models.CharField(blank=True, max_length=100)),
                ('ShipToAddress2', models.CharField(blank=True, max_length=100)),
                ('ShipToAddress3', models.CharField(blank=True, max_length=100)),
                ('BillToStreet', models.CharField(blank=True, max_length=100)),
                ('BillToBlock', models.CharField(blank=True, max_length=100)),
                ('BillToBuilding', models.CharField(blank=True, max_length=100)),
                ('BillToCity', models.CharField(blank=True, max_length=100)),
                ('BillToZipCode', models.CharField(blank=True, max_length=100)),
                ('BillToCounty', models.CharField(blank=True, max_length=100)),
                ('BillToState', models.CharField(blank=True, max_length=100)),
                ('BillToCountry', models.CharField(blank=True, max_length=100)),
                ('BillToAddress2', models.CharField(blank=True, max_length=100)),
                ('BillToAddress3', models.CharField(blank=True, max_length=100)),
                ('PlaceOfSupply', models.CharField(blank=True, max_length=100)),
                ('PurchasePlaceOfSupply', models.CharField(blank=True, max_length=100)),
                ('U_SCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SSTATE', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPB', models.CharField(blank=True, max_length=100)),
                ('U_BSTATE', models.CharField(blank=True, max_length=100)),
                ('U_BCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPS', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CreditNotesDocumentLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LineNum', models.IntegerField(default=0)),
                ('CreditNotesId', models.CharField(blank=True, max_length=5)),
                ('Quantity', models.IntegerField(default=0)),
                ('UnitPrice', models.FloatField(default=0)),
                ('DiscountPercent', models.FloatField(default=0)),
                ('ItemDescription', models.CharField(blank=True, max_length=150)),
                ('ItemCode', models.CharField(blank=True, max_length=10)),
                ('TaxCode', models.CharField(blank=True, max_length=10)),
                ('BaseEntry', models.CharField(blank=True, default='', max_length=10)),
                ('TaxRate', models.CharField(blank=True, default=0, max_length=10)),
                ('UomNo', models.CharField(blank=True, default='', max_length=100)),
                ('LineTotal', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_DIST', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_SP', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_DD', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_SD', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_TD', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_MRPI', models.CharField(blank=True, default='', max_length=100)),
                ('U_RateType', models.CharField(blank=True, default='', max_length=100)),
                ('MeasureUnit', models.CharField(blank=True, default='', max_length=100)),
                ('SACEntry', models.CharField(blank=True, default='', max_length=100)),
                ('HSNEntry', models.CharField(blank=True, default='', max_length=100)),
                ('SAC', models.CharField(blank=True, default='', max_length=250)),
                ('HSN', models.CharField(blank=True, default='', max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='addressextension',
            name='BillToAddress2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='BillToAddress3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='BillToBlock',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='BillToCounty',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='PlaceOfSupply',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='PurchasePlaceOfSupply',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='ShipToAddress2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='ShipToAddress3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='ShipToBlock',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='addressextension',
            name='ShipToCounty',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='HSN',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='HSNEntry',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='LineTotal',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='MeasureUnit',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='SAC',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='SACEntry',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_RateType',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_UTL_DD',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_UTL_DIST',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_UTL_MRPI',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_UTL_SD',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_UTL_SP',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='documentlines',
            name='U_UTL_TD',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='AdditionalCharges',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='Address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='Address2',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='BPLID',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='BPLName',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='CGST',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='CNNo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='CancelStatus',
            field=models.CharField(blank=True, default='csNo', max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='ContactPersonCode',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='CreateDate',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='CreateTime',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='CreationDate',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DeliveryCharge',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DiscountPercent',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DocCurrency',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DocDueDate',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DocNum',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DocType',
            field=models.CharField(blank=True, default='dDocument_Items', max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='DocumentStatus',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='GSTRate',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='GSTTransactionType',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='IGST',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='NumAtCard',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='OrderID',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='OriginalRefDate',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='OriginalRefNo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='PaymentGroupCode',
            field=models.CharField(blank=True, default=1, max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='RoundingDiffAmount',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='SGST',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='Series',
            field=models.CharField(blank=True, default='241', max_length=100),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='TaxDate',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_EWayBill',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_E_INV_Date',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_E_INV_NO',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_SignedInvoice',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_SignedQRCode',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_TransporterID',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_TransporterName',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_UNE_IRN',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_UNE_LRDate',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_UNE_LRNo',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='U_VehicalNo',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='UpdateDate',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='UpdateTime',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='VATRegNum',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='VatSum',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchasecreditnotes',
            name='WTAmount',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='Address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='Address2',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='BPLID',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='BPLName',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='CGST',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='CNNo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='DocNum',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='DocType',
            field=models.CharField(blank=True, default='dDocument_Items', max_length=100),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='GSTRate',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='GSTTransactionType',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='IGST',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='NumAtCard',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='OriginalRefDate',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='OriginalRefNo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='RoundingDiffAmount',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='SGST',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_EWayBill',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_E_INV_Date',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_E_INV_NO',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_SignedInvoice',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_SignedQRCode',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_TransporterID',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_TransporterName',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_UNE_IRN',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_UNE_LRDate',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_UNE_LRNo',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='U_VehicalNo',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='VATRegNum',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='purchaseinvoices',
            name='WTAmount',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='vendorpayments',
            name='JournalRemarks',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='CardCode',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='CardName',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='DocDate',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='DocEntry',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='DocTotal',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='InvoiceDocEntry',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='purchasecreditnotes',
            name='SalesPersonCode',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
