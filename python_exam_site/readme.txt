Python Exam Site

Bu proje, Flask ve SQLAlchemy kullanarak basit bir Python sınav platformu oluşturur. Kullanıcılar sınava girerek puanlarını kaydedebilir ve en yüksek puanlarını görebilirler.

-Kurulum-

Gerekli Bağımlılıkları Yükleyin

pip install flask flask-sqlalchemy

Projeyi Çalıştırın

python app.py

-Kullanım-

Ana Sayfa (/): Kullanıcı adı girerek sınava başlama sayfası.

Sınav Başlatma (/start_exam): Kullanıcı adı ile giriş yapılarak sınav başlatılır.

Sınav Sayfası (/exam/<username>): Soruların listelendiği ve cevapların verildiği sayfa.

Sonuç Sayfası (/submit_exam/<username>): Kullanıcının puanını ve genel en yüksek puanı gösterir.

Sonuçları Görüntüleme (/view_results): Tüm kullanıcıların sınav sonuçlarını listeler.

Veritabanını Temizleme (/clear_database): Tüm kayıtları sıfırlar.

-Veri Tabanı-

SQLite kullanılarak oluşturulmuş bir veritabanı bulunmaktadır.

User (Kullanıcılar)

id (int, Primary Key)

username (str, unique)

highest_score (int, varsayılan 0)

last_score (int, varsayılan 0)

Exam (Sınavlar)

id (int, Primary Key)

score (int)

user_id (int, Foreign Key)

answers (JSON, kullanıcı cevapları)

-Sorular-

Sınav soruları questions listesinde saklanmaktadır. Sorular Flask, Discord.py, TensorFlow, NLTK, BeautifulSoup gibi Python kütüphanelerine dayalıdır.

-Notlar-

Veritabanı exam.db olarak SQLite kullanmaktadır.

db.create_all() ile veritabanı tabloları oluşturulur.

Debug modu açık olarak çalıştırılmaktadır.

Kullanıcı sınavı tamamladıktan sonra en yüksek puanı güncellenir.
**Ekstra Olarak Yaptıklarım**  

- En yüksek skoru alan kullanıcıları listeledim.  
  - Sadece en yüksek puanı alan tek bir kişiyi göstermek yerine, aynı skoru alan tüm kullanıcıları ekrana yansıttım.  

- Kullanıcının en son aldığı skoru da kaydettim.  
  - **highest_score** dışında **last_score** değişkenini ekleyerek, kullanıcının en son sınav sonucunu da sakladım.  

- Her kullanıcı için sınav geçmişini tuttum.  
  - Kullanıcının tüm sınavlarının cevaplarını JSON formatında kaydederek, geçmiş sınavlara dair detaylı bir kayıt oluşturdum.  

- HTML sayfalarını destekledim.  
  - **index.html**, **exam.html**, **result.html**, **view_results.html** gibi sayfalar oluşturarak, sınav sürecini kullanıcı dostu bir arayüze taşıdım.  

- Global en yüksek skor bilgisini daha görünür hale getirdim.  
  - Hem sınav ekranında hem de sonuç sayfasında, kullanıcıların rekabet edebilmesi için en yüksek skoru gösterdim.  

- Kullanıcıyı sisteme otomatik ekledim.  
  - Eğer bir kullanıcı daha önce veritabanında yoksa, sınava başlarken onu otomatik olarak oluşturdum. Böylece ekstra bir kayıt işlemi yapmasına gerek kalmadan sınava başlayabilmesini sağladım.