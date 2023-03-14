import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pymysql
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import itertools
import networkx as nx
from pyvis.network import Network
import numpy as np
import datetime as dt
from datetime import timedelta

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Covid Network")

@st.experimental_memo(ttl=3600)
def load_data():
	server = SSHTunnelForwarder(
	   	 st.secrets["SSH_host"],
	   	 ssh_username=st.secrets["SSH_username"],
		 ssh_password=st.secrets["SSH_password"],
    		 remote_bind_address=('127.0.0.1', 3306)
	)
	server.start()


	url_object = URL.create("mysql+pymysql",username=st.secrets["DB_username"],
    				port=server.local_bind_port,
    				password=st.secrets["DB_password"],  # plain (unescaped) text
    				host="127.0.0.1",
    				database=st.secrets["DB"],
	)

	engine = create_engine(url_object)

	df2=pd.read_sql_table('covid',con = engine)


	engine.dispose()
	server.stop()
	
	return df2

@st.experimental_memo
def create_graph(data):
	col1 = []
	col2 = []
	data['clean_text']=data['clean_text'].str.lower()
	data['tags']=data['clean_text'].str.findall(r'(\#\w+)')
	for index, row in data.iterrows():
    		hashtags=row['tags']
    		hashtags_len = len(hashtags)
    		for n in list(itertools.combinations(hashtags, 2)):
        		col1.append(n[0])
        		col2.append(n[1])
	df3 = pd.DataFrame(list(zip(col1, col2)),columns=['source', 'target'])
	df3 = pd.DataFrame({'counts' : df3.groupby(['source', 'target']).size()}).reset_index()
	g = nx.from_pandas_edgelist(df3[df3.counts>100], source='source', target='target', edge_attr='counts')
	return g


st.sidebar.header("Covid Network")

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

st.sidebar.header("Select date")
## Range selector
cols1,_ = st.columns((1,2)) # To make it narrower
format = 'MMM DD'#, YYYY'  # format output
start_date = data['date'].min().date() #dt.date(year=2023,month=2,day=20)  #  I need some range in the past
end_date = data['date'].max().date()#dt.datetime.now().date()
max_days = end_date-start_date
start_value_date=end_date - timedelta(days=10)

slider = st.sidebar.slider('', min_value=start_date, value=(start_value_date,end_date) ,max_value=end_date, format=format)
## Sanity check
#st.table(pd.DataFrame([[start_date, slider, end_date]],
#                      columns=['start',
#                               'selected',
#                               'end'],
#                      index=['date']))

st.write('#Hashtags Network analysis from **'+str(slider[0]) + '** to **' + str(slider[1])+'**')
mask = (data['date'] > pd.to_datetime(slider[0])) & (data['date'] <= pd.to_datetime(slider[1]))

data_load_state = st.text('Creating graph...')
g=create_graph(data.loc[mask])
data_load_state.text("Done! ")

nt = Network(notebook=True)
nt.from_nx(g)
nt.repulsion()
nt.show('test.html')

HtmlFile = open("test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 1600,width=600)
