
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    
    path('anak/', views.anak_index, name='anak_index'),
    path('anak/create/', views.anak_create, name='anak_create'),
    path('anak/update/<int:anak_id>/', views.anak_update, name='anak_update'),
    path('anak/delete/<int:anak_id>/', views.anak_delete, name='anak_delete'),
    path('anak/list/', views.anak_nilai_index, name='anak_list'),
    
    path('wp_method/', views.wp_result, name='wp_method'),
    
    
    path('nilai_kriteria_anak/', views.nilai_kriteria_anak_index, name='nilai_kriteria_anak_index'),
    path('nilai_kriteria_anak/create/', views.nilai_kriteria_anak_create, name='nilai_kriteria_anak_create'),
    # path('nilai_kriteria_anak/update/<int:nilai_id>/', views.nilai_kriteria_anak_update, name='nilai_kriteria_anak_update'),
    path('nilai_kriteria_anak/delete/<int:nilai_id>/', views.nilai_kriteria_anak_delete, name='nilai_kriteria_anak_delete'),
    
    path('kriteria/', views.kriteria_index, name='kriteria_index'),
    path('delete_all/', views.delete_all_kriteria, name='delete_all_kriteria'),
    path('create/', views.kriteria_create, name='kriteria_create'),
    path('kriteria/delete/<int:kriteria_id>/', views.kriteria_delete, name='kriteria_delete'),
    path('hitung_bobot_ahp/', views.hitung_bobot_ahp, name='hitung_bobot_ahp'),
    
    # Read Range
    path('kriteria/<int:kriteria_id>/range/', views.range_index, name='range_index'),

    # Create Range
    path('kriteria/<int:kriteria_id>/range/create/', views.range_create, name='range_create'),

    # Edit Range
    path('kriteria/<int:kriteria_id>/range/<int:range_id>/edit/', views.range_edit, name='range_edit'),
    
    path('is_range/<int:kriteria_id>/', views.is_range, name='is_range'),
    path('get_ranges/<int:kriteria_id>/', views.get_ranges, name='get_ranges'),
    path('get-range-kategori/<int:kriteria_id>/', views.get_range_kategori, name='get_range_kategori'),
    
    path('manage/<int:anak_id>/', views.anak_nilai_manage, name='anak_nilai_manage'),
    path('manage/', views.anak_nilai_manage, name='anak_nilai_manage'),
    path('anak/nilai/delete/<int:anak_id>/', views.anak_nilai_delete, name='anak_nilai_delete'),

]