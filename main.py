import pandas as pd
from openai import OpenAI

client = OpenAI(
    api_key="aa-ZAyyQX9y072RyJorOyx1zDtS7dk4MJUiifyEzNmj5xen56tX", base_url="https://api.avalai.ir/v1"
)


def read_excel(file_path):
    return pd.read_excel(file_path)


def identify_columns(records):
    columns = ["first_name", "last_name", "mobile", "birth_day", "national_code", "degree", "father_name" ]
    prompt = f"""
    من یک فایل اکسل دارم و می‌خواهم بررسی کنی که کدام ستون‌های آن با لیست زیر مطابقت دارند:

    - لیست ستون‌های مورد نظر: {columns} - 
    degree به منظور مدرک تحصیلی فرد است ماننده دیپلم لیسانس دکترا لطفاً برای هر یک از این ستون‌ها، شماره ستون مربوطه 
    را در فایل اکسل پیدا کن و نتیجه را به صورت یک دیکشنری به من برگردان:
    
    - فرمت خروجی مورد نظر: 
    {{
        'first_name': int,
        'last_name': int,
        'mobile': int,
        'birth_day': int,
        'national_code': int,
        'degree': int,
        'father_name': int,
    }}

    توجه: شماره تلفن‌ها با فرمت ایران هستند.
    توجه: اگر پیدا نکردی null بزار بجایه شماره ستون آن.
    داده‌های موجود در فایل اکسل:{records}    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "شما یک دستیار هوشمند هستید که به تجزیه و تحلیل داده‌ها و استخراج اطلاعات از فایل‌های اکسل کمک می‌کنید. وظیفه شما این است که با توجه به اطلاعات داده شده، مطابقت ستون‌ها را بررسی کرده و نتایج را به صورت دیکشنری بازگردانید."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def main(file_path):
    df = read_excel(file_path)
    top_records = df.head(5)

    columns = top_records.columns.tolist()
    records_list = top_records.values.tolist()

    records_list.insert(0, columns)

    records_string = "[\n" + ",\n".join([f"    {list(record)}" for record in records_list]) + "\n]"
    result = identify_columns(records_string)
    print(result)

if __name__ == "__main__":
    file_path = 'users.xls'
    main(file_path)
