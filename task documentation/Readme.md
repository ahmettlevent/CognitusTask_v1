 - Projede istenen Cognitus backend ekibinin bir gorevi olarak algoritma implementasyonunu uctan uca tamamlamakdir
- algorithm.py ornek olarak Machine Learning ekibinden iletilen classification kodunu icermektedir.
- Kodun icerisinde ornek bir datayi file'dan okuyan bir kod blogu
- Datayi train eden bir kod blogu
- Ardindan da prediction yapan bir kod blogu bulunmaktadir.

Django Application
==================
- Algoritmanin calisabilmesi icin text, label seklinde iki tane text field'a
  ihtiyac vardir. Bu bilgileri kaydetmek icin Data adinda django model olusturulur.
- Restfull servisler olusturularak kullanicinin api ustunden data eklemesine,
  gunellemesine, silmesine, listelemesine olanak saglanir.
- Bir train endpointi tasarlanarak asagida belirtecegim Flask servisindeki train endpointi tetiklenir.
- Bir prediction endpointi tasarlanarak asagida belirtecegim Flask servisindeki prediction endpointine prediction istegi atilir ve sonucu servisten aldiktan sonra kullaniciya donulur.


Flask Application
=================

- Iki adet endpointi olmalidir. Train ve predict

Train - Servis olarak bir input almasi gerekmemektedir.
    - Train kodlari kullaniciyi bloke etmemek adina celery vasitasiyla async olarak calistirilmalidir.
    - Production sisteminde kullanicinin datasini file olarak tasiyamayacagimiz icin database'den okumamiz gerekmektedir. Algoritmanin icindeki datayi filedan okuyan kod blogu degistirilmelidir. Django uygulamasinda kullanilan db'ye baglanacak sekilde konfigurasyon yapilir ardindan bu tablodaki veriler okunup algoritmaya iletilir.(duz sql de yazilabilir, sqlalchemy yardimiyla mevcut django modellerine baglanacak sekilde konfigurasyon da yapilabilir. Tercih size ait)
    - Algoritma ciktisindaki model.pickle ve vectorizer.pickle dosyalari docker icerisinde uygun gorulen bir path'e yazilir.

Predict - API input olarak bir text gelecek sekilde kodlanmalidir.
    - Train ciktisi olarak olusturulan pickle dosyalarinin yardimiyla prediction kodu calistirilir ve api'den json olarak return edilir.

Dikkat edilmesi gerekenler
==========================
- Yazilan kodlarin tamami docker containerlarinda calistirilmasi gerekmektedir. docker-compose kullanarak containerlar calistirilabilir. Asagida beklenen container listesi ve aciklamalari yazmaktadir.

Services:
  - db(postgresql, mysql farketmez). Veri kaybini onlemek adina db'nin data path'i volume olarak tanimlanmalidir.
  - web - Django uygulamasinin calistigi container. Data CRUD islemleri ve train predict endpointleriyle flask uygulamasini cagirir.
  - algorithm - Train ve predict servislerini barindirir.
  - algorithm_celery - Flask uygulamasinda baslatilan train kodlarinin calistigi container. Cikti olarak olusan model ve vectorizer dosyalarini volume olarak tanimlamak gerekmektedir. Ayni volume algorithm container'ina da verilmelidir ki train olan pickle dosyalarini okuyup prediction calistirabilsin.
 - redis - algorithm ve algorithm_celery containerlari arasinda broker gorevi gorur





NOTE
====
- Kodda anlasilmayan yer olmasi halinde mesai saatleri icerisinde faruk.rahmet@etiya.com ile cekinmeden iletisime gecebilirsiniz.
