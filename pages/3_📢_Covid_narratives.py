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
from collections import Counter
import re, string
from nltk import word_tokenize
from nltk.corpus import stopwords


from utilities import preprocessText


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

	N=3
	df2['date']=[pd.to_datetime(d) for d in df2.date]
	df=pd.DataFrame()
	for d in df2.date.dropna().dt.strftime('%Y-%m-%d').unique():
    		tokenized_text = re.sub(r'(\w{3,})s\b', r'\1', preprocessText(' '.join(df2[df2.date==d].clean_text))).split()
    		words_c=Counter(tokenized_text)
    		df_temp = pd.DataFrame(words_c.most_common(N))
    		df_temp = df_temp.rename(columns={0:'word', 1:'count'})
    		df_temp['date']=[d]*N
    		df=pd.concat([df,df_temp])
	
	
	return df


st.set_page_config(page_title="Covid Narratives", page_icon="📢")

data_load_state = st.text('Loading data...')
data=load_data()
data_load_state.text("Done! (using st.cache_data)")



st.header('#Covid narratives with area plot')

fig = px.area(data, x="date", y="count", color="word",color_discrete_sequence=px.colors.qualitative.Alphabet)


st.plotly_chart(fig)

