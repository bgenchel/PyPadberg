# PyPadberg
A Python recreation of Harriet Padberg's 1965 Thesis, "Computer Composed Canon and Free Fugue," one of the first instances of algorithmic music created using a computer.

Run `python main.py` to start the program.

## How it works
* `main.py` creates an interface instance and runs it.
* `interface.py` defines the interface, which contains an instance of the Padberg object, defined in `padberg.py`
* The interface allows the user to input text and passes it to the Padberg object, which processes it according to our implementation of Padberg's original algorithm.
* The algorithm defines the pitch contour of the resulting cannon by mapping letters to a microtonal scale (defined in `padberg.py`), and defines the rhythm (`rhythm.py`) using the relatively prime factors of the least common multiple of 5 numbers:
  * the number of vowels
  * the number of consonants
  * the total length of the text
  * number of pitches in the 'center'
  * number of pitches in the 'outer'
    * (vaguely defined in the original paper)
* Once the text is processed, the interface directs the user to a screen displaying logging on text processing.
* Finally, the user is directed to a final control panel with which they can play back the generated music using a chosen sound and number of voices. Additionally, the user can enter a name for and save a midi file of the music.
