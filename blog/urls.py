from django.conf.urls import include, url
from blog import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='homepage'),
    url(r'^soru-olustur/$', views.SoruSorFormView.as_view(), name='soru_olustur'),
    url(r'^soru-detay/(?P<id>[\d]+)/$', views.SoruCevapView.as_view(), name='soru_detay'),
    url(r'^cevap-olustur/(?P<id>[\d]+)/$', views.CevapFormView.as_view(), name='cevap_detay'),
    url(r'^soru-oy-kullan/(?P<id>[\d]+)/$', views.SoruOyView.as_view(), name='soru_oy_kullan'),
    url(r'^cevap-oy-kullan/(?P<id>[\d]+)/$', views.CevapOyView.as_view(), name='cevap_oy_kullan')
]
