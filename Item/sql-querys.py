

# Invoice item total sales group by ItemCode wise
first = "SELECT Invoice_documentlines.`id`, Invoice_documentlines.`ItemDescription`,Invoice_documentlines.ItemCode, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` LEFT Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode WHERE Item_item.ItemsGroupCode = '1512' GROUP BY Invoice_documentlines.ItemCode"

# Invoice item total sales group by sub-group wise
second = "SELECT Invoice_documentlines.`id`, Invoice_documentlines.`U_UTL_ITSBG`, sum(Invoice_documentlines.LineTotal) as LineTotal, sum(Invoice_documentlines.Quantity) as Quantity FROM `Invoice_documentlines` LEFT Join Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode WHERE Item_item.ItemsGroupCode = '1512' GROUP BY Invoice_documentlines.`U_UTL_ITSBG`"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
updateQuery  = "UPDATE Invoice_documentlines INNER JOIN Item_item ON Item_item.ItemCode = Invoice_documentlines.ItemCode SET Invoice_documentlines.U_UTL_ITSBG = Item_item.U_UTL_ITSBG"