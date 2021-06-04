from django.shortcuts import render
from django.http import FileResponse
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from pdfrw import PdfReader, PdfWriter
import os
from django.conf import settings
import shortuuid

from .forms import *
import PyPDF2
import zipfile


def index(request):
	return render(request,'base.html')
def extract_selection(request):
    return render(request,'main/extract_select.html')
def conversion_selection(request):
    return render(request,'main/conversion_select.html')

def merge(request):
    if request.method == 'POST':        
        form = PdfMergeForm(request.POST, request.FILES)
        if form.is_valid():            
            pdf1 = form.cleaned_data['pdf1']            
            pdf2 = form.cleaned_data['pdf2']            
            
            pdf_list = [pdf1, pdf2]
            
            pdfMerger = PyPDF2.PdfFileMerger()

            
            for pdfs in pdf_list:
                if pdfs:
                    pdfFileObj = PyPDF2.PdfFileReader(pdfs)
                    pdfMerger.append(pdfFileObj,import_bookmarks=False)
            
            with open(os.path.join('media', 'merged_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerger.write(pdfOutputFile)
            
            response = FileResponse(open(os.path.join('media', 'merged_file.pdf'), 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'

            return response
        else:
            form=PdfMergeForm()
    else:
        form=PdfMergeForm()
    return render(request, 'main/merge.html', {'form': form})

def single_page_extract(request):
    if request.method == 'POST':        
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():            
            f = form.cleaned_data['file']            
            pdfFileObj = PyPDF2.PdfFileReader(f)           
            page_num_list = form.cleaned_data['page'].split(',')            
            zf = zipfile.ZipFile(os.path.join('media', 'extracted_pages.zip'), 'w')

            for page_num in page_num_list:            
                page_index = int(page_num) - 1            
                pageObj = pdfFileObj.getPage(page_index)           
                pdfWriter = PyPDF2.PdfFileWriter()           
                pdfWriter.addPage(pageObj)            
                pdf_file_path = os.path.join('media', 'extracted_page_{}.pdf'.format(page_num))            
                with open(pdf_file_path, 'wb') as pdfOutputFile:
                    pdfWriter.write(pdfOutputFile)            
                zf.write(pdf_file_path)
            zf.close()
            
            response = FileResponse(open(os.path.join('media', 'extracted_pages.zip'), 'rb'))
            response['content_type'] = "application/zip"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.zip"'
            return response

    else:
        
        form = PdfExtractForm()

    return render(request, 'main/single_page_extract.html', {'form': form})

def multiple_pages_extract(request):
    if request.method == 'POST':        
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():           
            f = form.cleaned_data['file']            
            pdfFileObj = PyPDF2.PdfFileReader(f)
            page_range = form.cleaned_data['page'].split('-')
            page_start = int(page_range[0])
            page_end = int(page_range[1])            
            pdf_file_path = os.path.join('media', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))
            pdfOutputFile = open(pdf_file_path, 'ab+')            
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end + 1):               
                page_index = int(page_num) - 1               
                pageObj = pdfFileObj.getPage(page_index)                
                pdfWriter.addPage(pageObj)

            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

            extractedPage = open(pdf_file_path, 'rb')
            response = FileResponse(extractedPage)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.pdf"'

            return response
    else:
        
        form = PdfExtractForm()

    return render(request, 'main/multiple_range_extract.html', {'form': form})

def pdf_word_convert(request):
    if request.method=='POST':
        form=PdfWordConvertForm(request.POST,request.FILES)
        if form.is_valid():
            f=form.cleaned_data['pdf_file']
            pdfFileObj=PyPDF2.PdfFileReader(f)
            pdfOutputFile = pdfFileObj.getPage(0)
            converted_file=pdfOutputFile.extractText()

           # with open(os.path.join('media', 'converted.docx'), 'wb') as pdfOutputFile:
               # pdfOutputFile.write(pdfOutputFile) 
            response = FileResponse(converted_file, 'rb')
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="converted.docx"'
            return response

                

            

    else:
        form=PdfWordConvertForm()           

    return render(request,'main/pdf_word_convert.html',{'form':form})

def pdf_optimize(request):
    if request.method=='POST':
        form=PdfOptmizeForm(request.POST,request.FILES)
        if form.is_valid():
            f=form.cleaned_data['pdf_file']
            pdfFileObj=PyPDF2.PdfFileReader(f)

    else:
        form=PdfOptimizeForm()

    return render(request,'main/optimize.html',{'form':form})

def pdf_resize(request):
    if request.method=='POST':
        form=PdfResizeForm(request.POST,request.FILES)
        if form.is_valid():
            f=form.cleaned_data['pdf_file']
            pdfFileObj=PyPDF2.PdfFileReader(f)

    else:
        form=PdfResizeForm()

    return render(request,'main/resize.html',{'form':form})
