from django.contrib import admin
from .models import Kriteria, Anak, NilaiKriteriaAnak, Tipe, NilaiKepentingan

# ============================= Tipe ============================
class TipeAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)
    ordering = ('nama',)

admin.site.register(Tipe, TipeAdmin)


# ============================= Nilai Kepentingan ============================
class NilaiKepentinganAdmin(admin.ModelAdmin):
    list_display = ('nilai', 'deskripsi')
    search_fields = ('nilai', 'deskripsi')
    ordering = ('nilai',)

admin.site.register(NilaiKepentingan, NilaiKepentinganAdmin)


# ============================= Kriteria ============================
class KriteriaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bobot', 'tipe', 'nilai_kepentingan')
    search_fields = ('nama', 'tipe__nama', 'nilai_kepentingan__deskripsi')
    list_filter = ('tipe', 'nilai_kepentingan')
    ordering = ('nama',)

admin.site.register(Kriteria, KriteriaAdmin)


# ============================= Anak ============================
class AnakAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tanggal_lahir')
    search_fields = ('nama',)
    ordering = ('nama',)
    date_hierarchy = 'tanggal_lahir'

admin.site.register(Anak, AnakAdmin)


# ======================== Nilai Kriteria Anak =========================
class NilaiKriteriaAnakAdmin(admin.ModelAdmin):
    list_display = ('anak_name', 'kriteria_name', 'nilai')
    search_fields = ('anak__nama', 'kriteria__nama')
    list_filter = ('kriteria',)
    ordering = ('anak', 'kriteria')

    def anak_name(self, obj):
        return obj.anak.nama
    anak_name.short_description = 'Anak'

    def kriteria_name(self, obj):
        return obj.kriteria.nama
    kriteria_name.short_description = 'Kriteria'

admin.site.register(NilaiKriteriaAnak, NilaiKriteriaAnakAdmin)
