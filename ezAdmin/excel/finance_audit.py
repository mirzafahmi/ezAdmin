def generate_inventory_assets():
    import csv
    import pandas as pd
    from openpyxl import Workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    import os
    import sys

    from django.utils import timezone

    # Add the path to the parent directory of your_project to the Python path
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    # Now you can import modules from your Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ezAdmin.settings')
    import django
    django.setup()

    # Import your Django models
    from purchasing.models import RawMaterialInventory
    from django.db.models import Sum

    # Retrieve all data from the Django model with related fields
    data = RawMaterialInventory.objects.select_related('component__identifier', 'purchasing_doc').values(
        'id',
        'component__id',
        'component__component',
        'component__identifier_id',
        'component__identifier__parent_item_code',
        'quantity',
        'lot_number',
        'exp_date',
        'price_per_unit',
        'stock_type',
        'purchasing_doc__id',
        'purchasing_doc__po_number',
        'purchasing_doc__invoice_number',
        'purchasing_doc__packing_list',
        'purchasing_doc__k1_form',
        'purchasing_doc__AWB_number',
        'stock_in_tag__id',
        'stock_in_date',
        'stock_out_date',
        'validation_date',
        'log_date'
    ).order_by('component__identifier__parent_item_code', 'component__component')

    # Dictionary to store data based on parent_item_code and component
    data_dict = {}

    instances = RawMaterialInventory.objects.all().order_by('component__identifier__parent_item_code', 'component__component').filter(stock_type='1')
    print(timezone.now())
    for instance in instances:    
        stock_in = RawMaterialInventory.objects.filter(
            stock_in_tag=instance.stock_in_tag_id,
            stock_type='1').aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        print(stock_in)
        stock_out = RawMaterialInventory.objects.filter(
            stock_in_tag=instance.stock_in_tag_id,
            stock_type='2').aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        print(stock_out)
        balance = stock_in - stock_out
        print(balance)
        if balance != 0:
            parent_item_code = instance.component.identifier.parent_item_code

            if parent_item_code not in data_dict:
                data_dict[parent_item_code] = {}

            component = instance.component.component

            if component not in data_dict[parent_item_code]:
                data_dict[parent_item_code][component] = []

            flattened_row = {
                'QUANTITY': balance,
                'LOT_NUMBER': instance.lot_number,
                'EXP_DATE': instance.exp_date,
                'PRICE_PER_UNIT': instance.price_per_unit,
                'PO_NUMBER': instance.purchasing_doc.po_number,
                'INVOICE_NUMBER': instance.purchasing_doc.invoice_number,
                'PACKING_LIST': instance.purchasing_doc.packing_list,
                'K1_FORM': instance.purchasing_doc.k1_form,
                'AWB_NUMBER': instance.purchasing_doc.AWB_number
            }

            data_dict[parent_item_code][component].append(flattened_row)


    output_csv_file_path = 'ezAdmin/excel/output.csv'

    with open(output_csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['IDENTIFIER', 'COMPONENT', 'QUANTITY', 'LOT_NUMBER', 'EXP_DATE', 'PRICE_PER_UNIT', 'PO_NUMBER', 'INVOICE_NUMBER', 'PACKING_LIST', 'K1_FORM', 'AWB_NUMBER']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for identifier, components_data in data_dict.items():
            for component, component_data in components_data.items():
                for row in component_data:
                    # Add the 'identifier' and 'component' to each row
                    row['IDENTIFIER'] = identifier
                    row['COMPONENT'] = component
                    writer.writerow(row)
        print('Finished writing to CSV:', output_csv_file_path)

    # Combine all the data into a single list of dictionaries
    all_data = []
    for identifier, components_data in data_dict.items():
        for component, component_data in components_data.items():
            for row in component_data:
                row['identifier'] = identifier
                row['component'] = component
                all_data.append(row)

    # Specify the order of columns
    columns_order = ['IDENTIFIER', 'COMPONENT', 'QUANTITY', 'LOT_NUMBER', 'EXP_DATE', 'PRICE_PER_UNIT', 'PO_NUMBER', 'INVOICE_NUMBER', 'PACKING_LIST', 'K1_FORM', 'AWB_NUMBER']

    # Create a DataFrame with a specified order of columns
    df = pd.DataFrame(all_data, columns=columns_order)

    # Save the DataFrame to an Excel file
    output_excel_file_path = 'ezAdmin/excel/output.xlsx'

    # Create a new Excel workbook and add a worksheet
    wb = Workbook()
    ws = wb.active

    # Write the DataFrame to the worksheet
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)

    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell)) > max_length:
                    max_length = len(cell)
            except:
                pass
        adjusted_width = (max_length + 25)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    # Save the workbook to the specified path
    wb.save(output_excel_file_path)

    print('Finished writing to Excel:', output_excel_file_path)

if __name__ == '__main__':
    generate_inventory_assets()