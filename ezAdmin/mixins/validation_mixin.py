from django.db.models import Sum
from production.models import RawMaterialInventory

class QuantityValidationMixin:
    def get_available_quantity_fifo(self, component_id, inventory_log = None):
        # Logic to calculate available quantity based on component_id
        current_raw_material = None
        current_raw_material_quantity = None

        # 1. Filter stock type 1 (Stock In) items, ordered by FIFO criteria.
        stock_in_items = RawMaterialInventory.objects.filter(
            component_id=component_id,
            stock_type='1',
        ).order_by('exp_date')

        for stock_in_item in stock_in_items:
            # 2. Get stock items with the same lot number and purchasing document in stock type 2 (Stock Out).
            if not inventory_log:
                stock_out_items = RawMaterialInventory.objects.filter(
                    component_id=component_id,
                    stock_type='2',
                    stock_in_tag=stock_in_item.stock_in_tag
                )

            else:
                stock_out_items = RawMaterialInventory.objects.filter(
                    component_id=component_id,
                    stock_type='2',
                    stock_in_tag=stock_in_item.stock_in_tag
                )
                stock_out_items = stock_out_items.exclude(pk=inventory_log)
    
            # 3. Deduct quantity based on stock_out_items.
            quantity_type_1 = stock_in_item.quantity
            quantity_type_2 = stock_out_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            available_quantity = quantity_type_1 - quantity_type_2

            if available_quantity < 0:
                current_raw_material_quantity = available_quantity
                break
            
            if available_quantity > 0:
                current_raw_material = stock_in_item
                current_raw_material_quantity = available_quantity
                break  # Quantity found, exit the loop.

        return current_raw_material, current_raw_material_quantity

    def get_overide_data(self, component_id, lot_number, inventory_log = None):
        lot_number_data = RawMaterialInventory.objects.filter(
                    component_id=component_id,
                    lot_number=lot_number,
                    stock_type='1'
                    ).first() 

        stock_in_item = RawMaterialInventory.objects.filter(
            component_id=component_id,
            lot_number=lot_number,
            stock_type='1', 
            ).first()

        if inventory_log:
            stock_out_item = RawMaterialInventory.objects.filter(
            stock_type='2',
            lot_number=lot_number,
            component_id=component_id,
        ).exclude(pk=inventory_log)

        else:
            stock_out_item = RawMaterialInventory.objects.filter(
            stock_type='2',
            lot_number=lot_number,
            component_id=component_id,
            )
        
        lot_number_stock_in =  stock_in_item.quantity
        lot_number_stock_out = stock_out_item.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        lot_number_balance_stock = lot_number_stock_in - lot_number_stock_out
        print(lot_number_stock_in)
        print(lot_number_stock_out)
        print(lot_number_balance_stock)
        return lot_number_data, lot_number_balance_stock
