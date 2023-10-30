import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_annual_orders_df(df):
    annual_orders_df = df.resample(rule='Y', on='order_purchase_timestamp').agg({
        'order_id': 'nunique',
        'payment_value': 'sum'
    })
    annual_orders_df = annual_orders_df.reset_index()
    annual_orders_df.rename(columns={
        'order_id': 'order_count_year',
        'payment_value': 'revenue_year'
    }, inplace=True)

    return annual_orders_df

def create_sum_orders_items_df(df):
    sum_order_items_df = df.groupby('product_category_name_english').product_id.count().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_payment_type_df(df):
    payment_type_df = df.groupby(by='payment_type').order_id.count().sort_values(ascending=False).reset_index()
    return payment_type_df

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bycity_df

def create_bystate_df(df):
    bystate_df = df.groupby(by='customer_state').customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        'customer_id': 'customer_count'
    }, inplace=True)

    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby(by='customer_id', as_index=False).agg({
        'order_purchase_timestamp': 'max',
        'order_id': 'nunique',
        'payment_value': 'sum'
    })
    rfm_df.columns = ['customer_id', 'max_order_timestamp', 'frequency', 'monetary']

    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
    recent_date = df['order_purchase_timestamp'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)
    rfm_df.drop('max_order_timestamp', axis=1, inplace=True)

    return rfm_df

# Load dataset
all_df = pd.read_csv("all_df_ecommerce.csv")

datetime_columns = ["order_purchase_timestamp", "shipping_limit_date", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

# KOMPONEN FILTER
with st.sidebar:
    # Menambahkan deskripsi dataset
    st.title(":anchor: About the dataset")
    st.markdown("The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. It's features allows viewing an order from multiple dimensions: order status, price, payment and freight performance, location, product attributes, and reviws.")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_orders_items_df = create_sum_orders_items_df(main_df)
annual_orders_df = create_annual_orders_df(main_df)
payment_type_df = create_payment_type_df(main_df)
bycity_df = create_bycity_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# VISUALISASI DATA
st.header('E-Commerce Public Dataset :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Annual Orders')
col1, col2 = st.columns(2)

with col1:
    total_orders_year = annual_orders_df.order_count_year.sum()
    st.metric("Total orders", value=total_orders_year)

with col2:
    total_revenue_year = format_currency(annual_orders_df.revenue_year.sum(), "BRL", locale='es_CO')
    st.metric('Total Revenue', value=total_revenue_year)

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    annual_orders_df['order_purchase_timestamp'],
    annual_orders_df['order_count_year'],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("The Most and Least Product Category")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#F89880", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='product_id', y='product_category_name_english', data=sum_orders_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title('Most Popular Product Categories', loc='center', fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x='product_id', y='product_category_name_english', data=sum_orders_items_df.sort_values(by='product_id', ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Less Popular Product Categories", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Payment Type")

fig, ax = plt.subplots(figsize=(35,15))

colors = ["#BEA9DF", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y='order_id',
    x='payment_type',
    data= payment_type_df.sort_values(by='order_id', ascending=False),
    palette = colors
)
ax.set_title("Payment Type", loc='center', fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader('Customer Demographics')

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20,10))

    colors = ["#FAC898", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y='customer_count',
        x='customer_city',
        data=bycity_df.sort_values(by='customer_count', ascending=False).head(5),
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of Customer by City', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20,10))

    colors = ["#FAC898", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y='customer_count',
        x='customer_state',
        data=bystate_df.sort_values(by='customer_count', ascending=False).head(5),
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of Customer by State', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

rfm_df['customer'] = [i for i in range (99440)]

st.subheader('Best Customer Based on RFM')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), 'BRL', locale='es_CO')
    st.metric("Average Monetary", value = avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35,15))
colors = ["#00A36C", "#00A36C", "#00A36C", "#00A36C", "#00A36C"]

sns.barplot(y='recency', x='customer', data=rfm_df.sort_values(by='recency', ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="customer", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="customer", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)