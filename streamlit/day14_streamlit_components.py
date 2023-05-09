
# Components are third-party Python modules that extend what's possible with Streamlit 
# In this tutorial, let's get you started in using the streamlit_pandas_profiling component 
# pip install streamlit_pandas_profiling

import streamlit as st
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

st.header('`streamlit_pandas_profiling`')

df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')

# the pandas profiling report is generated via the profile_report() command and displayed using st_profile_report:
pr = df.profile_report()
st_profile_report(pr)