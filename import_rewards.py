import os
import sys
import django
import openpyxl
from datetime import datetime
import re
import uuid
from django.utils.text import slugify
import string


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  
django.setup()

from rewards.models import RewardBrand, Reward, PurchaseDetail



# Creamos el array de letras
letters = list(string.ascii_lowercase)  # ['a', 'b', 'c', ..., 'z']

# Creamos el diccionario key donde cada letra tiene su índice
key = {letter: index for index, letter in enumerate(letters)}

def parse_range(value):
    value = value.strip()

    if value == "ANY":
        return [10000000000000]

    if "-" in value:
        parts = value.split("-")
        first = parts[0].strip()
        second = parts[1].strip()

        first = 10000000000000 if first == "Unlimited" else first
        second = 10000000000000 if second == "Unlimited" else second

        return [first, second]

    # Si es solo un número (por si acaso)
    try:
        return [value]
    except ValueError:
        return [10000000000000]  # fallback por si viene un valor raro

def import_reward_from_excel(filename='base_rewards1.xlsx'):
    try:
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2):

            try:
                """
                purchase_details
                id,where_to_buy,how_to_buy,how_to_redeem,bulk_detail,process_duration_detail,
                comments,merchant_coverage_detail,conditions,validity,created_at,updated_at,deleted_at
                """

                where_to_buy = row[key['q']].value
                how_to_buy = row[key['r']].value
                how_to_redeem = row[key['s']].value
                bulk_detail = row[key['t']].value
                process_duration_detail = row[key['u']].value
                comments = row[key['v']].value
                merchant_coverage_detail = row[key['w']].value
                conditions = row[key['x']].value
                validity = row[key['y']].value

                # print({
                #     "where_to_buy" : where_to_buy,
                #     "how_to_buy" : how_to_buy,
                #     "how_to_redeem" : how_to_redeem,
                #     "bulk_detail" : bulk_detail,
                #     "process_duration_detail" : process_duration_detail,
                #     "comments" : comments,
                #     "merchant_coverage_detail" : merchant_coverage_detail,
                #     "conditions" : conditions,
                #     "validity" : validity,
                # })
                purchase_detail = None
                if where_to_buy:
                    purchase_detail, created = PurchaseDetail.objects.get_or_create(where_to_buy = where_to_buy,
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
                """
                reward_brands
                id,uuid,slug,name,status,verified,created_at,updated_at,deleted_at,website_url,contact_name,
                contact_email,contact_phone_number,purchase_detail
                """
                slug = slugify(re.sub(r'[^\w\s-]', '', f"{row[key['c']].value} {row[key['f']].value}"))[:50] #la-farma-the-skin-project-ec
                name = row[key['c']].value
                verified = 1
                website_url = row[key['h']].value
                

                # print({
                #     "slug" : slug,
                #     "name" : name,
                #     "status": "active",
                #     "verified" : verified,
                #     "website_url" : website_url,
                #     "contact_name" : contact_name,
                #     "contact_email" : contact_email,
                #     "contact_phone_number" : contact_phone_number,
                # })

                reward_brand = None
                if name:
                    reward_brand, created = RewardBrand.objects.get_or_create(name = name,
                                                                                    defaults={
                                                                                        'slug' : slug,
                                                                                        'name' : name,
                                                                                        'status': 'active',
                                                                                        'verified' : verified,
                                                                                        'website_url' : website_url,
                                                                                        
                                                                                        'purchase_detail' : purchase_detail,
                                                                                    }
                                                                                )

                """
                reward
                id,uuid,slug,category_slug,country,currency,price_type,price,status,created_at,
                updated_at,deleted_at,reward_brand
                """
                
                slug = slugify(re.sub(r'[^\w\s-]', '', f"{row[key['c']].value} {row[key['f']].value}"))[:50] #la-farma-the-skin-project-ec
                category_slug = slugify(re.sub(r'[^\w\s-]', '', f"{row[key['g']].value}"))[:50] 
                country = row[key['f']].value
                currency = row[key['n']].value
                price_type = row[key['p']].value
                price= parse_range(f"{row[key['o']].value}")

                contact_name = row[key['i']].value
                contact_email = row[key['j']].value
                contact_phone_number = f"{row[key['k']].value}{row[key['l']].value}"

                # print({
                #         'slug' : slug,
                #         'category_slug' : category_slug,
                #         'country' : country,
                #         'currency' : currency,
                #         'price_type' : price_type,
                #         'price' : price,
                #         'status' : 'active',
                #         'reward_brand' : reward_brand,
                #     })

                reward = None
                if slug:
                    reward, created = Reward.objects.get_or_create(slug = slug,
                                                                                    defaults={
                                                                                        'slug' : slug,
                                                                                        'category_slug' : category_slug,
                                                                                        'country' : country,
                                                                                        'currency' : currency,
                                                                                        'price_type' : price_type,
                                                                                        'price' : price,
                                                                                        'status' : 'active',
                                                                                        'contact_name' : contact_name,
                                                                                        'contact_email' : contact_email,
                                                                                        'contact_phone_number' : contact_phone_number,
                                                                                        'reward_brand' : reward_brand,
                                                                                    }
                                                                                )

                # print({
                #         'slug' : slug,
                #         'category_slug' : category_slug,
                #         'country' : country,
                #         'currency' : currency,
                #         'price_type' : price_type,
                #         'price' : price,
                #         'status' : 'active',
                #         'reward_brand' : reward_brand,
                #     })
                print(f"Reward '{slug}' importado exitosamente.")
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