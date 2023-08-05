from . import complain
from PIL import Image
import numpy as np
import pyfftw
import wave

pyfftw.interfaces.cache.enable()


class CalculatedFFT:
    """Stores data about FFTs calculated in a Sample."""

    def __init__(self, avgdata, spacing):
        self.avgdata = avgdata
        self.spacing = spacing


class Sample:
    """Reads and analyzes WAV files."""

    def __init__(self, filename, binsize=8192, volume=0.9, fundamental_freq=None):
        self.binsize = binsize

        if binsize < 2:
            raise complain.ComplainToUser("FFT bin size must be at least 2.")

        self._fundamental_freq = fundamental_freq
        self._fft = None
        self._img = None

        if isinstance(filename, str):
            self.filename = str
        else:
            try:
                self.filename = "<file handle {}>".format(filename.fileno())
            except:
                self.filename = "<unknown file handle>"

        self.wav = self.parse_wav(filename)

        max_amplitude = int(max(max(abs(min(chan)), abs(max(chan)))
                                for chan in self.wav))
        self.volume = 256 ** 4 / (max_amplitude * 2) * volume

    def parse_wav(self, filename):
        """Load a WAV file into a NumPy array."""
        try:
            with wave.open(filename, "rb") as wavfile:
                self.sampwidth = wavfile.getsampwidth()
                self.framerate = wavfile.getframerate()
                self.channels = wavfile.getnchannels()
                self.length = wavfile.getnframes()

                if self.sampwidth == 1:
                    self.size = np.int8
                elif self.sampwidth == 2:
                    self.size = np.int16
                elif self.sampwidth == 3 or self.sampwidth == 4:
                    self.size = np.int32
                else:
                    raise wave.Error

                wav = np.empty((self.channels, self.length), dtype=self.size)
                for i in range(0, self.length):
                    frame = wavfile.readframes(1)
                    for chan in range(self.channels):
                        wav[chan][i] = int.from_bytes(
                            frame[self.sampwidth * chan:self.sampwidth * (chan + 1)], byteorder="little", signed=True)
                return wav
        except IOError:
            raise complain.ComplainToUser(
                "Error opening WAV file at path '{}'.".format(filename))
        except wave.Error:
            raise complain.ComplainToUser(
                "This WAV type is not supported. Try opening the file in Audacity and exporting it as a standard WAV.")

    @property
    def fft(self):
        """Run a Fast Fourier Transform on the WAV file to create a histogram of frequencies and amplitudes."""
        if not self._fft:
            if self.binsize % 2 != 0:
                print(
                    "Warning: Bin size must be a multiple of 2, correcting automatically")
                self.binsize += 1
            spacing = float(self.framerate) / self.binsize
            avgdata = np.zeros(self.binsize // 2, dtype=np.float64)
            for chan in range(self.channels):
                for i in range(0, self.wav.shape[1], self.binsize):
                    data = np.array(
                        self.wav[chan][i:i + self.binsize], dtype=self.size)
                    if len(data) != self.binsize:
                        continue
                    fft = pyfftw.interfaces.numpy_fft.fft(data)
                    fft = np.abs(fft[:self.binsize // 2])
                    avgdata += fft
                    del data
                    del fft
            if max(avgdata) == 0:
                print(
                    "Warning: Bin size is too large to analyze sample; dividing by 2 and trying again")
                self.binsize = self.binsize // 2
                self._fft = self.fft
            else:
                self._fft = CalculatedFFT(avgdata, spacing)
        return self._fft

    @property
    def img(self):
        """Generate a PIL image from the WAV file."""
        if not self._img:
            self._img = Image.frombytes("I",
                                        (self.length, self.channels),
                                        (self.wav * self.volume).astype(np.int32).tobytes(),
                                        "raw", "I", 0, 1)
            # Pillow recommends those last args because of a bug in the raw parser
            # See
            # http://pillow.readthedocs.io/en/3.2.x/reference/Image.html?highlight=%22raw%22#PIL.Image.frombuffer
        return self._img

    @property
    def fundamental_freq(self):
        """Find the most prominent frequency from the FFT."""
        if not self._fundamental_freq:
            self._fundamental_freq = (
                np.argmax(self.fft.avgdata[1:]) * self.fft.spacing) + (self.fft.spacing / 2)
        return self._fundamental_freq

    def __len__(self):
        return self.length
