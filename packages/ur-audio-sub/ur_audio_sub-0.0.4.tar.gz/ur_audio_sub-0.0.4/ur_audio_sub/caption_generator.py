# I. Transcribe Youtube Videos
import os
import pandas as pd
import pytube
from pytube import YouTube
import whisper
from ur_gadget import *

# Generate subtitle for a youtube video
def ytSub(link, model='medium', language='', translate=False, lmt=LMT, basepath=ROOT_DIR):
  """
  Generate caption for any specific Youtube video.
  Args:
      link (:obj:`str`, required): Input the target Youtube video link "https://www.youtube.com/watch?v=21j_OCNLuYg&t=88s&ab_channel=TEDxTalks"
  """
  path = newest_file(basepath)
  subGen_path(path)
  return path + '.txt'


# Generate subtitle for a local file
def subGen_path(file_path, model='medium', language='', translate=False):
  """
  Input audio file path to generate the text caption 
  Args:
      file_path (:obj:`str`, required): Eg: "/content/sample_recording.mp3"
      model (:obj:`str`, optional): choose 1 of 3 options: 'base', 'medium', 'large'. Default value = 'medium'
      language (:obj:`str`, optional): Target language of the audio file to be generated caption. Auto detects language by default.
      translate (:obj:`str`, optional): Translate caption to English. No translation by default.
  """
  if language == '':
    if translate == False:
      os.system('whisper "{}" --model {}'.format(file_path, model))
    else:
      os.system('whisper "{}" --model {} --task translate'.format(file_path, model))
  else:
    if translate == False:
      os.system('whisper "{}" --model {} --language {}'.format(file_path, model, language))
    else:
      os.system('whisper "{}" --model {} --language {} --task translate'.format(file_path, model, language))

def subGen_order(model='medium', lmt=LMT, basepath=ROOT_DIR):
  """Input a number corresponding to the audio file to the prompt to start generating a caption"""
  files_list = file_ls()
  print(pd.Series(files_list))
  no_input = input('Input the number corresponding to the target file: ')
  file = lmt.join([basepath, files_list[int(no_input)]])
  print('Generating caption for: ' + files_list[int(no_input)])
  os.system('whisper "{}" --model {}'.format(file, model))

def get_yt (link, lmt=LMT, basepath=ROOT_DIR):
  """Download youtube video from its link"""
  yt = YouTube(link) # get Youtube video info
  yt.streams.filter(only_audio=True)[0]\
          .download(output_path='') # save audio file to current directory
  file_path = lmt.join([basepath, video_title(link)]) + '.mp4'
  return file_path



