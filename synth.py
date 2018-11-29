import librosa as lb
import numpy as np
import os
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
    pygame.init()
    #brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
    mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()

    pitches = lb.core.hz_to_midi(frequencies) % 60

    durationMod = [(x % 32)/8 + 1 for x in durations]

    canonStart = sum(durationMod[0:2])

    sample = soundtypes[soundtype]
    phrase = np.empty((0))

    for p, l in zip(pitches, durationMod):
        sample_shift = lb.effects.pitch_shift(sample, sr, n_steps=p)
        sample_shift = lb.effects.time_stretch(sample_shift, l)
        phrase = np.append(phrase, sample_shift)

    phrases = [phrase]
    for i in range(1, 4):
        phrases.append(np.insert(phrase, 0, np.zeros(int(canonStart * 11025.0 * i))))

    sounds = []
    for i, phrase in enumerate(phrases):
        # lb.output.write_wav('temp%i.wav' % (i + 1), phrase.astype(np.float16), sr, norm=False)
        fname = 'temp_%i.wav' % (i + 1)
        soundfile.write(fname, phrase, sr, subtype="PCM_16")
        sounds.append((fname, mixer.Sound(fname)))

    mixer.set_num_channels(canon)
    for i in range(canon):
        mixer.Channel(i).play(sounds[i][1])

    # clean up the temp files
    for fname, _ in sounds:
        os.remove(fname)
