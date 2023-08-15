Step 1: Create the environment
Creating / setting a conda environment for cdk.

In this example we will call the conda env workshop--cdk .
I like to add the --cdk suffix to all of my cdk conda envs.

This is often to distinguish them from the project logic itself which may be called workshop.

```
$ conda create --yes \
    --name 'workshop--cdk' \
    --channel 'conda-forge' \
    nodejs=="20.1.0" \
    pip python=3.11
```

```
$ pip freeze > requirements.txt
pip install -r requirements.txt
```

Step 2: Add in the activation script
Activate the environment and install aws-cdk.

```conda activate workshop--cdk```

Let’s ensure that the node environment variables are set
when we activate the cdk project.

We can do that by adding in a quick shell script into the conda environment’s activate.d directory.

Firstly let’s create the activate.d with the following.

```$ mkdir -p "${CONDA_PREFIX}/etc/conda/activate.d"```

Now let’s add in the activation script into that directory under the name node.sh with the following contents:
Navigate to the following as an example:

```/Users/michaelcruz/opt/miniconda3/envs/image-ai/etc/conda/activate.d```
Then create a node.sh file in that directory

```
#!/usr/bin/env bash

# Set both NPM_CONFIG_PREFIX and NODE_PATH env vars
export NPM_CONFIG_PREFIX="${CONDA_PREFIX}"
export NODE_PATH="${NPM_CONFIG_PREFIX}/node_modules:${NODE_PATH}"

# Create the node modules directory
mkdir -p "${NPM_CONFIG_PREFIX}/node_modules"

# Add in the bin path for each of the node modules that we install
for bin_path in `find "${NPM_CONFIG_PREFIX}/node_modules" -mindepth 2 -maxdepth 2 -name "bin"`; do
    export PATH="${bin_path}:${PATH}"
done
```

Step 3: Re-activate the environment
This ensures that all of our environment scripts are activated correctly.

```$ conda deactivate```

```$ conda activate workshop--cdk```

Step 4: Install aws-cdk
For this app, we will install version 2.
We need to set the prefix for the first npm installation into this directory.

```$ npm install aws-cdk@^2 --prefix "${NPM_CONFIG_PREFIX}"```

Deactivate and activate the environment

```$ conda deactivate```
```$ conda activate workshop--cdk```

Step 5: Test out your cdk version
We can see that the cdk is the right cdk (inside the conda prefix) and is the version we expect.

```
$ which cdk
/home/alexiswl/miniforge3/envs/cdk--cdk-workshop-v2/node_modules/aws-cdk/bin/cdk
$ cdk --version
2.1.0 (build f4f18b1)
```

Step 6: Create your cdk app
Change directory to where you wish to initialise your app and then run cdk init .

```
$ cd /path/to/cdk/dir
$ cdk init sample-app --language python
```

Step 7 (optional): Install project requirements into conda
If we set the project as a python project in the previous step, we need to install the requirements into our conda env. Typescript projects can skip this step.

```pip install -r requirements.txt```

And we’re done!!
