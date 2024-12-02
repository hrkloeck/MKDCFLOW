# Generate the container

## Generate the Singularity image


- make a directory 

```
mkdir my_CAL_TEST
cd my_CAL_TEST
```

- get the depository, either via git clone or download the source:

```
git clone https://github.com/hrkloeck/MKDCFLOW.git
```

- generate the singularity image

```
cd MKDCFLOW/singularity
```

```
singularity build --fakeroot MKDCFLOW.simg singularity.meerkat.recipe_082024
```

The next steps are needed to setup a pseudo home directory for CASA, python, etc.

```
cd ../../
mkdir -p ${USER}/.casa/data

```

Get some additional packages outside the singularity container 
```
git clone https://github.com/hrkloeck/DASKMSWERKZEUGKASTEN.git
git clone https://github.com/hrkloeck/2GC.git
git clone https://github.com/JonahDW/Image-processing.git
```

Ok lets go and start.
