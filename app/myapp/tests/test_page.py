from django.test import TestCase, Client
from django.views import *
from myapp.models import *
from myapp import urls
from myapp.utils.tableUploader import uploadFileToDB
from myapp.utils.csvToXlsx import csvToXlsx
from django.urls import reverse, resolve
# Create your tests here.


class TestIntegrity(TestCase, Client):
    page_names = urls.page_names

    def test_page(self):
        client = Client()
        for i in self.page_names:
            print("Testing " + i)
            response = client.get(reverse(i))
            self.assertEquals(response.status_code, 200)

    def test_fileupload(self):
        raised = False
        try:
            uploadFileToDB("./static/dataset/testdatabase-with-names.csv")
            uploadFileToDB("./static/dataset/testdatabase-with-names.xlsx")
        except Exception as e:
            print("@fileUpload")
            print(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def test_filetransfer(self):
        raised = False
        try:
            csvToXlsx("./static/dataset/testdatabase-with-names.csv", True)
        except Exception as e:
            print("@fileTransfer")
            print(e)
            raised = True
        finally:
            self.assertEqual(raised, False)
