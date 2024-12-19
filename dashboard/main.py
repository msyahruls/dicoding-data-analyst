# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import pandas as pd
import plotly.express as px
import streamlit as st
# import requests
# from PIL import Image
# from io import BytesIO

products_df = pd.read_csv('./content/products_dataset.csv')
order_item_df = pd.read_csv('./content/order_items_dataset.csv')
orders_df = pd.read_csv('./content/orders_dataset.csv')

columns = ["order_purchase_timestamp","order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
for column in columns:
  orders_df[column] = pd.to_datetime(orders_df[column])

order_item_df['shipping_limit_date'] = pd.to_datetime(order_item_df['shipping_limit_date'], format='mixed')

products_order_item_df = pd.merge(
  left=products_df,
  right=order_item_df,
  how="inner",
  left_on="product_id",
  right_on="product_id"
)

top_product_category = products_order_item_df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).head(5)

top_product_category_df = top_product_category.reset_index()
top_product_category_df.columns = ['Product Category Name', 'Total']


group_param = orders_df['order_purchase_timestamp'].dt.to_period("M")
monthly_order = orders_df.groupby(group_param).order_id.nunique()

monthly_order_df = monthly_order.reset_index()
monthly_order_df.columns = ['Month', 'Total Orders']
monthly_order_df['Month'] = monthly_order_df['Month'].astype(str)

# # Geolocation Dataset
# geolocation_df = pd.read_csv('./content/geolocation_dataset.csv')
# st.write("## Products Dataset", geolocation_df.head())
# # data_geolocation_df = geolocation_df.drop_duplicates(subset='customer_unique_id')

# url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
# response = requests.get(url)
# brazil = Image.open(BytesIO(response.content))
# # ax = data_geolocation_df.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10,10), alpha=0.3,s=0.3,c='maroon')
# plt.axis('off')
# plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
# map_plot = st.pyplot()

st.write(
  """
  # Proyek Analisis Data: E-Commerce Data
  - **Nama:** Muhammad Syahrul Setiawan
  - **Email:** msyahruls2910@gmail.com
  - **ID Dicoding:** m_syahruls
  """
)

st.write("## Top Product Categories")
fig = px.bar(
    top_product_category_df,
    x="Product Category Name",
    y="Total",
    title="Top 5 Product Categories by Total Orders",
    labels={
        "Product Category Name": "Product Category Name",
        "Total": "Total Orders"
    },
    text="Total"  # Add text labels for counts
)

fig.update_layout(
    xaxis_title="Product Category Name",
    yaxis_title="Total Orders",
    xaxis=dict(tickangle=45),
    title_x=0.5,
    margin=dict(t=50, b=100)
)
st.plotly_chart(fig)

# Add date filter
st.write("## Monthly Orders Trend with Date Filtering")
st.sidebar.write("### Filter by Date")
start_date = st.sidebar.date_input("Start Date", value=orders_df['order_purchase_timestamp'].min().date())
end_date = st.sidebar.date_input("End Date", value=orders_df['order_purchase_timestamp'].max().date())

# Validate date input
if start_date > end_date:
    st.sidebar.error("Start date must be before end date!")
else:
  # Filter dataset by date
  filtered_orders_df = orders_df[
    (orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
    (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))
  ]
  filtered_group_param = filtered_orders_df['order_purchase_timestamp'].dt.to_period("M")
  filtered_monthly_order = filtered_orders_df.groupby(filtered_group_param).order_id.nunique()
  
  filtered_monthly_order_df = filtered_monthly_order.reset_index()
  filtered_monthly_order_df.columns = ['Month', 'Total Orders']
  filtered_monthly_order_df['Month'] = filtered_monthly_order_df['Month'].astype(str)

  # Plot filtered trend
  fig = px.line(
    filtered_monthly_order_df,
    x="Month",
    y="Total Orders",
    title=f"Monthly Orders Trend ({start_date} to {end_date})",
    labels={"Month": "Month", "Total Orders": "Total Orders"},
    markers=True
  )
  fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Orders",
    xaxis=dict(tickangle=45),
    title_x=0.5,
    margin=dict(t=50, b=80),
    hovermode="x unified"
  )
  st.plotly_chart(fig)


# map_plot.plot()

st.write("## Products Dataset", products_df.head())
st.write("## Order Items Dataset", order_item_df.head())
st.write("## Orders Dataset", orders_df.head())