from mock import patch
from django.test import TestCase
from dbbackup.storage import get_storage, Storage
from dbbackup.tests.utils import HANDLED_FILES, FakeStorage
from dbbackup import utils

DEFAULT_STORAGE_PATH = 'django.core.files.storage.FileSystemStorage'
STORAGE_OPTIONS = {'location': '/tmp'}


class Get_StorageTest(TestCase):
    @patch('dbbackup.settings.STORAGE', DEFAULT_STORAGE_PATH)
    @patch('dbbackup.settings.STORAGE_OPTIONS', STORAGE_OPTIONS)
    def test_func(self, *args):
        self.assertIsInstance(get_storage(), Storage)

    def test_set_path(self):
        fake_storage_path = 'dbbackup.tests.utils.FakeStorage'
        storage = get_storage(fake_storage_path)
        self.assertIsInstance(storage.storage, FakeStorage)

    @patch('dbbackup.settings.STORAGE', DEFAULT_STORAGE_PATH)
    def test_set_options(self, *args):
        storage = get_storage(options=STORAGE_OPTIONS)
        self.assertEqual(storage.storage.__module__, 'django.core.files.storage')


class StorageTest(TestCase):
    def setUp(self):
        self.storageCls = Storage
        self.storageCls.name = 'foo'
        self.storage = Storage()


class StorageListBackupsTest(TestCase):
    def setUp(self):
        HANDLED_FILES.clean()
        self.storage = get_storage()
        HANDLED_FILES['written_files'] += [
            (utils.filename_generate(ext, 'foo'), None) for ext in
            ('db', 'db.gz', 'db.gpg', 'db.gz.gpg')
        ]
        HANDLED_FILES['written_files'] += [
            (utils.filename_generate(ext, 'foo', None, 'media'), None) for ext in
            ('tar', 'tar.gz', 'tar.gpg', 'tar.gz.gpg')
        ]
        HANDLED_FILES['written_files'] += [
            ('file_without_date', None)
        ]

    def test_nofilter(self):
        files = self.storage.list_backups()
        # self.assertEqual(len(HANDLED_FILES['written_files']), len(files))
        for file in files:
            self.assertNotEqual('file_without_date', file)

    def test_encrypted(self):
        files = self.storage.list_backups(encrypted=True)
        # self.assertEqual(8, len(files))
        for file in files:
            self.assertIn('.gpg', file)

    def test_compressed(self):
        files = self.storage.list_backups(compressed=True)
        # self.assertEqual(8, len(files))
        for file in files:
            self.assertIn('.gz', file)

    def test_dbbackup(self):
        files = self.storage.list_backups(content_type='db')
        # self.assertEqual(8, len(files))
        for file in files:
            self.assertIn('.db', file)

    def test_database(self):
        files = self.storage.list_backups(database='foo')
        # self.assertEqual(9, len(files))
        for file in files:
            self.assertIn('foo', file)

    def test_mediabackup(self):
        files = self.storage.list_backups(content_type='media')
        # self.assertEqual(8, len(files))
        for file in files:
            self.assertIn('.tar', file)


class StorageGetLatestTest(TestCase):
    def setUp(self):
        self.storage = get_storage()
        HANDLED_FILES['written_files'] = [(f, None) for f in [
            '2015-02-06-042810.bak',
            '2015-02-07-042810.bak',
            '2015-02-08-042810.bak',
        ]]

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_func(self):
        filename = self.storage.get_latest_backup()
        self.assertEqual(filename, '2015-02-08-042810.bak')


class StorageGetMostRecentTest(TestCase):
    def setUp(self):
        self.storage = get_storage()
        HANDLED_FILES['written_files'] = [(f, None) for f in [
            '2015-02-06-042810.bak',
            '2015-02-07-042810.bak',
            '2015-02-08-042810.bak',
        ]]

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_func(self):
        filename = self.storage.get_older_backup()
        self.assertEqual(filename, '2015-02-06-042810.bak')


class StorageCleanOldBackupsTest(TestCase):
    def setUp(self):
        self.storage = get_storage()
        HANDLED_FILES.clean()
        HANDLED_FILES['written_files'] = [(f, None) for f in [
            '2015-02-06-042810.bak',
            '2015-02-07-042810.bak',
            '2015-02-08-042810.bak',
        ]]

    def test_func(self):
        self.storage.clean_old_backups(keep_number=1)
        self.assertEqual(2, len(HANDLED_FILES['deleted_files']))
