import streamlit as st 
import pandas as pd
import plotly.express as px 
import datetime as dt

df = pd.read_csv('dashboard_data.csv')
st.set_page_config(page_title='E-Commerce Dashboard',layout='wide')


# ---SIDEBAR
st.sidebar.header("Please Choose the Filter")
category = st.sidebar.multiselect(
    "Product Category: ",
    options=sorted(list(df['product_category_name_english'].unique())),
    default=df['product_category_name_english'].unique()
)
payment = st.sidebar.multiselect(
    "Payment Method: ",
    options=sorted(list(df['payment_type'].unique())),
    default=df['payment_type'].unique()
)
order_status = st.sidebar.multiselect(
    "Order Status: ",
    options=sorted(list(df['order_status'].unique())),
    default = df['order_status'].unique()
)

filter = df.query("product_category_name_english == @category & payment_type==@payment & order_status==order_status")
#-----Main------
st.title("E-Commerce Dashboard")
st.markdown("##")

#KPI Metric 
total_sales = round(filter['payment_value'].sum(),2)
star_rating = ":star:" * int(round(round(filter['review_score'].mean(),1),0))
average_freight = round(filter['freight_value'].mean(),2)

left,mid,right = st.columns(3)
with left:
    st.subheader("Total Payment Value")
    st.subheader(f"$ {total_sales:,}")
with mid: 
    st.subheader("Average Rating: ")
    st.subheader(f"{round(filter['review_score'].mean(),1)} {star_rating}")
with right: 
    st.subheader("Average Freight Cost")
    st.subheader(f"${average_freight:,}")
st.markdown("---")

##VISUALIZATION 
#Bar Chart - Sales by Category
sales_by_category = filter.groupby(by='product_category_name_english').sum()[['payment_value']].sort_values(by='payment_value',ascending=False).head()
sales_by_category_bar = px.bar(
    sales_by_category,x="payment_value",y=sales_by_category.index,orientation='h',title='<b>Sales by Product Category</b>',
    template="simple_white")


#Line Chart - Sales in 2017
filter['order_purchase_timestamp'] = pd.to_datetime(filter['order_purchase_timestamp'])
filter['Year'] = filter['order_purchase_timestamp'].dt.year
filter['Month'] = filter['order_purchase_timestamp'].dt.month
sales_in_2017 = filter[filter['Year']==2017].groupby(by='Month').sum()[['payment_value']]
sales_in_2017_line = px.line(sales_in_2017,x=sales_in_2017.index,y='payment_value',title='Sales in 2017',template="simple_white")


#Bar Chart : Top 5 Customer City 
sales_by_customer_city = filter.groupby(by='customer_city').sum()[['payment_value']].sort_values(by='payment_value',ascending=False).head()
sales_by_customer_city_bar = px.bar(
    sales_by_customer_city,x=sales_by_customer_city.index,y='payment_value',title='Top 5 Customer City',template='simple_white')


# Bar Chart : Sales by Payment Type 
sales_by_payment = filter.groupby(by='payment_type').sum()[['payment_value']].sort_values(by='payment_value',ascending=False)
sales_by_payment_bar = px.bar(sales_by_payment,x=sales_by_payment.index,y='payment_value',title='Total Payment Value per Payment Type',template='simple_white')


# VISUALIZATION
left_column,right_column = st.columns(2)
with left_column:
    st.plotly_chart(sales_by_category_bar)
    st.plotly_chart(sales_by_customer_city_bar)
with right_column: 
    st.plotly_chart(sales_in_2017_line)
    st.plotly_chart(sales_by_payment_bar)