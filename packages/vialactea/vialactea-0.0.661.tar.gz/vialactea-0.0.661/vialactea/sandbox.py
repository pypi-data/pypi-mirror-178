import os
from vialactea.bifrost import __bifrost

def format_product_formula():
    sku_name = input("Insira o nome do sku: ")
    print(sku_name)
    user_resp = input('Confirmar? (S/N)  ')
    if user_resp.upper() == 'S':
        final_formula = ''
        with open(os.path.join(__bifrost.vialactea_import, "formula.txt"), 'r', encoding='utf8') as formula_file:
            formula_file_r = formula_file.readlines()
            for line in formula_file_r:
                final_formula += f'{line.rstrip().upper()}, '

        try:
            with open(os.path.join(__bifrost.vialactea_export, f"{sku_name}_parsed_formula.txt"), 'w', encoding='utf8') as formula_export:
                formula_export.write(final_formula)

        except Exception as e:
            print('Something went wrong')
            print(e)


format_product_formula()
