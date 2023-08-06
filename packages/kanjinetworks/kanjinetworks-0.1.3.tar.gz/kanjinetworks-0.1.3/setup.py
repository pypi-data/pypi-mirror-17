from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

def requires():
    with open('requirements.txt') as f:
        return f.read().split("\n")

config = {
    'name': 'kanjinetworks',
    'version': '0.1.3',
    'description': 'Kanji Networks interface',
    'long_description': readme(),
    'license': 'MIT',
    'author': 'Arnaud Coomans',
    'author_email': 'arnaud.coomans@gmail.com',
    'url': 'https://github.com/acoomans/kanjinetworks',
    'download_url': 'https://github.com/acoomans/kanjinetworks/archive/master.zip',
    'install_requires': requires(),
    'packages': ['kanjinetworks', 'kanjinetworks.extract', 'kanjinetworks.export'],
    'scripts': ['scripts/kn_to_ja.py'],
    'data_files' : [('data', ['data/etymologicaldictionaryofhanchinesecharacters-160816005400.pdf'])],
    'zip_safe': False,
    'include_package_data': True,
    'test_suite': 'kanjinetworks',
}

setup(**config)