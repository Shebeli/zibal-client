
# کلاینت زیبال

هدف از این پروژه, مهیا کردن کلاینتی برای کار با 
خدمات پرداختی زیبال بصورت مفید و موثر می باشد. 

شما میتوانید با استفاده از این پکیچ, در اپلیکیشن های خود از خدمات  پرداختی زیبال همچون درخواست پرداخت, تایید پرداخت و ...  بهره مند شوید.

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

# ایجاد لینک پرداختی
track_id = request_data.track_id
payment_link = client.create_payment_link(track_id)

# تایید پرداخت
verify_data = client.verify_transaction(track_id)

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

data = request_data.model_dump()
print(data)
# {
#     "message": "success",
#     "result": 100,
#     "trackId": 3714061627,
# }

```

در این [لینک](https://docs.pydantic.dev/latest/api/base_model/) میتوانید از متد های دیگر این مدل و نحوه کار با آن ها مطلع شوید. 
## Features to be added

- Handle response and result errors more gracefully and in a structured way
- Implement a new client for IPG's Lazy methods which is quite similar to ZibalIPGClient
- Add new test cases using mocks for handling expected error cases for ZibalClient
- Add new clients for other Zibal's services, such as Zibal's comprehensive payment service and inquiry payment service
- Add different python versions support other than 3.12 (down from 3.12 until 3.8)