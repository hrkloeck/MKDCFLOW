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

NEED TO DO 

generate explanation oon the CASA setup wrst to the singularity thing define HOME !!!
