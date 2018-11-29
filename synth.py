import librosa as lb
import numpy as np
<<<<<<< HEAD
=======
import subprocess
import pygame
from pydub import AudioSegment
from pydub.playback import play

pygame.init()
pygame.mixer.init()
>>>>>>> ba6d42907d9c4682b31f47c5dcb041243939b7bd

one, sr = lb.load('audio/1.wav') ## loads audio file
two, sr = lb.load('audio/2.wav') ## loads audio file
three, sr = lb.load('audio/3.wav') ## loads audio file

soundtypes =  {
    "one": one,
    "two": two,
    "three": three
}

#Frequencies in HZ, durations in ms, soundtype is one,two,three
def synth(frequencies, durations, soundtype, canon):

    pitches = lb.core.hz_to_midi(frequencies) % 60

    durationMod = [(x % 32)/8 + 1 for x in durations]

    canonStart = sum(durationMod[0:2])

    new_sample = soundtypes[soundtype]
    new_phrase = []
    new_phrase_two =[]
    new_phrase_three=[]
    new_phrase_four=[]
    new_sample_shift = []

    for p, l in zip(pitches, durationMod):
        new_sample_shift = lb.effects.pitch_shift(new_sample, sr, n_steps=p)
        new_sample_shift = lb.effects.time_stretch(new_sample_shift, l)
        new_phrase = np.append(new_phrase, new_sample_shift)

<<<<<<< HEAD
    if canon == 2:
        new_phrase_two = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0)))

    if canon == 3:
        new_phrase_three = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0*2)))

    if canon == 4:
        new_phrase_four = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0*3)))
=======
    lb.output.write_wav('temp.wav', new_phrase, sr, norm=False) #
    subprocess.call(['play', 'temp.wav'], stdout=open("output.txt"))
    # subprocess.Popen(['play', 'temp.wav']) 
    # sound = AudioSegment.from_file("temp.wav", format="wav")
    # play(sound)
    # pygame.mixer.music.load("temp.wav")
    # pygame.mixer.music.play(0)

    if canon >= 2:
        pygame.time.Clock().tick(canonStart)
        pygame.mixer.music.play(0)

    if canon >= 3:
        pygame.time.Clock().tick(canonStart*2)
        pygame.mixer.music.play(0)

    if canon >= 4:
        pygame.time.Clock().tick(canonStart*3)
        pygame.mixer.music.play(0)
>>>>>>> ba6d42907d9c4682b31f47c5dcb041243939b7bd

    lb.output.write_wav('temp.wav', new_phrase, sr, norm=False) #
    lb.output.write_wav('temp2.wav', new_phrase_two, sr, norm=False)
    lb.output.write_wav('temp3.wav', new_phrase_two, sr, norm=False)
    lb.output.write_wav('temp4.wav', new_phrase_two, sr, norm=False)
