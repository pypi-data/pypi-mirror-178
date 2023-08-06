#!/usr/bin/env python
# coding: utf-8

# #### Loading and visualizing the time series dataset

# In[28]:


import pandas as pd
#  we sell beauty shampoo brand
wsb_df = pd.read_csv( 'wsb.csv' ) 
wsb_df.tail(5) 


# In[29]:


# Visualize sale quantity over month
import matplotlib.pyplot as plt
#import seaborn as sn


# In[30]:


#plt.xlabel( "Months" ) 
#plt.ylabel( "Quantity" ) 
plt.plot(wsb_df['Sale Quantity'] );


# In[31]:


wsb_df.info() 


# ### Simple moving average
# In this exercise, our aim is to calculate 12 month's WMA using last 12 months data , starting from the last data
# 
# - rolling () : for wma for the required data
# - shift() - where to start
# 

# In[32]:


#wsb_df['mavg_12'] = wsb_df['Sale Quantity'].rolling( window = 12 ).mean().shift(1) 
wsb_df['smavg_12'] = wsb_df['Sale Quantity'].rolling( window = 12 ).mean()


# In[33]:


wsb_df[['Sale Quantity', 'smavg_12']]
#Note that the first three observations are NaN since our rolling window was set to 12 
#The 12th observation (index=11)


# In[34]:


# Visualization
plt.figure( figsize=(10,4)) 
plt.xlabel( "Months" ) 
plt.ylabel( "Quantity" ) 
plt.plot( wsb_df['Sale Quantity'] ); # line plt.plot will generate line chart
plt.plot( wsb_df['smavg_12'] ); 
plt.legend(); 


# ##### Calculating forecast accuracy for WMA

# In[35]:


# Root mean square error
import numpy as np
from sklearn.metrics import mean_squared_error 
np.sqrt(mean_squared_error( wsb_df['Sale Quantity'][12:].values, wsb_df['smavg_12'][12:].values)) 
#np.sqrt(mean_squared_error( wsb_df['Sale Quantity'].values, wsb_df['smavg_12'].values)) 


# ### Weighted Moving Average

# 

# In[36]:


weights = np.array(list(range(1, 13))) / 100
sum_weights = np.sum(weights)

def weighted_ma(value):
    return np.sum(weights*value) / sum_weights

wsb_df['12wma'] = wsb_df['Sale Quantity'].rolling(window=12).apply(weighted_ma)
wsb_df


# In[37]:


# Visualization
plt.figure( figsize=(10,4)) 
plt.xlabel( "Months" ) 
plt.ylabel( "Quantity" ) 
plt.plot( wsb_df['Sale Quantity'] ); 
plt.plot( wsb_df['smavg_12'] ); 
plt.plot( wsb_df['12wma'] ); 
plt.legend(); 


# In[38]:


# Root mean square error
import numpy as np
from sklearn.metrics import mean_squared_error 
np.sqrt(mean_squared_error( wsb_df['Sale Quantity'][12:].values, wsb_df['12wma'][12:].values)) 


# ### EMA : Exponential moving average
# In this exercise, our aim is to calculate 12 month's WMA using last 12 months data , starting from the last data
# 
# - ewm () : for ema
# - aplha : smoothinhg constant ( from 0 to 1)
# 

# In[39]:


wsb_df['ewm12'] = wsb_df['Sale Quantity'].ewm( alpha = 0.2 ).mean() 
wsb_df


# In[40]:


# visualization 
plt.figure( figsize=(10,4)) 
plt.xlabel( "Months" ) 
plt.ylabel( "Quantity" ) 
plt.plot( wsb_df['Sale Quantity'] ); 
plt.plot( wsb_df['ewm12'] ); 
plt.plot( wsb_df['smavg_12'] );
plt.plot( wsb_df['12wma'] );  
plt.legend(); 


# In[41]:


# Root mean square error
import numpy as np
from sklearn.metrics import mean_squared_error 
np.sqrt(mean_squared_error( wsb_df['Sale Quantity'][12:].values, wsb_df['ewm12'][12:].values)) 


# ### Decomposing Time Series Data

# In[42]:


from statsmodels.tsa.seasonal import seasonal_decompose 
ts_decompse = seasonal_decompose( np.array(wsb_df['Sale Quantity']), model='multiplicative', period = 12 ) 
## Plotting the deocompsed time series components
ts_plot = ts_decompse.plot() 


# In[43]:


# The “residuals” in a time series model are what is left over after fitting a model
wsb_df['seasonal'] = ts_decompse.seasonal 
wsb_df['trend'] = ts_decompse.trend
wsb_df.head()


# ### Acf or Auto correation function or correlogram

# Exericse : Aircraft space parts
#     
# Monthly demand for avionic system spares used in vimana 007 aircraft is provided in vimana.csv

# In[44]:


vimana_df = pd.read_csv('vimana.csv') 
vimana_df.head(5) 


# Print the ACF plot to show the autocorrelation upto lag of 20

# In[45]:


from statsmodels.graphics.tsaplots import plot_acf, plot_pacf 
# Show autocorrelation upto lag 20
acf_plot = plot_acf( vimana_df.demand, lags=20)


# In[46]:


pacf_plot = plot_pacf( vimana_df.demand, lags=10)
plot_pacf()


# ### Build AR Model and MA Model 

# In[47]:


# AR Model

from statsmodels.tsa.arima.model import ARIMA


# In[48]:


arima = ARIMA( vimana_df.demand[0:30], order = (1,0,0)) 
ar_model = arima.fit() 
ar_model.summary()


# In[49]:


# From the model summary p static (0.0027) is less then critical value (0.05)
# Hence the model is valid as per the assumption


# ##### Forecast and Measure Accuracy -AR Model

# In[50]:


forecast_31_37 = ar_model.predict(30, 36)
forecast_31_37 


# In[51]:


def get_mape(actual, predicted): 
 y_true, y_pred = np.array(actual), np.array(predicted) 
 return np.round( np.mean(np.abs((actual - predicted) / actual)) * 100, 2 )


# In[52]:


get_mape( vimana_df.demand[30:], 
forecast_31_37 ) 


# ##### MA Model

# In[53]:


arima = ARIMA( vimana_df.demand[0:30], order = (0,0,1)) 
ma_model = arima.fit() 
ma_model.summary()


# In[54]:


# From the model summary p static (0.0256) is less then critical value (0.05)
# Hence the model is valid as per the assumption


# In[55]:


forecast_31_37 = ma_model.predict(30, 36)
forecast_31_37


# In[56]:


# Model performance
get_mape( vimana_df.demand[30:], 
forecast_31_37 )


# #### ARMA Model

# In[57]:


arima = ARIMA( vimana_df.demand[0:30], order = (1,0,1)) 
arma_model = arima.fit() 
arma_model.summary() 


# In[58]:


forecast_31_37 = arma_model.predict(30, 36)
forecast_31_37


# In[59]:


# From the summary of ARMA Model, p static value of MA (0.1010) is greater than critical value (0.05)
# Hence ARMA model is not valid for shift 1; hence use either AR or MA model
# ARMA Model is good for stationary data


# In[60]:


# Model performance
get_mape( vimana_df.demand[30:], 
forecast_31_37 )


# ## ARIMA MODEL

# - Prereqisute : What is non stationairity of data
#     - mean of yt at different values of t are constant
#     - varience of yt at different time period are constant
#     - the covarience of yt abd y t-k for different lags depends only on k and not ont 
# 
# - Arima moodels are used when the data are non srationary
# - components of ARIMA Model : p(AR component), d (integration or differencing) and q (MA component)
# - the main ojective of d component is to convert non stationarity data to stationarity data
# 

# Example : 
#     
# Daily demand for a production in a store for the past 115 days are provided in store.xlsx. Delelope an appropriate ARIMA model that can be used for forecasting demand.

# In[61]:


# slow delcline of auto correlation indicates that series is non stationary- Qualitative decision


# ### Step-1 Non Stationarity check- statistical (Quantitative test)

# ##### Non stationarity test- Quantitative Decision

# # Dickey fuller test
# 
# ![adf.png](attachment:adf.png)

# In[62]:


# adf (dickey fuller test)
from statsmodels.tsa.stattools import adfuller


# In[63]:


results=adfuller(vimana_df.demand)
print("p- value is " , results[1])


# ##### Since the p value (0.46) is greater than critical values (0.05) , we can not reject the null hypothesis, 
# ie the series is non stationary only

# ### Step 2 Differencing
# 
# Converting the non stationarity data to stationarity data

# In[64]:


vimana_df['demand_diff'] = vimana_df.demand - vimana_df.demand.shift(1) 
vimana_df.head(4)


# In[65]:


vimana_df=vimana_df.dropna()
vimana_df.head(4)


# ### Step-3 Apply Arima Model

# In[66]:


arima = ARIMA(vimana_df.demand[0:30], order = (1,1,1)) 
arima_model = arima.fit() 


# In[67]:


store_predict, stderr, ci = arima_model.forecast(steps = 3) 


# In[68]:


store_predict


# #### Step -4 Performance metric

# In[69]:


# Model performance
get_mape( vimana_df.demand[30:], store_predict)


# ***End******jayesh P

#!/usr/bin/env python
# coding: utf-8

# ### Load the Dataset

# In[27]:


import pandas as pd
Data = pd.read_csv("mdata.csv")
Data


# ### checking missing values in each columns of the dataset

# In[28]:


Data.isnull().sum()


# In[29]:


#returns True for all the missing values & False for all the occupied values.
Data.isnull()


# In[30]:


#notnull()
#returns True for all the occupied values and False for the missing value.
Data.notnull()


# In[31]:


#dropna()
#dropna removes the entire row having missing value
Data2=Data.dropna()
Data2


# In[32]:


#Fillna
# replace nan to zero
Data3=Data['Sales Revenue'].fillna(0)
Data3


# In[33]:


# Remove missin columns
updated_df = Data.dropna(axis=1)
updated_df


# In[34]:


print(Data.shape)
print(updated_df.shape)
# removed many columns, which is not really good


# In[35]:


# Remove only missig rows
updated_df1 = Data.dropna(axis=0)
print(Data.shape)
print(updated_df1.shape)


# ![image.png](attachment:image.png)

# ### Removing the existing duplicates from the dataset

# In[36]:


Data1 =Data.drop_duplicates()
Data1


# ### Missing Data imputation with mean value of the column in the dataset
# 

# In[37]:


Data1['Sales Revenue']=Data1['Sales Revenue'].fillna(Data1['Sales Revenue'].mean())
Data1


# ### Missing Data Imputation with mode values of the columns in the dataset

# In[38]:


Data1['Sales Person']=Data1['Sales Person'].fillna(Data1['Sales Person'].mode().iloc[0])
Data1


# ### Defining python Function to Identify outlers (This code will be provided during exam)

# In[66]:

q1, q3 = np.percentile(sorted(Data['Sales Revenue']), [25, 75])
iqr = q3 - q1
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)
outliers = [x for x in data if x <= lower_bound or x >= upper_bound]
return outliers


# ### Identifying outliers in a particular column of the dataset

# In[67]:


#input data
detect_outlier((Data['Sales Revenue']))


# In[68]:


# empty lists represents no outlier present on the columns


# In[69]:


Performance=[76,15,99.5,73.5,75.7,75,10,-100,0,1,10]

Data['Performance']=Performance
Data


# In[70]:


detect_outlier((Data['Performance']))


# ### Loading another dataset named train for more understanding

# In[ ]:


#  checking missing values in each columns of the dataset
df=pd.read_csv('train.csv')
df.isnull().sum()


# In[ ]:


# Treating missing values using relevant techniques
df['Age']=df['Age'].fillna(df['Age'].mean())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df['Cabin'] = df['Cabin'].fillna(df['Cabin'].mode()[0])
df.isnull().sum()


# In[ ]:




#!/usr/bin/env python
# coding: utf-8

# ### Time series - Missing value Imputation
# 
# 
# Time series is a sequence of observations recorded at regular time intervals. Time series analysis can be useful to see how a given asset, security, or economic variable changes over time. 
# 
#  backfill – bfill : according to the last observed value & forwardfill – ffill : according to the next observed value
# 

# In[3]:


# there are four missing values
import numpy as np
import pandas as pd
lst = [10001.0, 10002.0, 10003.0,10004.0, np.nan, np.nan, 10005.0, np.nan, 10000]
df = pd.DataFrame(lst)
df


# In[4]:


gfg1 = df.ffill()
# Filling forward
print("Using ffill() function:-")
print(gfg1)


# In[5]:


# Filling backward
gfg2 = df.bfill()
print("Using bfill() function:-")
print(gfg2)


# ### Detect & Remove ouliers from the Dataset

# - Outlier is an untypical observed data point in a given distribution of data points.
# 
# - An outlier can be easily defined and visualized using a box-plot 
# 
# ![Box%20plot.PNG](attachment:Box%20plot.PNG)
# 
# #In data analysis transformation is the replacement of a variable by afunction of that variable: for example, replacing a variable x by the square root of x or the logarithm of x. 

# In[6]:


Data = pd.read_csv("mdata.csv")

Performance=[76,15,99.5,73.5,75.7,10,-100,10.9, 100001,0.00001, 100]

Data['Performance']=Performance
Data


# In[7]:


#def detect_outlier(data):
# find q1 and q3 values
q1 = np.percentile(sorted(Data['Performance']), [25])
q3 = np.percentile(sorted(Data['Performance']), [75])
# compute IQR
iqr = q3 - q1
# find lower and upper bounds
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)
outliers = [x for x in data if x <= lower_bound or x >= upper_bound]
return outliers


# In[8]:


#input data
import numpy as np
detect_outlier((Data['Performance']))
# returns outliers


# In[9]:


import seaborn as sns
sns.kdeplot(Data['Performance'])


# In[10]:


from scipy.stats import skew
print('\nSkewness for data : ', skew(Data['Performance']))


# In[11]:


Data['Performance']


# In[12]:


Data_New=Data['Performance'].drop([1, 2])
Data_New


# In[13]:


import seaborn as sns
sns.kdeplot(Data_New)


# In[14]:


print('\nSkewness for data : ', skew(Data_New))


# In[15]:


# Practical example-1
diamonds = pd.read_csv("diamonds.csv")
diamonds=diamonds.dropna()
diamonds.head()


# In[18]:


diamonds['carat'].head(10)


# In[21]:


import seaborn as sns
import matplotlib.pyplot as plt
sns.boxplot(x=diamonds['carat'])
plt.show()
#this column has outliers (it is shown at boxplot)


# In[22]:


diamonds['carat'].describe()


# In[23]:


# Need more information np.log
df_carat_log=np.log(diamonds['carat'])
df_carat_log.head()


# In[24]:


sns.boxplot(x=df_carat_log)
plt.show()


# In[25]:


# # Practical example-2
data = pd.read_csv('employees_attrition.csv')
data.head()


# In[26]:


data.columns


# In[27]:


data['JobRole'].unique()


# In[28]:


plt.figure(figsize=(4,4))
sns.boxplot(data=data, y='MonthlyIncome')


# In[29]:


plt.figure(figsize=(14,4))
sns.boxplot(data=data, x='JobRole', y='MonthlyIncome')
plt.xticks(rotation=45)
plt.show()


# In[30]:


sales_rep = data[data['JobRole'] == 'Sales Representative']
q1 = sales_rep['MonthlyIncome'].quantile(0.25)
q3 = sales_rep['MonthlyIncome'].quantile(0.75)
iqr = q3 - q1
lw = q1 - 1.5 * iqr
uw = q3 + 1.5 * iqr
lw, uw


# In[36]:


sales_outliers = sales_rep[(sales_rep['MonthlyIncome'] < lw) | (sales_rep['MonthlyIncome'] > uw)]
sales_outliers.columns


# In[37]:


sales_outliers.index.tolist()


# In[38]:


data.MonthlyIncome.plot.hist()


# In[ ]:


data.MonthlyIncome.plot.kde()


# In[ ]:


data.MonthlyIncome.skew()


# In[ ]:


#np.log(data.MonthlyIncome).plot.kde()
DATA=np.log(data.MonthlyIncome)
DATA.plot.kde()


# In[ ]:


np.log(data.MonthlyIncome).skew()


