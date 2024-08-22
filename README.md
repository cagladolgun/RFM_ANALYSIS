# FLO RFM Analizi Projesi

Bu proje, FLO'nun müşteri verilerini analiz etmek ve RFM metriklerini hesaplamak amacıyla yapılmıştır.

## Adımlar

### 1. Veri Okuma ve İnceleme
- `flo_data_20K.csv` dosyası okundu ve veri setinin ilk 10 gözlemi, değişken isimleri, betimsel istatistikler, boş değerler ve değişken tipleri incelendi.

### 2. Yeni Değişkenler
- Toplam alışveriş sayısı ve harcama miktarı için yeni değişkenler oluşturuldu.

### 3. Tarih Değişkenleri
- Tarih değişkenlerinin tipleri `date` olarak değiştirildi.

### 4. Alışveriş Kanalları
- Alışveriş kanallarındaki müşteri sayısı, toplam ürün sayısı ve harcamaların dağılımı incelendi.

### 5. En Fazla Kazanç ve Sipariş
- En fazla kazancı getiren ve en fazla siparişi veren müşteriler sıralandı.

### 6. Veri Ön Hazırlık
- Veri ön hazırlık süreci fonksiyonlaştırıldı.

### 7. RFM Metrikleri
- Recency, Frequency ve Monetary metrikleri hesaplandı ve isimleri değiştirildi.

### 8. RF Skoru
- RFM metrikleri skorlara çevrildi ve RF_SCORE oluşturuldu.

### 9. Segment Tanımlamaları
- RF skorlarına dayalı segment tanımlamaları yapıldı.
### 10. Aksiyon Zamanı
- **Kadın Ayakkabı Markası için Hedef Müşteri Profilleri:**
  - Yeni bir kadın ayakkabı markası için sadık müşteriler (`Champions`, `Loyal Customers`) ve kadın kategorisinden alışveriş yapan müşteriler belirlendi. Bu müşterilerle özel iletişim kurulması planlanmaktadır.
  - İlgili müşteri ID'leri `target_female_customers.csv` dosyasına kaydedildi.

- **Erkek ve Çocuk Ürünleri için Hedef Müşteri Profilleri:**
  - Erkek ve çocuk ürünlerinde yapılacak indirimler için uykuda olan (`Sleepers`), kaybedilmemesi gereken (`Lost Customers`), ve yeni gelen (`New Customers`) müşteriler belirlendi. Bu müşterilerle indirimle ilgili özel iletişim kurulması planlanmaktadır.
  - İlgili müşteri ID'leri `target_male_kids_customers.csv` dosyasına kaydedildi.

## Kullanım Talimatları

1. **Veri Setini Hazırlama:**
   - `flo_data_20K.csv` dosyasını proje dizinine ekleyin.

2. **Veri Analizi ve RFM Hesaplamaları:**
   - Python ortamında, tüm adımları gerçekleştirmek için sağlanan kodları çalıştırın.

3. **Sonuçların İncelenmesi:**
   - Çıktı dosyalarını (`target_female_customers.csv` ve `target_male_kids_customers.csv`) inceleyerek hedef müşteri profillerini gözden geçirin.

## Gereksinimler

- Python 3.x
- pandas kütüphanesi
