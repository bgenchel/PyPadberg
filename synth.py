import librosa as lb
import numpy as np
import pygame as pygame
pygame.init()

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

    durationMod = [x % 8 for x in durations]

    canonStart = sum(durationMod[0:2])

    new_sample = soundtypes[soundtype]
    new_phrase = []
    new_sample_shift = []

    for p, l in zip(pitches, durationMod):
        new_sample_shift = lb.effects.pitch_shift(new_sample, sr, n_steps=p)
        new_sample_shift = lb.effects.time_stretch(new_sample_shift, l)
        new_phrase = np.append(new_phrase, new_sample_shift)

    lb.output.write_wav('temp.wav', new_phrase, sr, norm=False) #
    pygame.mixer.music.load("temp.wav")
    pygame.mixer.music.play()

    if canon >= 2:
        pygame.time.Clock().tick(canonStart)
        pygame.mixer.music.play()

    if canon >= 3:
        pygame.time.Clock().tick(canonStart*2)
        pygame.mixer.music.play()

    if canon >= 4:
        pygame.time.Clock().tick(canonStart*3)
        pygame.mixer.music.play()

    pygame.event.wait()
