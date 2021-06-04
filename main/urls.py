from django.conf.urls import url
from django.urls import path
from . import views


app_name="main"


urlpatterns=[

	path('',views.index,name='index'),

    path('pdf/merge/', views.merge, name="merge"),
    path('pdf/extract',views.extract_selection,name='es'),
    path('pdf/extract/page/single',views.single_page_extract,name='sp'),
    path('pdf/ectract/page/range',views.multiple_pages_extract,name='mp'),

    path('pdf/convert',views.conversion_selection,name='ctype'),
    path('pdf/convert/word',views.pdf_word_convert,name="cword"),

    path('pdf/optimize',views.pdf_optimize,name="p-optimize"),
    path('pdf/resize',views.pdf_resize,name='p-resize')


] 

