from django import forms
from .models import Anak

class AnakForm(forms.ModelForm):
    class Meta:
        model = Anak
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


from .models import NilaiKriteriaAnak


class NilaiKriteriaAnakForm(forms.ModelForm):
    class Meta:
        model = NilaiKriteriaAnak
        fields = ['anak', 'kriteria', 'nilai']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Styling semua field
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Logika dropdown/input
        if 'kriteria' in self.data:
            try:
                kriteria_id = int(self.data.get('kriteria'))
                kriteria = self.fields['kriteria'].queryset.get(id=kriteria_id)

                if kriteria.menggunakan_range:
                    self.fields['nilai'].widget = forms.Select(
                        choices=[(rk.nilai, rk.nama) for rk in kriteria.range_kategori.all()]
                    )
                else:
                    self.fields['nilai'].widget = forms.NumberInput()
            except (ValueError, TypeError):
                pass  # Jika tidak ada kriteria valid dalam data

        elif self.instance.pk and self.instance.kriteria.menggunakan_range:
            self.fields['nilai'].widget = forms.Select(
                choices=[(rk.nilai, rk.nama) for rk in self.instance.kriteria.range_kategori.all()]
            )
        else:
            self.fields['nilai'].widget = forms.NumberInput()
       
from .models import Kriteria, RangeKategori

class KriteriaForm(forms.ModelForm):
    class Meta:
        model = Kriteria
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Ubah widget menggunakan_range menjadi checkbox
        self.fields['menggunakan_range'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
            
class RangeKategoriForm(forms.ModelForm):
    class Meta:
        model = RangeKategori
        fields = ['nama', 'nilai']