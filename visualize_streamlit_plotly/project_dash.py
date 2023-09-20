import streamlit as st
import pandas as pd
import os
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="nebs store",page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: stores EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


#uploading data
f1=st.file_uploader(":file_folder: upload a file",type=(["csv","txt","xlxs","xls"]))

if f1 is not None:
    filename=f1.name
    st.write(filename)
    df=pd.read_csv(filename,encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\dread-miles\Documents\interactive-dash")
    df=pd.read_csv("Superstore.csv",encoding="ISO-8859-1")
    
#lets create 2 cols
col1,col2=st.columns((2))
df["Order Date"]=pd.to_datetime(df["Order Date"])

#getting the min and max date
startdate=pd.to_datetime(df["Order Date"]).min()
endate=pd.to_datetime(df["Order Date"]).max()


with col1:
    date1=pd.to_datetime(st.date_input("Start Date",startdate))

with col2:
    date2=pd.to_datetime(st.date_input("end date",endate))
    
df=df[(df["Order Date"] >= date1) & (df["Order Date"] <= endate)].copy()

#choose region for the sidebar
st.sidebar.header("choose your filter: ")
region=st.sidebar.multiselect("pick your region", df["Region"].unique())

if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]

#choose a state
state=st.sidebar.multiselect("pick your state",df2["State"].unique())

if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]

#choose city
city=st.sidebar.multiselect("pick your city",df3["City"].unique())

#if not city:
#    df4=df3.copy()
#else:
 #   df4=df3[df3["City"].isin(city)]
    

#lets see the filter the data
if not region and not state and not city:
    filtered_df=df
elif not state and not city:
    filtered_df=df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df=df2[df2["State"].isin(state)]
elif state and city:
    filtered_df=df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df=df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df=df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df=df3[df3["City"].isin(city)]
else:
    filtered_df=df

category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()  #add the same category

#this is for ploting on the right and left side of the webpage base on category and sales of the data
with col1:
    st.subheader("category wise sales")
    fig=px.bar(category_df,x="Category",y="Sales",text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
              template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height=200)
with col2:
    st.subheader("region wise sales")
    fig=px.pie(filtered_df,values="Sales",names="Region",hole=0.5)
    fig.update_traces(text=filtered_df["Region"],textposition="outside")
    st.plotly_chart(fig,use_container_width=True)

#this is for showing and dawnloading the selceted region,state and city part of the data
col1,col2=st.columns((2))
with col1:
    with st.expander("category_viewdata"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode('UTF-8')
        st.download_button("download data",data=csv,file_name="category_csv.csv",mime="text/csv",
                          help = "click here to download the csv file")
with col2:
    with st.expander("region_viewdata"):
        region=filtered_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="OrRd"))
        csv=region.to_csv(index=False).encode('utf-8')
        st.download_button("download data",data=csv,file_name="region_csv.csv",mime="text/csv",
                          help="click here to download the csv data")

#lets do the time series analysis of the data
filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart=pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y :%b"))["Sales"].sum()).reset_index()
fig2=px.line(linechart,x="month_year",y="Sales",labels={"sales":"amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("time series"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv=linechart.to_csv(index=False).encode('utf-8')
    st.download_button("download data",data=csv,file_name="time series.csv",mime="text/csv",
    help="click here to download the time series")

#create a tree based on region,category and sub category
st.subheader("hiererical view of the data based on region,category and sub category")
fig3=px.treemap(filtered_df,path=["Region","Category","Sub-Category"],values="Sales",hover_data=["Sales"],
                color="Sub-Category")
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3,use_container_width=True)

#lets see sales with segment and category
chart1,chart2=st.columns((2))

#the first is segement comparision
with chart1:
    st.subheader("segment with sales")
    fig=px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark")
    fig.update_traces(text=filtered_df["Segment"],textposition=["inside"])
    st.plotly_chart(fig,use_container_width=True)

#this is category in relation with sales
with chart2:
    st.subheader("category with sales")
    fig2=px.pie(filtered_df,values="Sales",names="Category",template="gridon")
    fig2.update_traces(text=filtered_df["Category"],textposition=["inside"])
    st.plotly_chart(fig2,use_container_width=True)

#lets show the data in tabular format
import plotly.figure_factory as ff
st.subheader(":point_right: month wise sub category sales")
with st.expander("summery table"):
    df_sample=df[:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig=ff.create_table(df_sample,colorscale="Cividis")
    st.plotly_chart(fig,use_container_width=True)

    #lets do data by month and sub category
    st.markdown("month wise sub category table")
    filtered_df["month"]=filtered_df["Order Date"].dt.month_name()
    sub_category_year=pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="month")
    st.write(sub_category_year.style.background_gradient(cmap="Blues"))

#lets display the data in scatter format
data1=px.scatter(filtered_df,x="Sales",y="Profit",size="Quantity")
data1['layout'].update(title="relation between sales and profits using scatter plot",
                      titlefont=dict(size=20),xaxis=dict(title="sales",titlefont=dict(size=19)),
                       yaxis=dict(title="proft",titlefont=dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

#show the wholle dataset
with st.expander("view data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")