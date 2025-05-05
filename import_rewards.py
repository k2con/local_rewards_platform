import os
import django
import openpyxl
import re
from django.utils.text import slugify
import string


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  
django.setup()

from rewards.models import BrandsCategory, Brand,Country,PurchaseDetail,BrandCountry,Reward,Currency,Price


# Creamos el array de letras
letters = list(string.ascii_lowercase)  # ['a', 'b', 'c', ..., 'z']
# Creamos el diccionario key donde cada letra tiene su índice
key = {letter: index for index, letter in enumerate(letters)}

def price_format(value):
    value = value.strip()

    if value.upper() in ['UNLIMITED', 'ANY']: 
        value = None    

    return value

def import_reward_from_excel(filename='base rewards v2.xlsx'):
    try:
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2):

            try:
                #Creando si no existe el brandCategory
                """BrandsCategory [title,created_at,updated_at,deleted_at]"""                
                title = row[key['g']].value.title()

                brand_category = None
                if title :
                    brand_category, bc_created = BrandsCategory.objects.get_or_create(title = title,
                                                                                   defaults={
                                                                                                "title" : title,
                                                                                            })
                    
                #Creando si no existe el brand
                """Brand [uid,name,website_url,status,verified,category,created_at,updated_at,deleted_at]"""
                name = row[key['c']].value.title()
                website_url = row[key['h']].value
                status = 'active'
                verified = 1

                brand = None
                if brand_category :
                    brand, b_created = Brand.objects.get_or_create(name = name,
                                                                        defaults={
                                                                            "name" : name,
                                                                            "website_url" : website_url,
                                                                            "status" : status,
                                                                            "verified" : verified,
                                                                            "category" : brand_category,
                                                                        })
                #Creando si no existe el country
                """Country [name,iso_code,phone_prefix,created_at,updated_at,deleted_at]"""
                name = row[key['e']].value.title()
                iso_code = row[key['f']].value.upper()
                phone_prefix = None
                if row[key['k']].value:
                    phone_prefix = str(int(row[key['k']].value))

                country = None
                if name :
                    country, c_created = Country.objects.get_or_create(name = name,
                                                                        defaults={
                                                                            "name" : name,
                                                                            "iso_code" : iso_code,
                                                                            "phone_prefix" : phone_prefix,
                                                                        })
                #Creando si no existe el purchaseDetail
                """PurchaseDetail [where_to_buy,how_to_buy,how_to_redeem,bulk_detail,process_duration_detail,comments,
                    merchant_coverage_detail,conditions,validity,created_at,updated_at,deleted_at]"""
                where_to_buy = row[key['q']].value
                how_to_buy = row[key['r']].value
                how_to_redeem = row[key['s']].value
                bulk_detail = row[key['t']].value
                process_duration_detail = row[key['u']].value
                comments = row[key['v']].value
                merchant_coverage_detail = row[key['w']].value
                conditions = row[key['x']].value
                validity = row[key['y']].value  

                purchase_detail = None
                if where_to_buy or how_to_buy or how_to_redeem or bulk_detail or process_duration_detail or comments or merchant_coverage_detail or conditions or validity:
                    purchase_detail, pd_created = PurchaseDetail.objects.get_or_create(where_to_buy = where_to_buy, how_to_buy = how_to_buy, how_to_redeem = how_to_redeem, bulk_detail = bulk_detail, process_duration_detail = process_duration_detail, comments = comments, merchant_coverage_detail = merchant_coverage_detail, conditions = conditions, validity = validity,
                                                                                    defaults={
                                                                                        "where_to_buy" : where_to_buy,
                                                                                        "how_to_buy" : how_to_buy,
                                                                                        "how_to_redeem" : how_to_redeem,
                                                                                        "bulk_detail" : bulk_detail,
                                                                                        "process_duration_detail" : process_duration_detail,
                                                                                        "comments" : comments,
                                                                                        "merchant_coverage_detail" : merchant_coverage_detail,
                                                                                        "conditions" : conditions,
                                                                                        "validity" : validity,
                                                                                    }
                                                                                )
                #Creando si no existe el brandCountry
                """BrandCountry [brand,country,purchase,contact_name,contact_email,contact_phone_number,created_at,
                    updated_at,deleted_at]"""
                contact_name = row[key['i']].value
                contact_email = row[key['j']].value
                if row[key['l']].value:
                    contact_phone_number = str(row[key['l']].value)
                    

                brand_country = None
                if brand and country and purchase_detail:
                    print({
                            "brand" : brand,
                            "country" : country,
                            "purchase" : purchase_detail,
                            "contact_name" : contact_name,
                            "contact_email" : contact_email,
                            "contact_phone_number" : contact_phone_number,
                        })
                    brand_country, bc_created = BrandCountry.objects.get_or_create(brand = brand,
                                                                                country = country,
                                                                                purchase = purchase_detail,
                                                                                defaults={
                                                                                    "brand" : brand,
                                                                                    "country" : country,
                                                                                    "purchase" : purchase_detail,
                                                                                    "contact_name" : contact_name,
                                                                                    "contact_email" : contact_email,
                                                                                    "contact_phone_number" : contact_phone_number,
                                                                                }
                                                                            )
                    
                #Creando si no existe el reward
                
                """Reward [uid,brand_country,comments,image_url,status,created_at,updated_at,deleted_at]"""

                reward = None
                if brand_country:
                    reward, r_created = Reward.objects.get_or_create(brand_country = brand_country,
                                                                        defaults={
                                                                            "brand_country" : brand_country,
                                                                            "status" : 'active', 
                                                                        }
                                                                    )

                """Currency [name,iso_code,created_at,updated_at,deleted_at]"""
                name = row[key['n']].value.title()
                iso_code = row[key['n']].value.upper()
                currency = None
                if name and iso_code:
                    currency, c_created = Currency.objects.get_or_create(name = name,
                                                                        defaults={
                                                                            "name" : name,
                                                                            "iso_code" : iso_code,
                                                                        }
                                                                    )
                """Price [reward,currency,type,value_min,value_max,created_at,updated_at,deleted_at]"""
                """
                    500 - 10000	Range
                    100, 150, 250, 350, 500	Multivalue
                    10	Fixed
                """
                type = row[key['p']].value.title()
                if "MULTIVALUE" in type.upper():
                    type = "Multivalue"
                elif "RANGE" in type.upper():
                    type = "Range"
                elif "FIXED" in type.upper():
                    type = "Fixed"

                
                value = str(row[key['o']].value)
                parts = []
                if '–' in value:
                    parts = value.split('–')
                    # print("1-")
                elif '-' in value:
                    parts = value.split('-')
                    # print("2-")
                elif "," in value:
                    parts = value.split(',')
                    # print(",")
                else:
                    parts.append(value)
                    # print("no ,-")
                    
                length = len(parts)

                if type.upper() in ['MULTIVALUE', 'FIXED']:
                        for i in range(length):
                            
                            price_min = price_format(parts[i])
                            price_max = price_format(parts[i])
                            
                            if parts[i].upper().strip() == 'ANY':
                                price_min = 1
                                type = "Range"
                            else:
                                type = "Fixed"
                            
                            Price.objects.get_or_create(reward = reward,
                                                        currency = currency,
                                                        type = type,
                                                        value_min = price_min,
                                                        value_max = price_max
                                                    )
                elif type.upper() in ['RANGE']:
                    price_min = price_format(parts[0])
                    price_max = price_format(parts[1])
                    # if parts[0].upper() == 'ANY' and parts[1].upper() == 'ANY':
                    #     price_min = 1
                    
                    Price.objects.get_or_create(reward = reward,
                                                currency = currency,
                                                type = type,
                                                value_min = price_min,
                                                value_max = price_max
                                            )
               
            except Exception as e:
                print(f"Error al procesar la fila {row}: {e}")
                raise e
        
        print("Importación de reward completada.")

    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado en la raíz del proyecto.")


if __name__ == "__main__":
    import_reward_from_excel()