from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.views import *

from myapp.datapipe.predUploadedFile import predictUploadedFile
from myapp.models import *
from myapp import urls
from myapp.utils.tableUploader import uploadFileToDB
from myapp.utils.csvToXlsx import csvToXlsx
from myapp.utils.task import CreateTrainModelPeriodicallyThread, train_model_periodically
from myapp.utils.customize_config import customize_config
from myapp.datapipe import *
from myapp.datapipe.backbone import createBackBone
from myapp.pred import *
from myapp.pred.entity import Entity
from myapp.pred.load_config import load_config, ConfigNotFoundError
from myapp.pred.load_model import load_model, ModelNotFoundError
from django.urls import reverse, resolve

# import the logging library
import logging
from pathlib import Path
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your tests here.


class TestIntegrity(TestCase, Client):
    page_names = urls.page_names

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_page(self):
        client = Client()
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        for i in self.page_names:
            print("\n======================" + "Testing " + i + "===========================")
            response = self.client.get(reverse(i))
            self.assertEquals(response.status_code, 200)
            print("====================================================================\n")

    '''
    def test_fileupload(self):
        print("\n======================" + "Testing File Upload" + "===========================")
        raised = False
        try:
            uploadFileToDB("./static/dataset/testdatabase-with-names.csv")
            uploadFileToDB("./static/dataset/testdatabase-with-names.xlsx")
        except Exception as e:
            logger.error("@fileUpload")
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)
            print("========================================================================\n")

    def testCreateDataPipe(self):
        raised = False
        try:
            backbone = createBackBone(init=True)
        except Exception as e:
            logger.error("@createDataPipe")
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def testCreateModel(self):
        raised = False
        try:
            entity = Entity()
        except Exception as e:
            logger.error("@createModel")
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def testMLtrain(self):
        raised = False
        try:
            entity = Entity()
            entity.train(usedataset=True, model_init=True, savemodel=False)
        except Exception as e:
            logger.error("@TrainModel")
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def testMLtest(self):
        raised = False
        error = None
        try:
            entity = Entity()
            entity.test(usedataset=True)
        except Exception as e:
            logger.error("@TestModel")
            logger.error(e)
            raised = True
        finally:
            if error:
                print(error)
            self.assertEqual(raised, False)

    def testMLPred(self):
        raised = False
        error = None
        try:
            entity = Entity()
            entity.predict(usedataset=True)
        except Exception as e:
            logger.error("@ModelPrediction")
            logger.error(e)
            raised = True
            error = e
        finally:
            if error:
                print(error)
            self.assertEqual(raised, False)

    def testDataPipeReadData(self):
        raised = False
        error = None
        try:
            backbone = createBackBone()
            backbone.readData(preprocess=False)
        except Exception as e:
            logger.error("@BackBonereadData")
            logger.error(e)
            raised = True
            error = e
        finally:
            if error:
                print(error)
            self.assertEqual(raised, False)

    def testDataPipeRuntimeTrain(self):
        raised = False
        error = None
        try:
            backbone = createBackBone()
            backbone.train_model_database_or_runtime(savemodel=False)
        except Exception as e:
            logger.error("@BackBoneRuntimeTrain")
            logger.error(e)
            raised = True
            error = e
        finally:
            if error:
                print(error)
            self.assertEqual(raised, False)

    def testDataPipeRuntimePred(self):
        raised = False
        error = None
        try:
            backbone = createBackBone()
            backbone.predict_database_or_runtime()
        except Exception as e:
            logger.error("@BackBoneRuntimePred")
            logger.error(e)
            raised = True
            error = e
        finally:
            if error:
                print(error)
            self.assertEqual(raised, False)

    def testDataPipeRuntimeTest(self):
        raised = False
        error = None
        try:
            backbone = createBackBone()
            backbone.test_database_or_runtime()
        except Exception as e:
            logger.error("@BackBoneRuntimeTest")
            logger.error(e)
            raised = True
            error = e
        finally:
            if error:
                print(error)
            self.assertEqual(raised, False)

    def test_filetransfer(self):
        raised = False
        try:
            csvToXlsx("./static/dataset/testdatabase-with-names.csv", True)
        except Exception as e:
            logger.error("@fileTransfer")
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def test_task_create_thread(self):
        raised = False
        try:
            t = CreateTrainModelPeriodicallyThread()
            t.start()
            t.join()
        except Exception as e:
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def test_train_periodically(self):
        raised = False
        try:
            backbone = createBackBone()
            train_model_periodically(backbone, False, 50)
        except Exception as e:
            logger.error(e)
            raised = True
        finally:
            self.assertEqual(raised, False)

    def test_predUploadFile(self):
        raised = False
        try:
            predictUploadedFile('temporary', 'test-campaign1.csv')
        except Exception as e:
            logger.error(e)
            raised = True
        self.assertEqual(raised,False)

    def test_customize_config(self):
        config_path = Path.joinpath(Path(__file__).parent, Path("test.json")).resolve()
        customize_config({'test': 0}, config_path)
        with open(config_path, 'r') as fp:
            config = json.load(fp)
        customize_config({'test': 1}, config_path)
        self.assertEqual(config['test'], 0)

    def test_load_config_not_found(self):
        invalid_path = Path.joinpath(Path(__file__).parent, Path("invalid.json")).resolve()
        with self.assertRaises(ConfigNotFoundError, msg="The config invalid.json is not found."):
            load_config(invalid_path)

    def test_load_model_not_found(self):
        invalid_path = Path.joinpath(Path(__file__).parent, Path("invalid.json")).resolve()
        with self.assertRaises(ModelNotFoundError, msg="The model invalid.json is not found."):
            load_model(invalid_path)
'''