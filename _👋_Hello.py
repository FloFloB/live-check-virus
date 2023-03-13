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

st.set_page_config(
    page_title="Live Check Virus",
    page_icon="👋",
)


st.write("# Welcome to Live Check Virus! 👋")

st.write("## Stay Ahead of the Curve with Live Check Virus")


st.sidebar.success("**⬆ Select a page from the sidebar** to visualize evolution of Covid")

st.markdown(
    """
    With **Live Check Virus**, you can stay one step ahead in **tracking and analyzing** Covid-19 on social networks. Our application provides **real-time** data analysis that enables users to **identify potential outbreaks** before they occur. We provide **powerful visualizations** to help you understand trends over time and quickly spot emerging patterns that could indicate a risk of outbreak. Plus, our intuitive interface makes it easy to manage your monitoring efforts from one central location – so you never miss a beat!

 Get the **most accurate information** available today with Live Check Virus – and **protect yourself against tomorrow's threats**.
    
    ### Want to learn more?
    - Check out [@misinfbot](https://twitter.com/misinfbot) to verify information directly on twitter
    - Check out [innov8ai.com](http://www.innov8ai.com/)
    
    
"""
)


