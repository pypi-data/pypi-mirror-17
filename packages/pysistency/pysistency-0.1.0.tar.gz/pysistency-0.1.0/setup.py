import os
import re
import sys
import codecs
try:
    sys.argv.remove('--cythonize')
except (IndexError, ValueError):
    cythonize = False
else:
    cythonize = True

from setuptools import setup, find_packages

# guard against rerunning setup.py when bootstrapping __main__
if __name__ == '__main__':
    repo_base = os.path.abspath(os.path.dirname(__file__))
    package_name = 'pysistency'
    source_base = os.path.join(repo_base, package_name)

    extensions = []
    cmdclass = {}
    # Cython support
    if cythonize:
        try:
            import Cython.Distutils
            from distutils.extension import Extension
        except Exception as err:
            raise SystemExit('Cannot cythonize: %s' % err)
        for dirpath, dirnames, filenames in os.walk(source_base):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if name == '__init__':
                    continue
                if ext == '.py':
                    rel_path = os.path.relpath(os.path.join(dirpath, filename), repo_base)
                    mod_path = os.path.splitext(rel_path)[0].replace(os.sep, '.')
                    print(mod_path, rel_path)
                    extensions.append(
                        Extension(name=mod_path, sources=[os.path.join(repo_base, rel_path)])
                    )
        if extensions:
            cmdclass = {'build_ext': Cython.Distutils.build_ext}
        print(extensions)
        #sys.exit(1)

    # grab meta without import package
    sys.path.insert(0, source_base)
    import meta as pysistency_meta

    install_requires = []

    # use readme for long descritpion, strip sphinx codes
    with codecs.open(os.path.join(repo_base, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    for directive_re, replacement_re in [
        (':py:\S*?:`~(.*?)`', '`\g<1>`'),
        (':py:\S*?:', ''),
        (':envvar:', ''),
    ]:
        long_description = re.sub(directive_re, replacement_re, long_description)

    setup(
        name=package_name,

        # meta data
        version=pysistency_meta.__version__,

        description='Python containers with persistency',
        long_description=long_description,
        url='https://github.com/maxfischer2781/pysistency',

        author='Max Fischer',
        author_email='maxfischer2781@gmail.com',

        license='Apache V2.0',
        platforms=['Operating System :: OS Independent'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            # 'Programming Language :: Python :: 2.6',
            # 'Programming Language :: Python :: 2.7',
            # 'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            # TODO: confirm others
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities'
        ],
        keywords='container persistent',

        # content
        packages=find_packages(exclude=('pysistency_*', 'dev_tools')),
        install_requires=install_requires,
        extras_require={
        },
        cmdclass=cmdclass,
        ext_modules=extensions,
        # unit tests
        test_suite='pysistency_unittests',
    )
