from django.db import models
    
class Tipe(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class NilaiKepentingan(models.Model):
    nilai = models.FloatField()
    deskripsi = models.CharField(max_length=200)

    def __str__(self):
        return f"Nilai: {self.nilai}, Deskripsi: {self.deskripsi}"


class Kriteria(models.Model):
    nama = models.CharField(max_length=100)
    bobot = models.FloatField(null=True, default=0.0)
    tipe = models.ForeignKey(Tipe, on_delete=models.SET_NULL, null=True)  # Relasi ke Tipe
    nilai_kepentingan = models.ForeignKey(NilaiKepentingan, on_delete=models.SET_NULL, null=True)  # Relasi ke NilaiKepentingan
    menggunakan_range = models.BooleanField(default=False)  # Tambahan
    nilai_min = models.FloatField(null=True, blank=True)  # Minimum value for normalization
    nilai_max = models.FloatField(null=True, blank=True)  # Maximum value for normalization
    
    def __str__(self):
        return self.nama


    
class RangeKategori(models.Model):
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='range_kategori')
    nama = models.CharField(max_length=100)
    nilai = models.FloatField()

    def __str__(self):
        return f"{self.nama} ({self.nilai})"


class Anak(models.Model):
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    
    def __str__(self):
        return self.nama

class NilaiKriteriaAnak(models.Model):
    anak = models.ForeignKey(Anak, on_delete=models.CASCADE, related_name='nilai_kriteria')
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='nilai_anak')
    nilai = models.FloatField()
    
    def is_using_range(self):
        return self.kriteria.menggunakan_range

    def __str__(self):
        return f"{self.kriteria.nama}: {self.nilai}"
