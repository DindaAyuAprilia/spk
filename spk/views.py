from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Anak
from .forms import AnakForm

def homepage(request):
    return render(request, 'base.html')

# Daftar Anak (Index)
def anak_index(request):
    query = request.GET.get('q', '')
    if query:
        anak_list = Anak.objects.filter(nama__icontains=query)
    else:
        anak_list = Anak.objects.all()
    
    return render(request, 'anak/index.html', {'anak_list': anak_list, 'query': query})

# Tambah Anak (Create)
def anak_create(request):
    if request.method == 'POST':
        form = AnakForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('anak_index')
    else:
        form = AnakForm()
    return render(request, 'anak/create.html', {'form': form})

# Ubah Anak (Update)
def anak_update(request, anak_id):
    anak = get_object_or_404(Anak, id=anak_id)
    if request.method == 'POST':
        form = AnakForm(request.POST, instance=anak)
        if form.is_valid():
            form.save()
            return redirect('anak_index')
    else:
        form = AnakForm(instance=anak)
    return render(request, 'anak/update.html', {'form': form, 'anak': anak})

# Hapus Anak (Delete)
def anak_delete(request, anak_id):
    if request.method == 'POST':
        anak = get_object_or_404(Anak, id=anak_id)
        anak.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

from .models import NilaiKriteriaAnak
from .forms import NilaiKriteriaAnakForm

# Daftar Nilai Kriteria Anak (Index)
def nilai_kriteria_anak_index(request):
    nilai_list = NilaiKriteriaAnak.objects.select_related('anak', 'kriteria').all()
    return render(request, 'nilai_kriteria_anak/index.html', {'nilai_list': nilai_list})

def is_range(request, kriteria_id):
    kriteria = Kriteria.objects.get(id=kriteria_id)
    return JsonResponse({'using_range': kriteria.menggunakan_range})


def get_ranges(request, kriteria_id):
    ranges = RangeKategori.objects.filter(kriteria_id=kriteria_id).values('id', 'nama', 'nilai')
    return JsonResponse({'ranges': list(ranges)})


def nilai_kriteria_anak_create(request):
    if request.method == 'POST':
        form = NilaiKriteriaAnakForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nilai_kriteria_anak_index')
    else:
        form = NilaiKriteriaAnakForm()

    return render(request, 'nilai_kriteria_anak/create.html', {'form': form})


# Endpoint untuk mendapatkan data range kategori
def get_range_kategori(request, kriteria_id):
    try:
        kriteria = Kriteria.objects.get(id=kriteria_id)
        if kriteria.menggunakan_range:
            range_kategori = kriteria.range_kategori.values('id', 'nama', 'nilai')
            return JsonResponse({'using_range': True, 'choices': list(range_kategori)})
    except Kriteria.DoesNotExist:
        pass
    return JsonResponse({'using_range': False})

# # Create nilai Kriteria Anak
# def nilai_kriteria_anak_create(request):
#     if request.method == 'POST':
#         form = NilaiKriteriaAnakForm(request.POST)
#         if form.is_valid():
#             nilai = form.save(commit=False)
            
#             # Check if the kriteria uses range
#             if nilai.kriteria.menggunakan_range:
#                 # Check if the value is within the valid range
#                 range_obj = RangeKategori.objects.filter(kriteria=nilai.kriteria, nilai=nilai.nilai).first()
#                 if not range_obj:
#                     form.add_error('nilai', 'Nilai harus berasal dari range kriteria.')
#                     return render(request, 'nilai_kriteria_anak/create.html', {'form': form})
#                 nilai.nilai = range_obj.nilai  # Save the value from the range
#             else:
#                 # If not using range, use the manual input value
#                 nilai.nilai = form.cleaned_data['nilai_input']
                
#             nilai.save()
#             return redirect('nilai_kriteria_anak_index')
#     else:
#         form = NilaiKriteriaAnakForm()
    
#     return render(request, 'nilai_kriteria_anak/create.html', {'form': form})


# # Ubah Nilai Kriteria Anak (Update)
# def nilai_kriteria_anak_update(request, pk):
#     nilai_kriteria = get_object_or_404(NilaiKriteriaAnak, pk=pk)
#     if request.method == 'POST':
#         form = NilaiKriteriaAnakForm(request.POST, instance=nilai_kriteria)
#         if form.is_valid():
#             nilai = form.save(commit=False)
#             if nilai.kriteria.menggunakan_range:
#                 nilai_range = form.cleaned_data['nilai']
#                 nilai.nilai = nilai_range.nilai
#             nilai.save()
#             return redirect('nilai_kriteria_anak_index')
#     else:
#         form = NilaiKriteriaAnakForm(instance=nilai_kriteria)
#     return render(request, 'nilai_kriteria_anak/update.html', {'form': form})


# Hapus Nilai Kriteria Anak (Delete)
def nilai_kriteria_anak_delete(request, nilai_id):
    if request.method == 'POST':
        nilai = get_object_or_404(NilaiKriteriaAnak, id=nilai_id)
        nilai.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def wp_result(request):
    # Step 1: Ambil semua anak dan nilai kriteria terkait
    nilai_kriteria_list = NilaiKriteriaAnak.objects.select_related('anak', 'kriteria')

    # Step 2: Ambil bobot kriteria dan tipe (Benefit/Cost)
    kriteria_list = Kriteria.objects.all()
    bobot_dict = {kriteria.id: kriteria.bobot for kriteria in kriteria_list}
    tipe_dict = {kriteria.id: kriteria.tipe.nama for kriteria in kriteria_list}

    # Step 3: Hitung nilai S_i untuk setiap anak
    si_dict = {}
    for nilai in nilai_kriteria_list:
        anak_id = nilai.anak.id
        bobot = bobot_dict.get(nilai.kriteria.id, 0.0)
        tipe = tipe_dict.get(nilai.kriteria.id, "Benefit")
        nilai_normalisasi = nilai.nilai

        if tipe == "Cost":
            nilai_normalisasi = 1 / nilai.nilai  # Inversi nilai untuk kriteria Cost

        if anak_id not in si_dict:
            si_dict[anak_id] = 1  # Inisialisasi S_i

        # S_i dihitung dengan perkalian nilai normalisasi yang dipangkatkan bobot
        si_dict[anak_id] *= pow(nilai_normalisasi, bobot)

    # Step 4: Hitung nilai V_i untuk setiap anak
    total_si = sum(si_dict.values())
    vi_dict = {anak_id: si / total_si for anak_id, si in si_dict.items()}

    # Check if the sum of all Vi is 1
    if not (abs(sum(vi_dict.values()) - 1) < 1e-6):
        raise ValueError("The sum of all Vi values is not 1, something went wrong.")

    # Step 5: Siapkan data untuk ditampilkan
    result = [
        {
            "anak": Anak.objects.get(id=anak_id).nama,
            "Si": round(si_dict[anak_id], 4),
            "Vi": round(vi, 4),
        }
        for anak_id, vi in vi_dict.items()
    ]

    # Step 6: Sort the results by Vi in descending order
    result.sort(key=lambda x: x['Vi'], reverse=True)

    # Step 7: Kirim hasil ke template
    return render(request, 'nilai_kriteria_anak/wp_result.html', {'results': result})


# ====================================================================
from django.http import JsonResponse
from .models import Kriteria
from .forms import KriteriaForm
import numpy as np

# Fungsi untuk menghitung bobot AHP
def hitung_bobot_ahp(request):
    kriteria = Kriteria.objects.all()
    jumlah_kriteria = kriteria.count()
    print(f"Jumlah kriteria: {jumlah_kriteria}")
    if jumlah_kriteria < 2:
        return JsonResponse({'status': 'error', 'message': 'Tidak cukup kriteria untuk perhitungan AHP.'})

    matriks = np.ones((jumlah_kriteria, jumlah_kriteria))
    nilai_kepentingan = [k.nilai_kepentingan.nilai for k in kriteria]
    print(f"Nilai Kepentingan: {nilai_kepentingan}")

    # Membuat matriks perbandingan
    for i in range(jumlah_kriteria):
        for j in range(jumlah_kriteria):
            if i != j:
                matriks[i][j] = nilai_kepentingan[i] / nilai_kepentingan[j]

    # Normalisasi matriks
    kolom_sum = np.sum(matriks, axis=0)
    matriks_normalisasi = matriks / kolom_sum
    bobot = np.mean(matriks_normalisasi, axis=1)

    print(f"Bobot yang dihitung: {bobot}")

    # Update bobot untuk setiap kriteria
    for idx, k in enumerate(kriteria):
        k.bobot = bobot[idx]
        k.save()
        print(f"Bobot kriteria {k.nama} diupdate menjadi {k.bobot}")

    return JsonResponse({'status': 'success', 'message': 'Bobot berhasil dihitung dan diperbarui.'})

# # Fungsi untuk menambah kriteria
# def kriteria_create(request):
#     if request.method == 'POST':
#         jumlah_kriteria = int(request.POST.get('jumlah_kriteria', 0))
#         forms = []
        
#         # Membuat form sesuai dengan jumlah yang dipilih
#         for i in range(jumlah_kriteria):
#             form_data = {key: value for key, value in request.POST.items() if key.startswith(f"form-{i}-")}
#             form = KriteriaForm(form_data)
#             forms.append(form)

#         if all(form.is_valid() for form in forms):  # Memeriksa apakah semua form valid
#             for form in forms:
#                 form.save()

#             # Hitung bobot AHP setelah data disimpan
#             hitung_bobot_ahp()

#             return redirect('kriteria_index')
#         else:
#             # Jika form tidak valid, tampilkan error
#             print(forms[0].errors)  # Tampilkan kesalahan untuk debugging
#     else:
#         forms = []
#         jumlah_kriteria = 0

#     return render(request, 'kriteria/create.html', {
#         'forms': forms,
#         'jumlah_kriteria': jumlah_kriteria
#     })

# Fungsi untuk membuat kriteria baru
def kriteria_create(request):
    if request.method == 'POST':
        form = KriteriaForm(request.POST)
        if form.is_valid():
            form.save()  # Menyimpan data kriteria yang valid
            return redirect('kriteria_index')  # Mengalihkan ke daftar kriteria
    else:
        form = KriteriaForm()
    
    return render(request, 'kriteria/create.html', {'form': form})


# Daftar Kriteria (Read)
def kriteria_index(request):
    kriteria_list = Kriteria.objects.all()
    return render(request, 'kriteria/index.html', {'kriteria_list': kriteria_list})

# Fungsi untuk menghapus semua data kriteria
def delete_all_kriteria(request):
    Kriteria.objects.all().delete()
    return redirect('kriteria_create')


def kriteria_delete(request, kriteria_id):
    if request.method == 'POST':
        kriteria = get_object_or_404(Kriteria, id=kriteria_id)
        kriteria.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)





# ==================================================



# Index View
def anak_nilai_index(request):
    anak_list = Anak.objects.prefetch_related('nilai_kriteria')
    kriteria_list = Kriteria.objects.all()
    return render(request, 'nilai_anak/index.html', {
        'anak_list': anak_list,
        'kriteria_list': kriteria_list
    })

def anak_nilai_manage(request, anak_id=None):
    kriteria_list = Kriteria.objects.prefetch_related('range_kategori')
    anak = get_object_or_404(Anak, id=anak_id) if anak_id else None

    if request.method == 'POST':
        form = AnakForm(request.POST, instance=anak)
        if form.is_valid():
            anak_instance = form.save()

            # Update NilaiKriteriaAnak
            for kriteria in kriteria_list:
                nilai_input = request.POST.get(f'nilai_{kriteria.id}', 0)
                nilai = (
                    float(nilai_input) if not kriteria.menggunakan_range
                    else RangeKategori.objects.get(id=nilai_input).nilai
                )
                NilaiKriteriaAnak.objects.update_or_create(
                    anak=anak_instance, kriteria=kriteria,
                    defaults={'nilai': nilai}
                )
            return redirect('anak_list')

    else:
        form = AnakForm(instance=anak)

    # Prepare `nilai_kriteria` for template
    nilai_kriteria = []
    for kriteria in kriteria_list:
        if kriteria.menggunakan_range:
            range_options = kriteria.range_kategori.all()
            selected_range = (
                NilaiKriteriaAnak.objects.filter(anak=anak, kriteria=kriteria).first()
            )
            nilai_kriteria.append({
                'kriteria_id': kriteria.id,
                'kriteria_nama': kriteria.nama,
                'range_options': range_options,  # Provide range options
                'selected_range': selected_range.nilai if selected_range else '',
                'is_range': True
            })
        else:
            nilai = (
                NilaiKriteriaAnak.objects.filter(anak=anak, kriteria=kriteria).first()
            )
            nilai_kriteria.append({
                'kriteria_id': kriteria.id,
                'kriteria_nama': kriteria.nama,
                'nilai': nilai.nilai if nilai else '',
                'is_range': False
            })

    return render(request, 'nilai_anak/form.html', {
        'form': form,
        'kriteria_list': kriteria_list,
        'nilai_kriteria': nilai_kriteria  # Pass structured data
    })


# Delete Anak
def anak_nilai_delete(request, anak_id):
    if request.method == 'POST':
        anak = get_object_or_404(Anak, id=anak_id)
        anak.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
# ==============================================================
from django.shortcuts import render, get_object_or_404, redirect
from .models import Kriteria, RangeKategori
from .forms import RangeKategoriForm

def range_index(request, kriteria_id):
    kriteria = get_object_or_404(Kriteria, id=kriteria_id)
    ranges = kriteria.range_kategori.all()
    return render(request, 'range/index.html', {'kriteria': kriteria, 'ranges': ranges})

def range_create(request, kriteria_id):
    kriteria = get_object_or_404(Kriteria, id=kriteria_id)
    if request.method == 'POST':
        form = RangeKategoriForm(request.POST)
        if form.is_valid():
            range_kategori = form.save(commit=False)
            range_kategori.kriteria = kriteria
            range_kategori.save()
            return redirect('range_index', kriteria_id=kriteria.id)
    else:
        form = RangeKategoriForm()
    return render(request, 'range/form.html', {'form': form, 'kriteria': kriteria})

def range_edit(request, kriteria_id, range_id):
    kriteria = get_object_or_404(Kriteria, id=kriteria_id)
    range_kategori = get_object_or_404(RangeKategori, id=range_id, kriteria=kriteria)
    if request.method == 'POST':
        form = RangeKategoriForm(request.POST, instance=range_kategori)
        if form.is_valid():
            form.save()
            return redirect('range_index', kriteria_id=kriteria.id)
    else:
        form = RangeKategoriForm(instance=range_kategori)
    return render(request, 'range/form.html', {'form': form, 'kriteria': kriteria})
