import setuptools

setuptools.setup(
     name='plex-aac-passthrough',  
     version='0.1',
     scripts=['plex-aac-passthrough'] ,
     author="Alex de Chaves",
     author_email="dechavesalex@gmail.com",
     description="A AAC and AC3 transcode utility package",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )