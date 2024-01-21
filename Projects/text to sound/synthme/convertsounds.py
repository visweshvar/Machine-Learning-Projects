# convertsounds.py
# Matches each phoneme from list with appropriate wav file

from synthme import phonemes
import wave, os

VOICE_PATH = os.path.dirname(__file__) + "/../data/voices/steve/"

def phonemes_to_sounds(phoneme_list, outfile):
    infiles = []
    for phoneme in phoneme_list:
        infiles.append(get_sound_file(phoneme))

    # Initialize parameters for crossfading
    crossfade_duration = 1000  # Duration of crossfade in frames (adjust as needed)
    overlap_frames = crossfade_duration // 2  # Half of crossfade duration for overlap

    data = []
    for idx, infile in enumerate(infiles):
        w = wave.open(infile, 'rb')
        frames = w.readframes(w.getnframes())
        data.append(frames)
        w.close()

        # Apply crossfading (except for the first and last phoneme)
        if idx > 0 and idx < len(infiles) - 1:
            data[-2] = apply_crossfade(data[-2], data[-1], overlap_frames)

    # Concatenate audio frames with crossfading
    output_frames = b"".join(data)

    # Write the output frames to the output WAV file
    output = wave.open(outfile, 'wb')
    output.setparams(w.getparams())
    output.writeframes(output_frames)
    output.close()

def get_sound_file(phoneme):
	fname = "%02d" % phoneme
	return VOICE_PATH + fname + ".wav"


def apply_crossfade(prev_frames, next_frames, overlap_frames):
    # Convert frames to bytearray to allow manipulation
    prev_frames = bytearray(prev_frames)
    next_frames = bytearray(next_frames)

    # Linear crossfade
    for i in range(overlap_frames):
        # Calculate crossfade coefficients
        coeff_prev = 1.0 - (i / overlap_frames)
        coeff_next = 1.0 - coeff_prev

        # Apply crossfade to frames
        for j in range(2 * i):  # Assuming each frame is 2 bytes (16-bit audio)
            prev_frames[-overlap_frames * 2 + j] = int(
                coeff_prev * prev_frames[-overlap_frames * 2 + j] +
                coeff_next * next_frames[j]
            )

    return bytes(prev_frames)
