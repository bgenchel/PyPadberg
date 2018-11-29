import librosa as lb
import numpy as np
from pygame import *
import pygame
import soundfile

one, sr = lb.load('audio/1.wav') ## loads audio file
two, sr = lb.load('audio/2.wav') ## loads audio file
three, sr = lb.load('audio/3.wav') ## loads audio file

soundtypes =  {
    "one": one,
    "two": two,
    "three": three
}


def synth(frequencies, durations, soundtype, canon):

    pitches = lb.core.hz_to_midi(frequencies) % 60

    durationMod = [(x % 32)/8 + 1 for x in durations]

    canonStart = sum(durationMod[0:2])

    new_sample = soundtypes[soundtype]
    new_phrase = np.empty((0))

    for p, l in zip(pitches, durationMod):
        new_sample_shift = lb.effects.pitch_shift(new_sample, sr, n_steps=p)
        new_sample_shift = lb.effects.time_stretch(new_sample_shift, l)
        new_phrase = np.append(new_phrase, new_sample_shift)

    new_phrase_two = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0)))
    new_phrase_three = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0*2)))
    new_phrase_four = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0*3)))

    lb.output.write_wav('temp.wav', new_phrase.astype(np.float16), sr, norm=False) #
    lb.output.write_wav('temp2.wav', new_phrase_two.astype(np.float16), sr, norm=False)
    lb.output.write_wav('temp3.wav', new_phrase_three.astype(np.float16), sr, norm=False)
    lb.output.write_wav('temp4.wav', new_phrase_four.astype(np.float16), sr, norm=False)

    pygame.init()

    #brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
    mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()

    # data, samplerate = soundfile.read('temp.wav')
    soundfile.write('new.wav', new_phrase, sr, subtype='PCM_16')
    soundfile.write('new2.wav', new_phrase_two, sr, subtype='PCM_16')
    soundfile.write('new3.wav', new_phrase_three, sr, subtype='PCM_16')
    soundfile.write('new4.wav', new_phrase_four, sr, subtype='PCM_16')

    sounds = [mixer.Sound('new.wav'),
              mixer.Sound('new2.wav'),
              mixer.Sound('new3.wav'),
              mixer.Sound('new4.wav')]

    mixer.set_num_channels(canon)
    for i in range(canon):
        mixer.Channel(i).play(sounds[i])

    while mixer.Channel(canon-1).get_busy():
        time.Clock().tick(10)

