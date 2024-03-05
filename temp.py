import json 
import requests
import requests
import warnings
import os
import boto3
from botocore.exceptions import ClientError
import base64
import subprocess
import logging
import time
from OpenSSL import crypto
os.environ["GIT_PYTHON_REFRESH"]="quiet"
import git
from git import Repo, Actor
import sys 
import shutil
import yaml 
from datetime import datetime 
import os.path 

logger=logging.getLogger()
logger.setLevel(logging.INFO)

sess = boto3.Session(region_name="us-east-1")
region = 'us-east-1'
acmClient = sess.client('acm')
s3Client = sess.client('s3')
s3bucket = 'my-bucket'
ssmClient = sess.client('ssm')
smClient = sess.client('secretsmanager')

def run_command(command):
    try:
        #logger.info("Running shell command: \"{}\"".format(command))
        result = subprocess.run(command, stdout=subprocess.PIPE, shell=True);
        logger.info("Command Output:\n---\n{}\n---".format(result.stdout.decode('UTF-8')))
    except Exception as e:
        logger.error("Exception: {}".format(e))
        return False
    return True

def cert_gen(
    file_path,
    emailAddress="michael.cruz@amtrak.com",
    commonName="michaelcruz.amtrak.com",
    countryName="US",
    localityName="Washington",
    stateOrProvinceName="District of Columbia",
    organizationName="National Railroad Passenger Corporation",
    organizationUnitName="NRPC",
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=2*60*60 
    ):
    #can look at generated file using openssl:
    #openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    KEY_FILE = f"/tmp/certfolder/{file_path}/private.key"
    CERT_FILE= f"/tmp/certfolder/{file_path}/selfsigned.crt"
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
    return file_path

def lambda_handler(event, context):

    secret_name_appuser = "/amtrak/aws/bitbucketappuser"
    secret_name_apppass = "/amtrak/aws/bitbucketapppass"

    try:
        get_secret_value_response_appuser = smClient.get_secret_value(
            SecretId=secret_name_appuser
        )
        get_secret_value_response_apppass = smClient.get_secret_value(
            SecretId=secret_name_apppass
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_appuser = json.loads(get_secret_value_response_appuser['SecretString'])
    secret_apppass = json.loads(get_secret_value_response_apppass['SecretString'])

    git_target = (ssmClient.get_parameter(Name='/git/repository-ssh')['Parameter']['Value'])
    git_url_target = f"https://{secret_appuser['AppUser']}:{secret_apppass['AppPass']}@{git_target}"

    empty_repo = git.Repo.init('/tmp/certfolder')
    origin = empty_repo.create_remote('origin', url=git_url_target)
    assert origin.exists()
    assert origin == empty_repo.remotes.origin == empty_repo.remotes['origin']
    origin.fetch()

    empty_repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.rename('new_origin')
    origin.pull()

    if os.path.isdir(f"/tmp/certfolder/{event['test']}"):
        shutil.rmtree(f"/tmp/certfolder/{event['test']}")
        
    # create new single directory
    path = f"/tmp/certfolder/{event['test']}"
    os.mkdir(path)
    
    # # create new single file
    # details_dict={"Details" : {
    #     "Full_Name" : "Mike Cruz",
    #     "Name": cert_gen(event['test'])
    #     }
    # }
    # f = open(f"/tmp/certfolder/{event['test']}/input.yaml", "w+")
    # yaml.dump(details_dict, f, allow_unicode=True)
    
    # create timestamp
    now = datetime.now()
    date_time = now.strftime("%m%d%Y%H%M%S")
    commit_message= f"cert-added-{date_time}"

    # git add
    empty_repo.git.add('-A')

    #git commit
    author = Actor("An author", "michael.cruz@amtrak.com")
    empty_repo.index.commit(commit_message, author=author)
    
    #git push 
    empty_repo.remote('new_origin').push(force=True,refspec='{}:{}'.format('main', 'main'))
