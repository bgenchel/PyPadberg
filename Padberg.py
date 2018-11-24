from mido import Message, MidiFile, MidiTrack
from audiolazy import lazy_midi
from richard2 import rhythm_gen
from math import floor
# import nltk
#
# entries = nltk.corpus.cmudict.entries()
# len(entries)
#
# d_entries = {}
# for key, ph in entries:
#     ph_string = ' '.join(ph)
#     d_entries.update({key: ph_string.lower()})


letter_freq = {
    'A':440,
    'B':458.3333,
    'C':476.6666,
    'D':495,
    'E':513.3333,
    'F':531.6666,
    'G':550,
    'H':568.3333,
    'I':586.6666,
    'J':605,
    'K':623.3333,
    'L':641.6666,
    'M':660,
    'N':678.3333,
    'O':696.6666,
    'P':715,
    'Q':733.3333,
    'R':751.6666,
    'S':770,
    'T':788.3333,
    'U':806.6666,
    'V':825,
    'W':825,
    'X':843.3333,
    'Z':861.6666
}

text = "harriet"

words = text.split(' ')

letters = []
l_freqs = []


for word in words:
    for letter in word:
        letters.append(letter)
        l_freqs.append(letter_freq[letter.upper()])

vowels = 0
consonants = 0
characters = 0
pitches_center = 22
pitches_outer = 22

vowel_list = ['a', 'e', 'i', 'o', 'u']

for i in text:
    if i in vowel_list:
        vowels += 1
    else:
        consonants += 1
    characters += 1

lcm_values = [vowels, consonants, characters, pitches_center, pitches_outer]

rhythm_intervals = rhythm_gen(lcm_values)

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=12, time=0))

for i in range(len(letters)):
    j = i % len(rhythm_intervals)
    print(letters[i], l_freqs[i], rhythm_intervals[j])
    track.append(Message('note_on', note=floor(lazy_midi.freq2midi(l_freqs[i])), velocity=80, time=25))
    track.append(Message('note_on', note=floor(lazy_midi.freq2midi(l_freqs[i])), velocity=0, time=rhythm_intervals[j]))

mid.save(text+'.mid')

mid.play()
