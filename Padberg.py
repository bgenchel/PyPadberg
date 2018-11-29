from audiolazy import lazy_midi
from math import floor
from mido import Message, MidiFile, MidiTrack
from rhythm import rhythm_gen
from string import ascii_lowercase
from synth import synth

PITCHES_CENTER = 22
PITCHES_OUTER = 22

LETTER_FREQS = {
    'a': 440,
    'b': 458.3333,
    'c': 476.6666,
    'd': 495,
    'e': 513.3333,
    'f': 531.6666,
    'g': 550,
    'h': 568.3333,
    'i': 586.6666,
    'j': 605,
    'k': 623.3333,
    'l': 641.6666,
    'm': 660,
    'n': 678.3333,
    'o': 696.6666,
    'p': 715,
    'q': 733.3333,
    'r': 751.6666,
    's': 770,
    't': 788.3333,
    'u': 806.6666,
    'v': 825,
    'w': 825,
    'x': 843.3333,
    'y': 586.6666,
    'z': 861.6666
}


class Padberg:

    def __init__(self):
        self._mid = None
        self._freqs = None
        self._durs = None
        self._log = []

    def _print(self, text):
        self._log.append(text)

    def _reset_log(self):
        self._log = []

    def _sanitize_text(self, text):
        return "".join([c for c in text.lower() if c in ascii_lowercase or c == ' '])

    def process_text(self, text):
        self._reset_log()
        self._print("::INFO:: Received Text - %s" % text)
        text = self._sanitize_text(text)
        self._print("::INFO:: Sanitized Text - %s" % text)

        words = text.split(' ')

        letters = []
        l_freqs = []
        y_used = 0

        for word in words:
            for letter in word:
                letters.append(letter)
                if letter == 'y':
                    if y_used == 0:
                        l_freqs.append(LETTER_FREQS['i'])
                        y_used = 1
                    else:
                        l_freqs.append(LETTER_FREQS['z'])
                else:
                    l_freqs.append(LETTER_FREQS[letter.lower()])

        vowels = 0
        consonants = 0
        characters = 0

        vowel_list = ['a', 'e', 'i', 'o', 'u']

        for i in text:
            if i in vowel_list:
                vowels += 1
            else:
                consonants += 1
            characters += 1

        lcm_values = [vowels, consonants, characters, PITCHES_CENTER, PITCHES_OUTER]
        rhythm_intervals = rhythm_gen(lcm_values)

        self._mid = MidiFile()
        track = MidiTrack()
        self._mid.tracks.append(track)

        track.append(Message('program_change', program=12, time=0))
        durations = []
        for i in range(len(letters)):
            j = i % len(rhythm_intervals)
            durations.append(rhythm_intervals[j])
            self._print("::INFO:: Processing - letter: {}, freq: {}, rhythm_interval: {}".format(letters[i], l_freqs[i], rhythm_intervals[j]))
            track.append(Message('note_on', note=floor(lazy_midi.freq2midi(l_freqs[i])), velocity=80, time=25))
            track.append(Message('note_on', note=floor(lazy_midi.freq2midi(l_freqs[i])), velocity=0, time=rhythm_intervals[j]))

        self._freqs = l_freqs
        self._durs = durations

    def get_summary(self):
        indices = [str(i) for i in range(len(self._log))]
        return list(zip(self._log, indices))

    def save(self, title=None):
        if title:
            self._mid.save(title + '.mid')
        else:
            self._mid.save('output.mid')

    def play(self, sound=1, num_voices=1):
        synth(self._freqs, self._durs, sound, num_voices)
