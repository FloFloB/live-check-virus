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

@st.experimental_memo
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

	df2=pd.read_sql_table('covid_clean',con = engine)


	engine.dispose()
	server.stop()
	
	return df2


st.set_page_config(page_title="Plotting Demo", page_icon="📈")

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

st.header('Last Tweets')
st.write(
  data.clean_text.head()
)



st.header('Timeline of Tweets with #Covid')
df_group1=data.groupby(['date']).size().reset_index(name='Count')
fig1 = px.line(df_group1, x='date', y="Count")
st.plotly_chart(fig1)

df_group2=data.groupby(['date','BERT_Mis']).BERT_Mis.count().unstack()
st.header('Timeline of Tweets with #Covid by Misinformation/Information')
fig2 = go.Figure()
for i,col in enumerate(df_group2.columns):
    fig2.add_trace(go.Line(x=df_group2.index, y=df_group2[col],name=col))

st.plotly_chart(fig2)
