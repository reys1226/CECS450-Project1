#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
get_ipython().system('{sys.executable} -m pip install pandas numpy pycountry wordcloud')


# In[25]:


import pandas as pd
import numpy as np
import pycountry as pc
import re
import base64
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
get_ipython().run_line_magic('matplotlib', 'inline')


# In[26]:


country_data = pd.read_csv('anthems.csv')


# In[27]:


country_data.head()


# In[28]:


country_data = pd.read_csv('anthems.csv',usecols=['nation'])

country_data.rename(columns={'nation':'country'},
          inplace=True)


# In[29]:


country_data.head()


# In[ ]:


def dropdown_menu_country(dataset):
    output = widgets.Output()
    dropdown_country = widgets.Dropdown(options = sorted(dataset.country.unique()),value=None, description='Country:')
    
    def dropdown_menu_country_eventhandler(change):
        display(input_widgets)
        country_choice = change.new
        display(country_choice)
        
    dropdown_country.observe(dropdown_menu_country_eventhandler, names='value')
    input_widgets = widgets.HBox([dropdown_country])
    display(input_widgets)


# In[52]:


dropdown_menu_country(country_data)


# In[ ]:




