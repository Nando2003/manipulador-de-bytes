from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.conf import settings
from manipulador_arquivos.forms import UploadForm
from django.http import FileResponse, HttpRequest, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from webdav3.client import Client
import requests
import os
import tempfile

# Create your views here.
    
class HomeView2(FormView):
    template_name = 'manipulador/homepage.html'
    form_class = UploadForm
    success_url = reverse_lazy('home-page')

    def get(self, request):
        files = self.listing_file()
        upload_form = self.form_class

        return render(request, self.template_name, {'upload_form' : upload_form, 'files': files})
    
    def post(self, request):

        local_path_upload = 'manipulador_arquivos/temp-file'
        local_path_download = os.path.join(tempfile.gettempdir(), 'temp-file-download')

        form = self.get_form()
        
        if form.is_valid():
            upload_file = form.cleaned_data['upload_file']
            file_name = upload_file.name
            file_path = local_path_upload + '/' + file_name

            self.upload_file(file_name, local_path_upload)
            return super().post(request)

        action = request.POST.get('action')
        selected_file = request.POST.get('download')

        if selected_file is None:
            return redirect('home-page')
        
        if action == 'delete':
            self.delete_file(selected_file)
            return redirect('home-page')
        
        self.download_file(selected_file, local_path_download)
        return FileResponse(open(local_path_download, 'rb'), as_attachment=True, filename=selected_file)
    
    def listing_file(self):

        options = {
            'webdav_hostname': settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example',
            'webdav_login': settings.WEBDAV_USERNAME,
            'webdav_password': settings.WEBDAV_PASSWORD
        }

        client = Client(options)

        return (client.list())[1:]
    
    def download_file(self, file_name, local_path):

        webdav_url = settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example/{file_name}'
        webdav_login = settings.WEBDAV_USERNAME
        webdav_password = settings.WEBDAV_PASSWORD

        response_get = requests.get(webdav_url, auth=(webdav_login, webdav_password))

        with open(local_path, 'wb') as f:
            f.write(response_get.content)

    def upload_file(self, file_name, local_path):
        webdav_url = settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example/{file_name}'
        webdav_login = settings.WEBDAV_USERNAME
        webdav_password = settings.WEBDAV_PASSWORD

        file_path = file_name + '/' + local_path
        
        if os.path.exists(local_path):
            with open(file_path, 'rb') as arquivo:
                resposta = requests.put(
                    webdav_url,
                    auth=(webdav_login, webdav_password),
                    data=arquivo,
                )

    def delete_file(self, file_name):
        webdav_url = settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example/{file_name}'
        webdav_login = settings.WEBDAV_USERNAME
        webdav_password = settings.WEBDAV_PASSWORD

        requests.delete(webdav_url, auth=(webdav_login, webdav_password))

class HomeView(FormView):
    template_name = 'manipulador/homepage.html'
    form_class = UploadForm
    success_url = reverse_lazy('home-page')

    def get(self, request):
        files = self.listing_file()
        upload_form = self.form_class

        return render(request, self.template_name, {'upload_form' : upload_form, 'files': files})
    
    def post(self, request):

        form = self.get_form()
        
        if form.is_valid():
            upload_file = form.cleaned_data['upload_file']
            file_name = upload_file.name
            file_path = f"manipulador_arquivos/upload-file/{file_name}"

            with open(file_path,'wb') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

            self.upload_file(file_name, file_path)

            return super().post(request)

        download_path = os.path.join(tempfile.gettempdir(), 'temp-file-download')
        action = request.POST.get('action')
        selected_file = request.POST.get('download')

        if selected_file is None:
            return redirect('home-page')
        
        if action == 'delete':
            self.delete_file(selected_file)
            return redirect('home-page')
        
        self.download_file(selected_file, download_path)
        return FileResponse(open(download_path, 'rb'), as_attachment=True, filename=selected_file)
    
    def listing_file(self):

        options = {
            'webdav_hostname': settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example',
            'webdav_login': settings.WEBDAV_USERNAME,
            'webdav_password': settings.WEBDAV_PASSWORD
        }

        client = Client(options)

        return (client.list())[1:]
    
    def upload_file(self, file_name, local_path):

        webdav_url = settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example/{file_name}'
        webdav_login = settings.WEBDAV_USERNAME
        webdav_password = settings.WEBDAV_PASSWORD
        
        if os.path.exists(local_path):
            with open(local_path, 'rb') as arquivo:
                requests.put(webdav_url, auth=(webdav_login, webdav_password), data=arquivo,)
        
        os.remove(local_path)

    def download_file(self, file_name, local_path):

        webdav_url = settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example/{file_name}'
        webdav_login = settings.WEBDAV_USERNAME
        webdav_password = settings.WEBDAV_PASSWORD

        response_get = requests.get(webdav_url, auth=(webdav_login, webdav_password))

        with open(local_path, 'wb') as f:
            f.write(response_get.content)

    def delete_file(self, file_name):
        webdav_url = settings.WEBDAV_URL + f'remote.php/dav/files/{settings.WEBDAV_USERNAME}/Temp-File-Nando-Example/{file_name}'
        webdav_login = settings.WEBDAV_USERNAME
        webdav_password = settings.WEBDAV_PASSWORD

        requests.delete(webdav_url, auth=(webdav_login, webdav_password))