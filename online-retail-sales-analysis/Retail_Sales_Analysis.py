#1.Count of Countries of Customers.
#2.Country comparisions based on Total sales.
#3.Boxplot for finding any outliers in Total Sales,Unit Price,Quantity.
#4.Trend of Total sales, extracting total sales using formula - Total Sales = Quantity*Unit Price.
#5.Scatter plot to know the relationship of Quantity vs Total Sales.
#6.Correlation Heatmap for finding correlation among columns.

#-------------------------------------------------------------------------------------------------------

#Importing the required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

#Loading the dataset and checking the basic info
Df = pd.read_csv('C:\TFOD\Matplotlib and Seaborn\Retail sales\online-retail-sales-analysis\online_retail_II.csv')
print(Df.head())
print(Df.info())
print(Df.describe())

#Check for Null values 
print(Df.isnull().sum())

#Replacing the Null values in description as NA and  the customer Id with guest
Df['Description'] = Df['Description'].fillna('NA')

#Converting the InvoiceDate column to datetime format
Df['InvoiceDate'] = pd.to_datetime(Df['InvoiceDate'])

#Extracting Month day and name from Invoice date 
Df['MonthNUM'] = Df['InvoiceDate'].dt.month
Df['Month_Name'] = Df['InvoiceDate'].dt.month_name()

Df['Total Sales'] = np.where((Df['Quantity'] > 0) & (Df['Price'] > 0), 
                             Df['Quantity'] * Df['Price'], 
                             0)


df_Sales = Df['Quantity']>0 
df_Returns = Df['Quantity']<0

df_Sales = Df[Df['Quantity']>0].copy()
df_Returns = Df[Df['Quantity']<0].copy()


Total_Revenue = (df_Sales['Quantity']*df_Sales['Price']).sum()
Total_Refunds = (df_Returns['Quantity']*df_Returns['Price']).abs().sum()

Gross_Revenue = Total_Revenue - Total_Refunds
#-------------------------------------------------------------------------------------------------------

#1.Count the countries 
Top_Countries = Df['Country'].value_counts().head(10)
sns.barplot(x=Top_Countries.index,y=Top_Countries.values)
plt.title('Top countries by Purchacse')
plt.xlabel('Countries')
plt.ylabel('Count')
plt.xticks(rotation = 45)
plt.show()
#Insights: 
#This plot is to show the top countries by customer purchase.
#2.United Kingdom has the highest number of transactions among all countries.

#2.Country comparisions based on Total sales.
Country_Sales = Df.groupby('Country')['Total Sales'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=Country_Sales.index,y=Country_Sales.values)
plt.title('Total Sales county wise')
plt.xlabel('Countries')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()
#Insights:
#1.The plot is to know that which country has contributed highest to the revenue.
#2.Among those all the countries United Kingdom has highest contribution to the Total Revenue.

#3.Boxplot for finding any outliers in Total Sales,Unit Price,Quantity.
#A.TotalSales
plt.boxplot(Df['Total Sales'])
plt.title('Total Sales')
plt.show()

#B.Price
plt.boxplot(Df['Price'])
plt.title('Price')
plt.show()

#C.Quantity
plt.boxplot(Df['Quantity'])
plt.title('Quantity')
plt.show()

#Insights:
#These boxplots are to know if there are any outliers.
#1.In the total sales and Price  there are some negative outliers means there are some refunds on the products.
#2.And also they have positive outliers means there are some high value priced products.
#3.Quantity has some returns which may be common in a retail.

#4.Trend of Total sales
Monthly_Sales = (
    Df.groupby(['MonthNUM', 'Month_Name'], as_index=False)['Total Sales']
      .sum()
      .sort_values('MonthNUM')
)

sns.lineplot( data=Monthly_Sales,
    x='Month_Name',
    y='Total Sales'
)
plt.title('Monthly Total Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.show()
#Insights:
#1.The Total Sales across months has Upward increase.
#2.November and December has the highest revenue/total sales compared to other months.
#3.The increase in the revenue may be due to the festivals as well as the discounts like Big Billion days and End of Season Sales.


#5.Scatter plot to know the relationship of Quantity vs Total Sales.
sns.scatterplot(x=Df['Quantity'],y=Df['Total Sales'])
plt.title('Relation Between Quantity and Total Sales')
plt.xlabel('Quantity')
plt.ylabel('Total Sales')
plt.show()
#Insights:
#1.The Quantity and total sales has some negative relations which is due to return and refund of products.
#2.But the relationship is not that strong as the sales remains almost constant as quantity increases but sometime increases it may be due to high price of the product.


#6.Correlation Heatmap for finding correlation among columns.
Df_Num = Df.select_dtypes(include = 'number')

sns.heatmap(Df_Num.corr(),annot=True)
plt.show()
#Insights:
#1.The relationship b/w Quantity and total sales is good as i gave insights above.
#2.The Quantity and price has a weak relationship and its negative.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Overall Insights and some Recommendations:
#United Kingdom has the highest number of transactions among all countries and has highest contribution to the Total Revenue,so we can consider to increase the marketing effort in the UK in upcoming days.
#In the total sales and Price  there are some negative outliers means there are some refunds on the products and also they have positive outliers means there are some high value priced products.
#Quantity has some returns which may be common in a retail.So we need to focus on reducing the returns and refunds.
#The Total Sales across months has Upward increase.November and December has the highest revenue/total sales compared to other months.The increase in the revenue may be due to the festivals as well as the discounts like Big Billion days and End of Season Sales.

Df.to_csv('Retail_Analysis_Output.csv', index=False)
