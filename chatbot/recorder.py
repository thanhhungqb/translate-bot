"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import wave

import pyaudio


def audio_record(audio_output_filename='output.wav', chunk=1024,
                 f_format=pyaudio.paInt16, channels=1, rate=44100,
                 record_seconds=5):

    p = pyaudio.PyAudio()

    stream = p.open(format=f_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("* recording")

    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(audio_output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(f_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
