import pdf2image
import os, fnmatch
from PyPDF2 import PdfFileWriter, PdfFileReader

def ConvertPDF2Image(pdf_folder, file_name,image_folder):
    pdf = PdfFileReader(open(pdf_folder + '\\' + file_name, 'rb'))
    max_page_count = pdf.numPages
    pdf = pdf_folder + '\\' + file_name
    main_file_name = file_name[:-4]

    for page in range(1, max_page_count + 1, 10) :
        pil_images = pdf2image.convert_from_path(pdf, dpi = 500, first_page=page,
                                                 last_page = min(page + 10 - 1, max_page_count),
                                                 fmt= 'jpeg', thread_count = 4,
                                                 userpw = None,
                                                 use_cropbox = False,
                                                 strict = False)
        SavePDFPage2Image(pil_images, page, image_folder, main_file_name)

def SavePDFPage2Image(pages, index, image_folder, main_file_name):
    for page in pages:
        page.save(image_folder + '\\' + main_file_name + '_p' + str(index) + '.jpg', 'jpeg')
        index = index + 1

def main():
    pdf_folder = 'path of pdf'
    image_folder = 'path of images saved'
    file_names = fnmatch.filter(os.listdir(pdf_folder), '*.pdf')
    for file_name in file_names:
        print('Convert ' + file_name + ' to Image')
        ConvertPDF2Image(pdf_folder, file_name,image_folder)

if __name__ == '__main__':
    main()

