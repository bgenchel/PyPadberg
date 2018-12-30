import librosa as lb
import numpy as np
import os
import os.path as op
from pygame import *
import pygame
import soundfile

this_dir = op.dirname(op.abspath(__file__))
one, sr1 = lb.load(op.join(this_dir, 'assets', 'audio', '1.wav')) ## loads audio file
two, sr2 = lb.load(op.join(this_dir, 'assets', 'audio', '2.wav')) ## loads audio file
three, sr3 = lb.load(op.join(this_dir, 'assets', 'audio', '3.wav')) ## loads audio file

SOUNDTYPES =  {
    "one": (one, sr1),
    "two": (two, sr2),
    "three": (three, sr3)
}

INTERVALS = [0.0, -8.0, -12.0, -20.0]

class Synth:
    def __init__(self):
        # for saving if desired
        self.voices = None
        self.pitches = None
        self.dursMod = None
        self.sample_rate = None

    def initialize(self, freqs, durs):
        self.pitches = lb.core.hz_to_midi(freqs) % 60
        self.dursMod = [(x % 32)/8 + 1 for x in durs]

    def _make_voices(self, soundtype):
        sample, sample_rate = SOUNDTYPES[soundtype] # track the sampling rate for saving later
        voices = [np.empty((0)), np.empty((0)), np.empty((0)), np.empty((0))]
        for i in range(0, 4):
            for p, l in zip(self.pitches, self.dursMod):
                sample_shift = lb.effects.pitch_shift(sample, sample_rate, n_steps=p + INTERVALS[i])
                sample_shift = lb.effects.time_stretch(sample_shift, l)
                voices[i] = np.append(voices[i], sample_shift)

        canonStart = sum(self.dursMod[0:2])
        for i in range(1, 4):
            voices[i] = np.insert(voices[i], 0, np.zeros(int(canonStart * 11025.0 * i)))

        return voices, sample_rate

    def play(self, soundtype, num_voices):
        pygame.init()
        #brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
        mixer.pre_init(44100, 16, 2, 4096)
        mixer.init()

        voices, sample_rate = self._make_voices(soundtype)

        sounds = []
        for i in range(num_voices):
            fname = 'temp_%i.wav' % (i + 1)
            soundfile.write(fname, voices[i], sample_rate, subtype="PCM_16")
            sounds.append((fname, mixer.Sound(fname)))

        mixer.set_num_channels(num_voices)
        for i in range(num_voices):
            mixer.Channel(i).play(sounds[i][1])

        # clean up the temp files
        # TODO: there is a problem if a person happens to name their file the same thing as the temp files
        for fname, _ in sounds:
            os.remove(fname)

    def save(self, soundtype, title=None):
        voices, sample_rate = self._make_voices(soundtype)
        if title:
            soundfile.write(title + "1.wav", voices[0], sample_rate, subtype="PCM_16")
            soundfile.write(title + "2.wav", voices[1], sample_rate, subtype="PCM_16")
            soundfile.write(title + "3.wav", voices[2], sample_rate, subtype="PCM_16")
            soundfile.write(title + "4.wav", voices[3], sample_rate, subtype="PCM_16")
        else:
            soundfile.write("output.wav", voices[0], sample_rate, subtype="PCM_16")
            soundfile.write("output.wav", voices[1], sample_rate, subtype="PCM_16")
            soundfile.write("output.wav", voices[2], sample_rate, subtype="PCM_16")
            soundfile.write("output.wav", voices[3], sample_rate, subtype="PCM_16")
