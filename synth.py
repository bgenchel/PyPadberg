import librosa as lb
import numpy as np

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
    new_phrase = []
    new_phrase_two =[]
    new_phrase_three=[]
    new_phrase_four=[]
    new_sample_shift = []

    for p, l in zip(pitches, durationMod):
        new_sample_shift = lb.effects.pitch_shift(new_sample, sr, n_steps=p)
        new_sample_shift = lb.effects.time_stretch(new_sample_shift, l)
        new_phrase = np.append(new_phrase, new_sample_shift)

    if canon == 2:
        new_phrase_two = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0)))

    if canon == 3:
        new_phrase_three = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0*2)))

    if canon == 4:
        new_phrase_four = np.insert(new_phrase,0,np.zeros(int(canonStart*11025.0*3)))

    lb.output.write_wav('temp.wav', new_phrase, sr, norm=False) #
    lb.output.write_wav('temp2.wav', new_phrase_two, sr, norm=False)
    lb.output.write_wav('temp3.wav', new_phrase_two, sr, norm=False)
    lb.output.write_wav('temp4.wav', new_phrase_two, sr, norm=False)
