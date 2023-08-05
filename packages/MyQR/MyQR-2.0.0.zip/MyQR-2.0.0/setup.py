# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'MyQR',
    version = '2.0.0',
    keywords = ('qr', 'qrcode', 'qr code', 'artistic', 'animated', 'gif'),
    description = 'Generater for amazing qr codes. Including Common, Artistic and Animated qr codes.',
    long_description = '''
        Overview
        ===============
        It can generate common qr-code, artistic qr-code (black & white or colorized), animated qr-code (black & white or colorized).

        Usage
        ===============
        terminal:
        
        myqr words
             [-h]
             [-v {1,2,3,...,40}]
             [-l {L, M, Q, H}]
             [-p image_filename]
             [-c]
             [-con contrast_value]
             [-bri brightness_value]
             [-n output_filename]
             [-d output_directory]

             
        import:
         
        from MyQR import myqr
        myqr.run(
            words,
            version=1,
            level='H',
            picture=None,
            colorized=False,
            contrast=1.0,
            brightness=1.0,
            save_name=None,
            save_dir=os.getcwd()
            )
             
             
        More
        ===============
        Please visit 'Home Page' blow for examples and details.
        
        Update
        ===============
        version 2.0.0 - Recoded to be importable.
        
        
        
        
    ''',

    author = 'sylnsfar',
    author_email = 'sylnsfar@gmail.com',
    url = 'https://github.com/sylnsfar/qrcode',
    download_url = 'https://github.com/sylnsfar/qrcode',

    install_requires = [
        'imageio >= 1.5',
        'numpy >= 1.11.1',
        'Pillow>=3.3.1'
    ],
    packages = ['MyQR', 'MyQR.mylibs'],
    
    license = 'GPLv3',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    entry_points = {
        'console_scripts': [
            'myqr = MyQR.terminal:main',
        ],
    }
)
