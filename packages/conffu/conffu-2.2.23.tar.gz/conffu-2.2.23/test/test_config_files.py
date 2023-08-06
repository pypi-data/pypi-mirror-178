import unittest
import inspect
import tempfile
from pathlib import Path
from conffu import Config
# noinspection PyProtectedMember
from conffu._config import argv_to_dict
from subprocess import Popen, DEVNULL
from urllib import request
from urllib.error import URLError
from time import sleep


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self._cfg = Config({
            "_globals": {
                "foo": "bar"
            },
            "baz": "qux {foo}",
            "quux": {
                "corge": "grault {foo}"
            },
            "garply": {
                "waldo": 1,
                "fred": ["plugh", "xyzzy", "{foo}", "{{foo}}"]
            },
            "thud": 42.0
        })

    def tearDown(self):
        self.tmpdir.cleanup()

    @staticmethod
    def _wait_for_server(url):
        retries = 100
        while True:
            try:
                request.urlopen(url)
                return True
            except URLError:
                retries -= 1
                if retries > 0:
                    sleep(.1)
                    continue
                else:
                    return False

    def _check_config(self, cfg):
        context = inspect.stack()[1][3]
        self.assertTrue(cfg.globals)
        self.assertIn('foo', cfg.globals, '_globals foo should have foo ({})'.format(context))
        self.assertEqual('bar', cfg.globals['foo'], '_globals foo should be bar ({})'.format(context))
        self.assertIn('baz', cfg, 'baz should be in config ({})'.format(context))
        self.assertEqual('qux bar', cfg.baz, 'baz should be qux bar after subst ({})'.format(context))
        self.assertIn('quux', cfg, 'quux should be in config ({})'.format(context))
        self.assertIn('corge', cfg.quux, 'quux should be in quux ({})'.format(context))
        self.assertEqual('grault bar', cfg.quux.corge, 'quux.corge should be qux bar after subst ({})'.format(context))
        self.assertIn('garply', cfg, 'garply should be in config ({})'.format(context))
        self.assertIn('waldo', cfg.garply, 'waldo should be in garply ({})'.format(context))
        self.assertEqual(1, cfg.garply.waldo, 'garply.waldo should be 1 (int) ({})'.format(context))
        self.assertIn('fred', cfg.garply, 'fred should be in garply ({})'.format(context))
        self.assertEqual(['plugh', 'xyzzy', 'bar', '{foo}'], cfg.garply.fred,
                         f'garply.fred should be ["plugh", "xyzzy", "bar", "{{foo}}"] (list) ({context})')
        self.assertEqual(42.0, cfg.thud, 'thud should be 42.0 (float) ({})'.format(context))

    def test_json_roundtrip(self):
        self._cfg.save(Path(self.tmpdir.name) / 'config_copy.json')
        cfg = Config.load(Path(self.tmpdir.name) / 'config_copy.json')
        self._check_config(cfg)
        self.assertEqual(cfg, self._cfg, 'JSON loaded from file identical')

        cfg_simple = Config({'a': 1})
        cfg_simple.save(Path(self.tmpdir.name) / 'config_simple.json')
        cfg = Config.load(Path(self.tmpdir.name) / 'config_simple.json')
        self.assertEqual(cfg, cfg_simple, 'simple JSON loaded from file identical')

    def test_xml_roundtrip(self):
        self._cfg.save(Path(self.tmpdir.name) / 'config_copy.xml')
        cfg = Config.load(Path(self.tmpdir.name) / 'config_copy.xml')
        self._check_config(cfg)
        self.assertEqual(cfg, self._cfg, 'XML loaded from file identical')

    def test_pickle_roundtrip(self):
        self._check_config(self._cfg)
        self._cfg.save(Path(self.tmpdir.name) / 'config_copy.pickle')
        cfg = Config.load(Path(self.tmpdir.name) / 'config_copy.pickle')
        self._check_config(cfg)
        self.assertEqual(cfg, self._cfg, 'pickle loaded from file identical')

    def test_from_url_text(self):
        self._cfg.save(Path(self.tmpdir.name) / 'config_copy.json')
        p = None
        try:
            p = Popen(['python', '-m', 'http.server'], cwd=self.tmpdir.name, stderr=DEVNULL, stdout=DEVNULL)
            self.assertTrue(self._wait_for_server('http://localhost:8000'), 'test server online')
            cfg = Config.load('http://localhost:8000/config_copy.json?foo=bar')
            self._check_config(cfg)
            self.assertEqual(cfg, self._cfg, 'json loaded from URL identical')
            cfg = Config.load('http://localhost:8000/config_copy.json?foo=bar', url_header='Cookie=api_key\\=1234')
            self.assertEqual(cfg, self._cfg, 'load not affected by header')
        finally:
            p.terminate()
            p.wait()

    def test_from_url_bin(self):
        self._cfg.save(Path(self.tmpdir.name) / 'config_copy.pickle')
        p = None
        try:
            p = Popen(['python', '-m', 'http.server'], cwd=self.tmpdir.name, stderr=DEVNULL, stdout=DEVNULL)
            self.assertTrue(self._wait_for_server('http://localhost:8000'), 'test server online')
            cfg = Config.load('http://localhost:8000/config_copy.pickle?foo=bar')
            self._check_config(cfg)
            self.assertEqual(cfg, self._cfg)
        finally:
            p.terminate()
            p.wait()

    def test_json_from_argument(self):
        p = Path(self.tmpdir.name) / 'config_copy.json'
        self._cfg.save(p)
        args = argv_to_dict(['script.py', '-cfg', str(p)])
        cfg = Config.load(cli_args=args)
        self.assertEqual(cfg, self._cfg)

    def test_import(self):
        cfgi = Config({'_globals': {'g': 3, 'i': 6}, 'd': 2, 'e': '{g}{h}'})
        pi = Path(self.tmpdir.name) / 'config_import.json'
        cfgi.save(pi)
        cfg = Config({'_globals': {'h': 4, 'i': 5}, 'a': 1, 'b': f'import@{pi}', 'c': f'x@{pi}',
                      'f': '{h}', 'g': '{g}'})
        cfg.resolve_imports()
        self.assertEqual(1, cfg.a, 'import does not affect other values')
        self.assertEqual('4', cfg.f, 'import does not affect other globals')
        self.assertEqual('3', cfg.g, 'import adds new globals, affecting existing keys as well')
        self.assertEqual('34', cfg.b.e, 'globals merged and all available to imported section')

    def test_import_url(self):
        cfg = Config({'_globals': {'x': 2}, 'c': 3})
        cfg.save(Path(self.tmpdir.name) / 'config_copy.json')
        cfg = Config({'a': 1, 'b': 'import@http://localhost:8000/config_copy.json?foo=bar', 'd': '{x}'})
        p = None
        try:
            p = Popen(['python', '-m', 'http.server'], cwd=self.tmpdir.name, stderr=DEVNULL, stdout=DEVNULL)
            self.assertTrue(self._wait_for_server('http://localhost:8000'), 'test server online, test_import_url')
            cfg.resolve_imports()
            self.assertEqual(1, cfg.a, 'import from url does not affect other values')
            self.assertEqual(3, cfg.b.c, 'import from url nested values available')
            self.assertEqual('2', cfg.d, 'import from url globals loaded')
        finally:
            p.terminate()
            p.wait()
