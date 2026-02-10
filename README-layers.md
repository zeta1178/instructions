# Layers

<br>
<div style="background-color: rgb(50, 50, 50);color:yellow">
`ssh -i "DockerKey.pem" ec2-user@ec2-52-91-173-27.compute-1.amazonaws.com

 

 

mkdir -p temp/python && mkdir layers ;

cd layers ;

python3 -m venv . ;

source bin/activate ;

python3 -m pip install --upgrade pip ;

python3 -m pip install papermill ipython jupyter ;

cd lib/python3.7/site-packages ;

cp -R * /home/ec2-user/temp/python/ ;

deactivate ;

cd /home/ec2-user/temp ;

zip -r layer.zip . ;

 

exit

 

sftp -i "DockerKey.pem" ec2-user@ec2-52-91-173-27.compute-1.amazonaws.com

 

get /home/ec2-user/temp/layer.zip /Users/cruzaws/Documents/layers/layer.zip`
</div>
<br>

# The Docker Method

Open a new folder add requirements.txt (with package(s))

<br>
<div style="background-color: rgb(50, 50, 50);color:yellow">
docker run --rm -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
</div>
<br>

# Docker Method Part 2.5

Open a folder add requirements.txt (with package(s)) 

<br>
<div style="background-color: rgb(50, 50, 50);color:yellow">
docker run --entrypoint="/bin/bash" --rm -v "$PWD":/var/task "amazon/aws-lambda-python:3.12" -c "pip install -r requirements.txt -t python/lib/python3.12/site-packages/;exit"
</div>
<br>

<br>
<div style="background-color: rgb(50, 50, 50);color:yellow">
zip -9 -r mylayer.zip python
</div>
<br>
