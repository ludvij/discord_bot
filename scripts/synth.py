import pyaudio
import numpy as np
import math
from time import sleep

class Basic_synth:
	def __init__(self):
		pass

	def open(self, amplitude:float=0.1, samples:int=44100):
		if amplitude < 0 or amplitude > 1:
			raise Exception("invalid audio")
		
		self.amplitude = amplitude
		self.samples = samples
		self.p = pyaudio.PyAudio()
		self.stream = stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=samples, output=True)

	def play_sine(self, freq:float, duration:float):
		# this is basically A * sin(2pi * x * f / samples)
		# x goes from [0, samples * duration)
		# normal sine wave
		PI = np.pi
		samples = (self.amplitude * np.sin(2*PI*np.arange(self.samples*duration) * freq/self.samples)).astype(np.float32).tobytes()
		self.stream.write(samples)

	def close(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()


def note_to_freq(noc:(str, int)):
	NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
	OCTAVE_MULT = 2
	STD_NOTE = 'A'; STD_NOTE_OCT = 4; STD_NOTE_FREQ = 440

	note = noc[0]
	octave = noc[1]
	# get absoulte index and index in oct of note
	note_index = NOTES.index(note)
	note_absolute_index = len(NOTES) * octave + note_index

	# get distance from note to A4
	# positive if note in higher oct and neg if lower
	A_index = NOTES.index(STD_NOTE)
	A_absolute_index = STD_NOTE_OCT * len(NOTES) + A_index
	distance = note_absolute_index - A_absolute_index

	# get freq from distance applying the inverse of the logarithm
	note_mult = OCTAVE_MULT ** (1/len(NOTES))
	rel_freq = note_mult ** distance
	freq = STD_NOTE_FREQ * rel_freq

	return freq


def freq_to_note(freq:int):
	# twelve western notes
	NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
	OCTAVE_MULT = 2
	STD_NOTE = 'A'; STD_NOTE_OCT = 4; STD_NOTE_FREQ = 440

	# cacluate distance to A4
	# since notes are spread evenly. going up a note will multiply by a constant
	# so we can ise a log to know how many times a freq was multiplied to get from A4 to our note
	# this will give a positive integer value for notes higher than A4, and a negative for lower
	note_mult = OCTAVE_MULT ** (1/len(NOTES))
	rel_freq = freq / STD_NOTE_FREQ
	distance = math.log(rel_freq, note_mult)

	# round to make up for floating point inaccuracies
	distance = round(distance)

	# using the distance in noteas ad the octave and name of A4
	# we can calculate the octave and name of our note
	A_index = NOTES.index(STD_NOTE)
	A_absolute_index = STD_NOTE_OCT * len(NOTES) + A_index

	note_absolute_index = A_absolute_index + distance
	note_octave = note_absolute_index // len(NOTES)
	note_index = note_absolute_index % len(NOTES)
	note_name = NOTES[note_index]

	return (note_name, note_octave)


def main():
	min_unit = 0.075
	bs = Basic_synth()
	bs.open(amplitude=0.2)
	for i in range(3):
		bs.play_sine(note_to_freq(('D',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('D',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('D',  5)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('A',  4)), min_unit*1)
		bs.play_sine(0, min_unit*4)
		bs.play_sine(note_to_freq(('G#', 4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('D',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)

		bs.play_sine(note_to_freq(('C',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('C',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('D',  5)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('A',  4)), min_unit*1)
		bs.play_sine(0, min_unit*4)
		bs.play_sine(note_to_freq(('G#', 4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('D',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)

		bs.play_sine(note_to_freq(('B',  3)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('B',  3)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('D',  5)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('A',  4)), min_unit*1)
		bs.play_sine(0, min_unit*4)
		bs.play_sine(note_to_freq(('G#', 4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('D',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)

		bs.play_sine(note_to_freq(('A#', 3)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('A#', 3)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('D',  5)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('A',  4)), min_unit*1)
		bs.play_sine(0, min_unit*4)
		bs.play_sine(note_to_freq(('G#', 4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*2)
		bs.play_sine(note_to_freq(('D',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('F',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)
		bs.play_sine(note_to_freq(('G',  4)), min_unit*1)
		bs.play_sine(0, min_unit*1)

	bs.close()
	


if __name__ == '__main__':
	main()