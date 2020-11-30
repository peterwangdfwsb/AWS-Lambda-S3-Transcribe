import json
import boto3
import parselmouth
import os
from subprocess import call

def lambda_handler(event, context):
    '''Draw intonation from wav files in AWS S3, and deploy the model on AWS Lambda'''
    
    #Connect to the AWS S3
    bucket = 'lambda-efs-ml'
    key = 'audio1.wav'
    s3 = boto3.client('s3')
    
    #Download the wav file in temporary storage on AWS Lambda
    s3.download_file(bucket, key, '/tmp/audio1.wav')
    
    #Process the wav file by using python praat package
    source='/tmp/audio1.wav'
    snd = parselmouth.Sound(source)
    pitch = snd.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    
    #Save the array in json format
    audio_pitch={'pitch':list(pitch_values)}
    
    #Delete the wav file in temporary storage on AWS Lambda
    call('rm -rf /tmp/*', shell=True)
    
    return audio_pitch
