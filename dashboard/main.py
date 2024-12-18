import pandas as pd
import plotly.express as px
import streamlit as st

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

st.write("## Monthly Orders Trend")
fig = px.line(
    monthly_order_df,
    x="Month",
    y="Total Orders",
    title="Monthly Orders Trend",
    labels={"Month": "Month", "Total Orders": "Total Orders"},
    markers=True
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Orders",
    xaxis=dict(
        tickangle=45,
        tickformat="%b %Y",
    ),
    yaxis=dict(
        title="Total Orders",
        showgrid=True
    ),
    title_x=0.5,
    margin=dict(t=50, b=80),
    hovermode="x unified"
)

max_value = monthly_order_df["Total Orders"].max()
max_month = monthly_order_df.loc[monthly_order_df["Total Orders"] == max_value, "Month"].values[0]

fig.add_annotation(
    x=max_month,
    y=max_value,
    text=f"Highest: {max_value}",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-30,
    font=dict(color="red", size=12)
)
st.plotly_chart(fig)

st.write("## Products Dataset", products_df.head())
st.write("## Order Items Dataset", order_item_df.head())
st.write("## Orders Dataset", orders_df.head())