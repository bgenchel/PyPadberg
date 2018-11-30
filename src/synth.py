import librosa as lb
import numpy as np
import os
import os.path as op
from pygame import *
import pygame
import soundfile

this_dir = op.dirname(op.abspath(__file__))
one, sr = lb.load(op.join(this_dir, 'assets', 'audio', '1.wav')) ## loads audio file
two, sr = lb.load(op.join(this_dir, 'assets', 'audio', '2.wav')) ## loads audio file
three, sr = lb.load(op.join(this_dir, 'assets', 'audio', '3.wav')) ## loads audio file

soundtypes =  {
    "one": one,
    "two": two,
    "three": three
}

intervals = [0.0, -8.0, -12.0, -20.0]

def synth(frequencies, durations, soundtype, canon):
    pygame.init()
    #brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
    mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()

    pitches = lb.core.hz_to_midi(frequencies) % 60

    durationMod = [(x % 32)/8 + 1 for x in durations]

    canonStart = sum(durationMod[0:2])

    sample = soundtypes[soundtype]
    phrase = [np.empty((0)), np.empty((0)), np.empty((0)), np.empty((0))]

    for i in range(0, 4):
        for p, l in zip(pitches, durationMod):
            sample_shift = lb.effects.pitch_shift(sample, sr, n_steps=p+intervals[i])
            sample_shift = lb.effects.time_stretch(sample_shift, l)
            phrase[i] = np.append(phrase[i], sample_shift)

    for i in range(1, 4):
        phrase[i] = np.insert(phrase[i], 0, np.zeros(int(canonStart * 11025.0 * i)))


    sounds = []
    for i in range(0,4):
        # lb.output.write_wav('temp%i.wav' % (i + 1), phrase.astype(np.float16), sr, norm=False)
        fname = 'temp_%i.wav' % (i + 1)
        soundfile.write(fname, phrase[i], sr, subtype="PCM_16")
        sounds.append((fname, mixer.Sound(fname)))

    mixer.set_num_channels(canon)
    for i in range(canon):
        mixer.Channel(i).play(sounds[i][1])

    # clean up the temp files
    for fname, _ in sounds:
        os.remove(fname)
