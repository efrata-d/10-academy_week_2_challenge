import pandas as pd
import numpy as np
import psycopg2
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def connect():

    conn = None
    try:
        print('Connecting..')
        conn = psycopg2.connect(database="xdrDb", user="admin", password="admin", host="localhost", port="5433")
        
    except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            sys.exit(1)   
 
        
    print("All good, Connection successful!")
    return conn

conn = connect()

telecom_data = pd.read_sql_query('SELECT * FROM xdr_data;', conn)  

telecom_data.fillna(telecom_data.mean(), inplace=True)

basic_metrics = telecom_data.describe()

dispersion_parameters = telecom_data.describe().loc[['std', 'min', '25%', '50%', '75%', 'max']]

plt.figure(figsize=(12, 6))
sns.histplot(data=telecom_data['Session_duration'], bins=30, kde=True)
plt.title('Distribution of Session Duration')
plt.xlabel('Session Duration')
plt.ylabel('Frequency')
plt.show()

bivariate_analysis = telecom_data[['Social_Media_DL', 'Google_DL', 'Email_DL', 'Youtube_DL', 
                                   'Netflix_DL', 'Gaming_DL', 'Other_DL', 'Total_DL']].corr()

telecom_data['Decile_Class'] = pd.qcut(telecom_data['Session_duration'], q=10, labels=False)
decile_data = telecom_data.groupby('Decile_Class')['Total_DL', 'Total_UL'].sum()

correlation_matrix = telecom_data[['Social_Media_DL', 'Google_DL', 'Email_DL', 'Youtube_DL', 
                                   'Netflix_DL', 'Gaming_DL', 'Other_DL']].corr()


scaler = StandardScaler()
scaled_data = scaler.fit_transform(telecom_data[['Social_Media_DL', 'Google_DL', 'Email_DL', 
                                                 'Youtube_DL', 'Netflix_DL', 'Gaming_DL', 'Other_DL']])

pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_data)

principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

telecom_data_with_pca = pd.concat([telecom_data, principal_df], axis=1)


basic_metrics.to_csv('basic_metrics.csv')
dispersion_parameters.to_csv('dispersion_parameters.csv')
bivariate_analysis.to_csv('bivariate_analysis.csv')
decile_data.to_csv('decile_data.csv')
correlation_matrix.to_csv('correlation_matrix.csv')
telecom_data_with_pca.to_csv('telecom_data_with_pca.csv')
