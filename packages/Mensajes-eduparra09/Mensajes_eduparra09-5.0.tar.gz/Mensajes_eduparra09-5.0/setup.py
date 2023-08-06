from setuptools import setup, find_packages

#Manera de instalar tu codigo y reutilizar en la maquina

setup( # Parametros para llamar a la funcion setup
    name='Mensajes_eduparra09',#Nombre del paquete a guardar
    version='5.0',
    description='Un paquete para saludar y despedir', # Descripcion del paquete a guardar
    long_description= open('README.md').read(),
    long_description_content_type= 'text/markdown',
    author='Eduar Parra Cancines', #Nombre del autor del paquete 
    author_email='eduarparra30@gmail.com',
    url='https://github.com/Edwiou9876/Edwiou9876', #Coreo del autor 
    license_files= ['LICENSE'],
    packages= find_packages(), # Automatiza la escripcion de cada paquete
    scripts=['test_1.py'],# Nombre del script a resolver
    test_suite = 'test',
    install_requires = [paquete.strip() for paquete in open("Requerir.txt").readlines()], #Para saber donde se depende de un modulo externo
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ]

) # Para instalar se ejectuta desde la terminal se llama al script setup.py se le pasa el parametro sdist 
# Se creara una carpeta comprimida con instrucciones que luego tendras que llamar aplicando un espacion de la siguiente manera
#cd dist te llamara la ubicacion de la carpeta 
#Luego indicas aplicando un espacio pip install nombre-1.0.0.tar.gz y se instalara

#Para actualizar el paquete debes usar el setup.py llamar de nuevo y usar el sdist


