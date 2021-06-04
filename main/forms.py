from django import forms


class PdfMergeForm(forms.Form):
    pdf1 = forms.FileField(label="PDF file 1")
    pdf2 = forms.FileField(label="PDF file 2", required=False)

class PdfExtractForm(forms.Form):
    file = forms.FileField(label="Upload PDF Document")
    page = forms.CharField(max_length=20, label="Page Number")

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Only pdf documents are allowed. ")
        return file


class PdfReplaceForm(forms.Form):
    file1 = forms.FileField(label="Replacement page")
    file2 = forms.FileField(label="PDF document to be replaced")
    page = forms.IntegerField(label="Replace page number")

class PdfWordConvertForm(forms.Form):
    pdf_file=forms.FileField(label='Upload the pdf to be converted')


class PdfOptimizeForm(forms.Form):
    pdf_file=forms.FileField(label='Upload the pdf to be Optimised')

class PdfResizeForm(forms.Form):
    pdf_file=forms.FileField(label='Upload the pdf to be resized')