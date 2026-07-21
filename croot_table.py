import requests
import json
import random
import string

def generate_random_id(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()

def draw_table(data, headers):
    """رسم جدول مخصص بدون مكتبات خارجية"""
    # حساب أطول نص في كل عمود
    col_widths = []
    for col_idx in range(len(headers)):
        max_len = len(str(headers[col_idx]))
        for row in data:
            max_len = max(max_len, len(str(row[col_idx])))
        col_widths.append(max_len + 4)

    def draw_line(char="─"):
        line = "┌"
        for i, w in enumerate(col_widths):
            line += char * w
            if i < len(col_widths) - 1:
                line += "┬"
        line += "┐"
        return line

    def draw_row(row, align="center"):
        line = "│"
        for i, (cell, w) in enumerate(zip(row, col_widths)):
            cell_str = str(cell)
            if align == "center":
                padding = w - len(cell_str)
                left = padding // 2
                right = padding - left
                line += " " * left + cell_str + " " * right
            elif align == "right":
                line += cell_str.rjust(w)
            else:
                line += cell_str.ljust(w)
            line += "│"
        return line

    def draw_separator():
        line = "├"
        for i, w in enumerate(col_widths):
            line += "─" * w
            if i < len(col_widths) - 1:
                line += "┼"
        line += "┤"
        return line

    def draw_bottom():
        line = "└"
        for i, w in enumerate(col_widths):
            line += "─" * w
            if i < len(col_widths) - 1:
                line += "┴"
        line += "┘"
        return line

    result = []
    result.append(draw_line())
    result.append(draw_row(headers))
    result.append(draw_separator())
    for row in data:
        result.append(draw_row(row))
    result.append(draw_bottom())
    return "\n".join(result)

def run_process():
    msisdn = input("ادخل رقم الهاتف : ")
    pin = input("ادخل الرقم السري للمحفظة: ")

    # الباقات بالتفاصيل الحقيقية: (product_id, السعر, الوحدات, الأيام)
    packages = {
        "1":  {"product_id": "Fakka_2.5_Unite",   "price": "2.5",   "units": "45",   "days": "24 ساعة"},
        "2":  {"product_id": "Fakka_5_Unite",     "price": "5",     "units": "80",   "days": "24 ساعة"},
        "3":  {"product_id": "Fakka_6_Unite",     "price": "6",     "units": "225",  "days": "24 ساعة"},
        "4":  {"product_id": "Fakka_9_Unite",     "price": "9",     "units": "400",  "days": "4 أيام"},
        "5":  {"product_id": "Fakka_10_Unite",    "price": "10",    "units": "300",  "days": "7 أيام"},
        "6":  {"product_id": "Fakka_10.5_Unite",  "price": "10.5",  "units": "400",  "days": "7 أيام"},
        "7":  {"product_id": "Fakka_11.5_Unite",  "price": "11.5",  "units": "450",  "days": "7 أيام"},
        "8":  {"product_id": "Fakka_12_Unite",    "price": "12",    "units": "450",  "days": "7 أيام"},
        "9":  {"product_id": "Fakka_12.5_Unite",  "price": "12.5",  "units": "425",  "days": "7 أيام"},
        "10": {"product_id": "Fakka_13.5_Unite",  "price": "13.5",  "units": "650",  "days": "7 أيام"},
        "11": {"product_id": "Fakka_15.5_Unite",  "price": "15",    "units": "625",  "days": "7 أيام"},
        "12": {"product_id": "Fakka_15.5_Unite",  "price": "15.5",  "units": "625",  "days": "7 أيام"},
        "13": {"product_id": "Fakka_16.5_Unite",  "price": "16.5",  "units": "425",  "days": "6 أيام"},
        "14": {"product_id": "Fakka_17.5_Unite",  "price": "17.5",  "units": "650",  "days": "10 أيام"},
        "15": {"product_id": "Fakka_19.5_Unite",  "price": "19.5",  "units": "550",  "days": "10 أيام"},
        "16": {"product_id": "Fakka_20_Unite",    "price": "20",    "units": "750",  "days": "10 أيام"},
    }

    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    📋 جدول الباقات المتاحة                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # إنشاء بيانات الجدول
    table_data = []
    for key, pkg in packages.items():
        table_data.append([
            key,
            pkg['price'] + " جنيه",
            pkg['units'] + " وحدة",
            pkg['days']
        ])

    headers = ["#", "السعر 💰", "الوحدات 📊", "المدة 📅"]
    print(draw_table(table_data, headers))
    print()

    choice = input("اكتب رقم الاختيار: ")
    if choice not in packages:
        print("❌ اختيار غير صحيح")
        return

    product_id = packages[choice]["product_id"]

    headers_base = {
        'User-Agent': "okhttp/4.12.0",
        'Accept-Encoding': "gzip",
        'Connection': "Keep-Alive",
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "ar",
        'x-agent-operatingsystem': "13",
        'x-agent-device': "Android Device",
        'x-agent-version': "2026.4.1",
        'x-agent-build': "1139",
    }

    url_seamless = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth"
    resp1 = session.get(url_seamless, params={'client_id': "ana-vodafone-app-seamless"}, headers=headers_base)

    if resp1.status_code != 200:
        print("❌ فشل الاتصال الأولي.")
        return

    seamless_token = resp1.json().get("seamlessToken")

    url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    payload_token = {
        'grant_type': "password",
        'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3",
        'client_id': "cash-app"
    }

    headers_token = headers_base.copy()
    headers_token.update({
        'seamlessToken': seamless_token,
        'clientId': "AnaVodafoneAndroid",
        'silentLogin': "true",
        'firstTimeLogin': "true"
    })

    resp2 = session.post(url_token, data=payload_token, headers=headers_token)
    if resp2.status_code != 200:
        print("❌ فشل تاكد انك فاتح داتا بخطك الفودافون اللي عليه الكاش")
        return

    access_token = resp2.json().get("access_token")

    url_order = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"
    payload_order = {
        "channel": {"name": "MobileApp"},
        "orderItem": [{
            "action": "insert",
            "id": product_id,
            "product": {
                "characteristic": [
                    {"name": "PaymentMethod", "value": "VFCash"},
                    {"name": "USE_EMONEY", "value": "False"},
                    {"name": "MerchantCode", "value": ""}
                ],
                "id": product_id,
                "relatedParty": [
                    {"id": msisdn.replace("0", "", 1), "name": "MSISDN", "role": "Subscriber"},
                    {"id": msisdn, "name": "Receiver", "role": "Receiver"}
                ]
            },
            "@type": product_id,
            "eCode": 0
        }],
        "relatedParty": [{"id": pin, "name": "pin", "role": "Requestor"}],
        "@type": "CashFakkaAndMared"
    }

    headers_order = headers_token.copy()
    headers_order.update({
        'Content-Type': "application/json",
        'Authorization': f"Bearer {access_token}",
        'api-host': "ProductOrderingManagement",
        'useCase': "CashFakkaAndMared",
        'api-version': "v2",
        'msisdn': msisdn
    })

    resp3 = session.post(url_order, data=json.dumps(payload_order), headers=headers_order)
    result = resp3.json()

    if resp3.status_code == 200:
        print("✅ تمت عملية الشحن بنجاح!")
    elif result.get("code") == "6051":
        balance = next((item['value'] for item in result.get("characteristic", []) if item['name'] == "RemainingBalance"), "غير معروف")
        print(f"❌ فشل: لا يوجد رصيد كافٍ. رصيدك الحالي هو: {balance} جنيه")
    else:
        print(f"❌ فشل الطلب: {result.get('reason', 'خطأ غير معروف')}")

if __name__ == "__main__":
    run_process()
