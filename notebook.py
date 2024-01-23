# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UhzvEsvdrNrLigrdAbAVkyt4V55t_KNA

# **Proyek Analisis Dataset: E-Commerce Public Dataset**


*   **Nama:** Venessa Yumadila S
*   **Id Dicoding:** nessasyahra

## Menentukan Pertanyaan


*   Kategori produk apa saja yang paling dan kurang diminati?
*   Bagaimana persebaran atau demografi customers?
*   Berapa rata-rata payment untuk setiap tipe pembayaran?
*   Apa saja tipe pembayaran yang memberikan transaksi terbesar?
*   Bagaimana performa pendapatan setiap tahunnya?

## Menyiapkan Library
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""## Gathering Data

---
pengumpulan data untuk menjawab pertanyaan

"""

customers = pd.read_csv('customers_dataset.csv')
customers.head()

geolocation = pd.read_csv('geolocation_dataset.csv')
geolocation.head()

order_items = pd.read_csv('order_items_dataset.csv')
order_items.head()

payments = pd.read_csv('order_payments_dataset.csv')
payments.head()

reviews = pd.read_csv('order_reviews_dataset.csv')
reviews.head()

orders = pd.read_csv('orders_dataset.csv')
orders.head()

product_translate = pd.read_csv('product_category_name_translation.csv')
product_translate.head()

products = pd.read_csv('products_dataset.csv')
products.head()

sellers = pd.read_csv('sellers_dataset.csv')
sellers.head()

"""## Assesing Data

---
penilaian terhadap data untuk menilai kualitas dari sebuah data, apakah dari data tersebut terdapat missing value, duplicated data, dan lain-lain

**Customers**
"""

customers.info()
# tidak ada missing value atau kesalahan tipe data

print('Jumlah data duplikat: ', customers.duplicated().sum())
# tidak ada data terduplikat

customers.describe()
# tidak ada inaccurate value

"""**Geolocation**"""

geolocation.info()
# tidak ada missing value dan kesalahan tipe data

print('Jumlah data duplikat: ', geolocation.duplicated().sum())
# data terduplikat sebanyak 261831

geolocation.describe()

"""**Order Items**"""

order_items.info()
# tidak ada missing value
# ada kesalahan tipe data pada shipping_limit_date

print('Jumlah data duplikat: ', order_items.duplicated().sum())
# tidak ada data duplikat

order_items.describe()
# ada oulier pada price dan freight_value

"""**Order Payments**"""

payments.info()
# tidak ada missing value dan kesalahan tipe data

print('Jumlah data duplikat: ', payments.duplicated().sum())
# tidak ada data duplikat

payments.describe()
# outlier pada payment_value

"""**Reviews**"""

reviews.info()
# missing value pada review comment title dan message

reviews.isna().sum()
# missing value pada review comment title dan comment message

print('Jumlah duplikat: ', reviews.duplicated().sum())
# tidak ada data duplikat

"""**Orders**"""

orders.info()
# ada missing value pada order approved, delivered carrier, dan delivered customer
# kesalahan tipe data pada kolom date

orders.isna().sum()
# order approves 160
# order delivered carrier 1783
# order delivered customer 2965

orders.describe()

"""**Product Category Name**"""

product_translate.info()
# tidak ada missing value dan kesalahan tipe data

print('Jumlah data duplikat: ', product_translate.duplicated().sum())
# tidak ada data duplikat

"""**Product**"""

products.info()
# ada missing value

products.isna().sum()

print('Jumlah duplikat:', products.duplicated().sum())
# tidak ada data duplikat

"""**Sellers**"""

sellers.info()
# tidak ada missing value dan kesalahan tipe data

print('Jumlah duplikat:', sellers.duplicated().sum())
# tidak ada data duplikat

sellers.describe()

"""## Cleaning Data

---
setelah data dilakukan penilaian maka data perlu dilakukan pembersihan agar data dapat dianalisis dengan baik

**Geolocation**
"""

# menghapus data duplikat
geolocation.drop_duplicates(inplace=True)
print('Jumlah data duplikat:', geolocation.duplicated().sum())

"""**Order Items**"""

# mengubah tipe data
order_items['shipping_limit_date'] = pd.to_datetime(order_items['shipping_limit_date'])
order_items.info()

"""**Orders**"""

# mengubah tipe data
date_columns = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']

for column in date_columns:
  orders[column] = pd.to_datetime(orders[column])

orders.info()

"""**Products**"""

products.isna().sum()

#products[products.product_category_name.isna()]
products.product_category_name.fillna('not defined', inplace=True)

"""## Exploratory Data Analysis

---
proses memperoleh insight yang akan menjawab pertanyaan

**Eksplorasi Data Orders**

---
gabungan data orders, payments, dan customers
"""

orders_df = pd.merge(
    left = orders,
    right = payments,
    how = 'left',
    left_on = 'order_id',
    right_on = 'order_id'
)
orders_df.head()

orders_df = pd.merge(
    left = orders_df,
    right = customers,
    how = 'left',
    left_on = 'customer_id',
    right_on = 'customer_id'
)
orders_df.head()

orders_df = orders_df.drop(columns = ['order_status','customer_zip_code_prefix', 'payment_sequential', 'payment_installments', 'customer_unique_id', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date'])
orders_df.head()

orders_df.describe(include='all')

"""Dari describe mengenai tabel orders_df diperoleh:
*   Tipe pembayaran yang sering digunakan adalah credit card
*   Kota yang paling sering melakukan transaksi adalah Sao Paulo
*   Rata-rata payment yang diperoleh sebesar 154.100380
"""

# mencari rata-rata payment tiap tipe pembayaran
orders_df.groupby(by='payment_type').agg({
    'payment_value': 'mean'
})

"""Rata-rata transaksi paling besar menggunakan credit card"""

# mencari order berdasarkan customers's city
orders_df.groupby(by='customer_city').order_id.nunique().sort_values(ascending=False)

# cari order bedasarkan customers's state
orders_df.groupby(by='customer_state').order_id.nunique().sort_values(ascending=False)

"""Seperti yang diperoleh dari hasil describe, diperoleh order terbanyak dilakukan oleh kota Sao Paulo dengan state SP

**Eksplorasi Data Products**

---

gabungan products (products dan product translate), order items, dan seller
"""

products_df = pd.merge(
    left = products,
    right = product_translate,
    how = 'left',
    left_on = 'product_category_name',
    right_on = 'product_category_name'
)
products_df.head()

products_df = pd.merge(
    left = products_df,
    right = order_items,
    how = 'left',
    left_on = 'product_id',
    right_on = 'product_id'
)
products_df.head()

products_df = pd.merge(
    left = products_df,
    right = sellers,
    how = 'left',
    left_on = 'seller_id',
    right_on = 'seller_id'
)
products_df.head()

products_df.tail()

products_df = products_df.drop(columns = ['seller_zip_code_prefix', 'product_width_cm', 'product_height_cm', 'product_length_cm', 'product_weight_g', 'product_photos_qty', 'product_description_lenght', 'product_name_lenght'])
products_df.head()

products_df.describe(include='all')

"""Dari hasil describe mengenai tabel products_df diperoleh:
*   Kategori produk yang banyak terjual adalah bed_bath_table
*   Kota yang aktif menjual adalah Sao Paulo
*   Rata-rata harga semua produk sebesar 120.653739
"""

# kategori yang memberikan harga tertinggi
products_df.sort_values(by='price', ascending=False)

"""Kategori produk yang memiliki harga termahal adalah housewares, sedangkan kategori produk yang memiliki harga paling rendah adalah construction tools"""

products_df.groupby(by='product_category_name_english').agg({
    'price': ['mean', 'min', 'max'],
    'product_id': 'count'
}).sort_values(by=('product_id','count'), ascending=False)

"""Kategori produk yang paling diminati oleh customers adalah bed_bath_table.
Kategori produk yang kurang diminati oleh customers adalah security_and_services.

**Eksplorasi All Data**

---
gabungan semua data
"""

all_df = pd.merge(
    left = orders_df,
    right = products_df,
    how = 'left',
    left_on = 'order_id',
    right_on = 'order_id'
)
all_df.head()

"""## Visualization & Explanatory Analysis

Performa penjualan dalam tahun
"""

year_order = all_df.resample(rule='Y', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',
    'payment_value': 'sum'
})
year_order.index = year_order.index.strftime('%Y')

year_order = year_order.reset_index()
year_order.rename(columns={
    'order_id': 'order_count',
    'payment_value': 'revenue'
}, inplace=True)
year_order.head()

plt.figure(figsize=(10,5))
plt.plot(
    year_order['order_purchase_timestamp'],
    year_order['revenue'],
    marker='o',
    linewidth=2,
    color='#72BCD4'
)
plt.title('Total Revenue per Year', loc='center', fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

plt.figure(figsize=(10,5))
plt.plot(
    year_order['order_purchase_timestamp'],
    year_order['order_count'],
    marker='o',
    linewidth=2,
    color='#72BCD4'
)
plt.title('Number of Orders per Year', loc='center', fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

"""Tipe pembayaran paling sering dipakai"""

pay_type = all_df.groupby(by='payment_type').order_id.count().sort_values(ascending=False).reset_index()
pay_type

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

plt.figure(figsize=(10,5))
sns.barplot(
    y='order_id',
    x='payment_type',
    data = pay_type.sort_values(by='order_id', ascending=False),
    palette = colors
)
plt.title('Payment Type', loc='center', fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.show()

"""Kategori produk yang paling dan kurang diminati"""

sum_orders = all_df.groupby('product_category_name_english').product_id.count().sort_values(ascending=False).reset_index()
sum_orders.head(5)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24,6))

# bar chart kanan
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x='product_id', y='product_category_name_english', data=sum_orders.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Best Product Category', loc='center', fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

# bar chart kiri
sns.barplot(x='product_id', y='product_category_name_english', data=sum_orders.sort_values(by='product_id', ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position('right')
ax[1].yaxis.tick_right()
ax[1].set_title('Worst Product Category', loc='center', fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle('The Most and Least Popular Product Category', fontsize=20)
plt.show()

"""**RFM Analysis**

---

proses analisis perilaku pelanggan yang dilihat dari recency (waktu terakhir order), frequency (berapa kali pelanggan bertransaksi), dan monetary (seberapa besar transaksi yang dilakukan pelanggan).
"""

rfm = all_df.groupby(by='customer_id', as_index=False).agg({
    'order_purchase_timestamp': 'max',
    'order_id': 'nunique',
    'payment_value': 'sum'
})
rfm.columns = ['customer_id', 'max_order', 'frequency', 'monetary']
rfm

rfm['customer'] = [i for i in range (99441)]
rfm.head()

# tanggal customers terakhir melakukan transaksi
rfm['max_order'] = rfm['max_order'].dt.date
recent_date = all_df['order_purchase_timestamp'].dt.date.max()
rfm['recency'] = rfm['max_order'].apply(lambda x: (recent_date-x).days)

rfm.drop('max_order', axis=1, inplace=True)
rfm.head()

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer", data=rfm.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(y="frequency", x="customer", data=rfm.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="customer", data=rfm.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Best Customer Based on RFM Parameters", fontsize=20)
plt.show()

"""Dengan melakukan RFM analisis dapat dilihat bagaimana perilaku customers kita. Menurut recency pelanggan ke-15595 menghabiskan waktu terbanyak untuk berinteraksi dengan produk. Dilihat dari monetary pelanggan ke-8546 menghabiskan biaya terbesar dalam melakukan transaksi. Sedangkan dilihat dari frequency hampir seluruh pelanggan melakukan transaksi setidaknya sekali."""

all_df.info()

all_df.to_csv('all_df.csv', index=False)

"""## Conclusion

1.   Kategori produk apa saja yang paling dan kurang diminati?

    Setelah dilakukan analisis diperoleh bahwa kategori produk yang paling diminati customers adalah bed_bath_table, sedangkan untuk kategori produk yang kurang diminati adalah security_and_services.

2.   Bagaimana persebaran atau demografi customer?

    Untuk persebaran demografi customers dapat dilihat dari persebaran kota customers. Kota yang paling sering melakukan pembelian atau transaksi adalah Sao Paulo.

3.   Berapa rata-rata payment untuk setiap tipe pembayaran?

    Dilakukan analisis untuk mencari rata-rata pembayaran atau transaksi untuk setiap tipe pembayaran sehingga diperoleh:
  *   boleto	145.034435
  *   credit_card	163.319021
  *   debit_card	142.570170
  *   voucher	65.703354

4.   Apa saja tipe pembayaran yang memberikan transaksi terbesar?

    Pembayaran dilakukan dengan berbagai jenis pembayaran sehingga ingin dilihat tipe pembayaran mana yang memberikan transaksi terbesar. Diperoleh bahwa penggunakan credit card memberikan transaksi terbesar dan paling sering digunakan.

5.   Bagaimana performa pendapatan setiap tahunnya?

    Pendapatan diperoleh setiap tahunnya dari 2016 hingga 2018. Performa pendapatan dari tahun 2016 meningkat signifikan ke tahun 2017 diikuti naiknya pendapatan ke tahun 2018. Sehingga dapat dilihat bahwa performa pendapatan setiap tahunnya dari 2016-2018 selalu meningkat.
"""
