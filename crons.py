#--------------------------- Blair Live ---------------------------------
# BusinessPartner
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/BusinessPartner/BP.py

# Campaign
# */2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Campaign/whatsappCampaign.py
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Campaign/emailCampaign.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Campaign/camSet.py

# Invoice
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Invoice/INV.py
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Invoice/INV_status.py
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Invoice/inv_incoming_payments.py
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Invoice/inv_credit_notes.py

# Item
# */2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Item/import-category.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Item/import-item.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Item/import-priceList.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Item/import-uom.py

# JournalEntries
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/JournalEntries/JE.py

# Order
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Order/ORD.py
*/2 * * * * /usr/bin/python3 /home/www/b2b/ledure_dev/bridge/Order/ORD_status.py






# /home/www/b2b/ledure_dev/bridge/BusinessPartner/groupsCron.py
# /home/www/b2b/ledure_dev/bridge/BusinessPartner/BP.py

# /home/www/b2b/ledure_dev/bridge/Campaign/whatsappCampaign.py
# /home/www/b2b/ledure_dev/bridge/Campaign/emailCampaign.py
# /home/www/b2b/ledure_dev/bridge/Campaign/camSet.py

# /home/www/b2b/ledure_dev/bridge/Company/branch.py

# /home/www/b2b/ledure_dev/bridge/DeliveryNote/DNOTE.py

# /home/www/b2b/ledure_dev/bridge/Employee/SP.py

# /home/www/b2b/ledure_dev/bridge/Industries/INDS.py

# /home/www/b2b/ledure_dev/bridge/Invoice/INV.py
# /home/www/b2b/ledure_dev/bridge/Invoice/INV_status.py
# /home/www/b2b/ledure_dev/bridge/Invoice/inv_incoming_payments.py
# /home/www/b2b/ledure_dev/bridge/Invoice/inv_credit_notes.py

# /home/www/b2b/ledure_dev/bridge/Item/import-category.py
# /home/www/b2b/ledure_dev/bridge/Item/import-item.py
# /home/www/b2b/ledure_dev/bridge/Item/import-priceList.py
# /home/www/b2b/ledure_dev/bridge/Item/import-uom.py
# /home/www/b2b/ledure_dev/bridge/Item/update-imported-item.py

# /home/www/b2b/ledure_dev/bridge/JournalEntries/JE.py

# /home/www/b2b/ledure_dev/bridge/Order/ORD_status.py

# /home/www/b2b/ledure_dev/bridge/PaymentTermsTypes/PTM.py
