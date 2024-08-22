# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 16:25:56 2024

@author: oem
"""

import pandas as pd
# flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz
df = pd.read_csv("flo_data_20k.csv")
df_copy = df.copy()
# Veri setinde
 #a. İlk 10 gözlem,
 #b. Değişken isimleri,
 #c. Betimsel istatistik,
 #d. Boş değer,
 #e. Değişken tipleri, incelemesi yapınız
df.head(10)
df.columns
df.describe().T
df.isnull().sum()
df.dtypes
# Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. 
#Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
df["total_order"] = df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]
df["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
df.head()
# Değişkentiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz
df["total_order"].dtypes
df["total_spending"].dtypes
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()
# Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız
df.groupby("order_channel").agg({"master_id": "count",
                                 "total_order": "sum",
                                 "total_spending": "sum"})
#En fazla kazancı getiren ilk 10 müşteriyi sıralayınız
df.sort_values("total_spending", ascending=False)[:10]
# En fazla siparişi veren ilk 10 müşteriyi sıralayınız
df.sort_values("total_order", ascending=False)[:10]
# Veri önhazırlık sürecini fonksiyonlaştırınız.
def data_prep(dataframe):
    dataframe["total_order"] = df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]
    dataframe["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df 
# Recency, Frequency ve Monetary tanımlarını yapınız.
df["last_order_date"].max() #2021/05/30
import datetime as dt
analysis_date = dt.datetime(2021,6,1)
#Hesapladığınız metrikleri rfm isimli bir değişkene atayınız
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"])
rfm["frequency"] = df["total_order"]
rfm["monatery"] = df["total_spending"]
rfm.head()
#Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
rfm["recency_score"] = pd.qcut(rfm["recency"],5,labels=[5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"),5,labels=[5,4,3,2,1])
rfm["monatery"] = pd.qcut(rfm["monatery"].rank(method="first"),5,labels=[5,4,3,2,1])
#recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.
rfm["RF_SCORE"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
#Oluşturulan RF skorları için segment tanımlamaları yapınız
seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'}
rfm["segment"] = rfm["RF_SCORE"].replace(seg_map,regex=True)
# Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
# İlk olarak metriklerin sayısal türde olduğundan emin olun
rfm["recency"] = pd.to_numeric(rfm["recency"], errors='coerce')
rfm["frequency"] = pd.to_numeric(rfm["frequency"], errors='coerce')
rfm["monatery"] = pd.to_numeric(rfm["monatery"], errors='coerce')
rfm[["segment", "recency", "frequency", "monatery"]].groupby("segment").agg(["mean", "count"]) 
# RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz.
# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
#tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak
#iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş
#yapankişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz
female_customers = df[df['interested_in_categories_12'] == 'female']['master_id'].tolist()
filtered_customers = rfm[(rfm['segment'].isin(['champions', 'loyal_customers'])) & (rfm['customer_id'].isin(female_customers))]
master_ids = filtered_customers['customer_id']
master_ids.to_csv('target_customers.csv', index=False, header=True)
# Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte
#iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni
#gelen müşteriler özel olarak hedef alınmak isteniyor. Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz
target_categories = ['male', 'children']
target_customers = df[df['interested_in_categories_12'].isin(target_categories)]['master_id'].tolist()
filtered_customers = rfm[(rfm['segment'].isin(['hibernating', 'about_to_sleep', 'new_customers'])) & 
                         (rfm['customer_id'].isin(target_customers))]
customer_ids = filtered_customers['customer_id']
customer_ids.to_csv('target_customers_discount.csv', index=False, header=True)
