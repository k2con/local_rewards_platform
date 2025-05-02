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
    if value.upper() in ['UNLIMITED', 'ANY']: 
        value = None    

    return value.strip()

def import_reward_from_excel(filename='base_rewards.xlsx'):
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
                    contact_phone_number = str(int(row[key['l']].value))
                    

                brand_country = None
                if brand and country and purchase_detail:
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
                type = row[key['p']].value.title()

                parts = str(row[key['o']].value).split("-")
                length = len(parts)

                # if length == 1:
                #     price_min = price_format(parts[0])
                #     price_max = price_format(parts[0])
                #     if parts[0].upper() == 'ANY':
                #         price_min = 1
                        
                #     Price.objects.get_or_create(reward = reward,
                #                                     currency = currency,
                #                                     type = "Fixed",
                #                                     value_min = price_min,
                #                                     value_max = price_max
                #                                 )
                    
                # elif length == 2:
                #     price_min = price_format(parts[0])
                #     price_max = price_format(parts[1])
                #     if parts[1].upper() in ['UNLIMITED', 'ANY']:
                #         price_max = None
                        
                #     Price.objects.get_or_create(reward = reward,
                #                                     currency = currency,
                #                                     type = "Range",
                #                                     value_min = price_min,
                #                                     value_max = price_max
                #                                 )

                """"""
                # if type.upper() in ['RANGE'] and length == 2:

                #     Price.objects.get_or_create(reward = reward,
                #                                 currency = currency,
                #                                 type = "Range",
                #                                 value_min = price_format(parts[0]),
                #                                 value_max = price_format(parts[1])
                #                             )
                                                
                    
                # elif type.upper() in ['FIXED'] and length == 1:

                #     if price_format(parts[0]) == 'ANY':
                #         value_min = 1
                #         value_max = 1
                #     else:
                #         value_min = price_format(parts[0])
                #         value_max = price_format(parts[0])

                #     Price.objects.get_or_create(reward = reward,
                #                                     currency = currency,
                #                                     type = "Fixed",
                #                                     value_min = value_min,
                #                                     value_max = value_max
                #                                 )

                # elif type.upper() in ['MULTI-VALUE'] and length >= 1:

                #     for i in range(length):
                #          Price.objects.get_or_create(reward = reward,
                #                                         currency = currency,
                #                                         type = 'Fixed',
                #                                         value_min = price_format(parts[0]),
                #                                         value_max = price_format(parts[0])
                #                                     )
                
                # if type.upper() in ['RANGE', 'FIXED', 'MULTI-VALUE', 'CUSTOM']:
               
                # print(f"Reward '{reward.id}' importado exitosamente.")
                # break
            except Exception as e:
                print(f"Error al procesar la fila {row}: {e}")
                break
        
        print("Importación de reward completada.")

    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado en la raíz del proyecto.")
    except Exception as e:
        print(f"Error general durante la importación: {e}")

if __name__ == "__main__":
    import_reward_from_excel()