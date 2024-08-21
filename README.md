# کلاینت زیبال

هدف از این پروژه, مهیا کردن کلاینتی برای کار با
خدمات پرداختی زیبال بصورت مفید و موثر می باشد.

شما میتوانید با استفاده از این پکیچ, در اپلیکیشن های خود از خدمات پرداختی زیبال همچون درخواست پرداخت, تایید پرداخت و ... بهره مند شوید.

## نصب

برای نصب این پکیچ این کامند را اجرا کنید:

```bash
pip install zibal-client
```

## نحوه استفاده

میتوانید از کد مرچنت `zibal` جهت تست سرویس درگاه پرداختی زیبال استفاده کنید.

تمامی تراکنش های ایجاد شده با این کد مرچنت فرضی هست و تراکنش واقعی صورت نمیگیرد.

```python
from zibal.client import ZibalIPGClient

# کد مرچنت خود را به کلاس کلاینت دهید
client = ZibalIPGClient("zibal")

# درخواست تراکنش جدید
request_data = client.request_transaction(
    amount=50000,
    callback_url="https://somecallbackurl.com",
)

print(requst_data.message)
# success

# ایجاد لینک پرداختی
track_id = request_data.track_id
payment_link = client.create_payment_link(track_id)

# تایید پرداخت (پس از پرداخت توسط کاربر، این تابع برای تاییدیه باید ران شود)
verify_data = client.verify_transaction(track_id)

print(verify_data.message)
# success

# استعلام پرداخت
inquiry_data = client.inquiry_transaction(track_id)
```

برای اطلاع از فرمت و تایپ داده های ورودی و خروجی این توابع, به تایپ تعریف شده آن در تعریف تابع مربوطه مراجع نمایید.

توجه شود که خروجی توابع مربوط به تراکنش ها همگی مدلی از `BaseModel` پکیج pydantic هستند و میتوانید از متد های آن طبق نیاز خودتان از آن استفاده نمایید.

برای مثال برای گرفتن یک خروجی به صورت دیکشنری میتوانید از متد `model_dump` استفاده نمایید:

```python
request_data = client.request_transaction(
    amount=50000,
    callback_url="https://somecallbackurl.com",
)

data = request_data.model_dump(exclude_none=True)
print(data)
# {
#     'track_id': 3722304104,
#     'result': 100,
#     'message': 'success'
# }

```

در این [لینک](https://docs.pydantic.dev/latest/api/base_model/) میتوانید از متد های دیگر این مدل و نحوه کار با آن ها مطلع شوید.

## Features to be added

- Handle result errors more gracefully and in a robust way ✅
- Add different python versions support starting from 3.9 up to 3.12 ✅
- Add new test cases for handling expected error cases for ZibalIPGClient ✅
- Add option to enable/disable pydantic validation error raise
- Implement a new client for IPG's Lazy methods which is quite similar to ZibalIPGClient
- Add new clients for other Zibal's services, such as Zibal's comprehensive payment service and inquiry payment service
