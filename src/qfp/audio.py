import librosa as rosa
import librosa.util as util
import librosa.display as disp
import matplotlib.pyplot as plt

Default_Samplerate = 8000


def load_stream(path, snip=None):
    """
    Creates array of samples from input audio file
    snip = only return first n seconds of input
    """
    downsample = Default_Samplerate
    normalize = True

    audio, sr = rosa.load(path, sr=downsample, mono=True)

    if normalize:
        audio = util.normalize(audio)

    duration = rosa.get_duration(audio)
    if snip is not None:
        if snip > duration:
            util.fix_length(audio, snip)
        audio = audio[:snip * sr]

    return audio


def spec(y, sr=Default_Samplerate, n_fft=1024):
    freqs, times, mags = rosa.reassigned_spectrogram(y=y, sr=sr, n_fft=n_fft)
    return rosa.power_to_db(mags, amin=1e-10)


def show_spec(mags_db):
    disp.specshow(mags_db, x_axis="s", y_axis="linear", sr=Default_Samplerate, hop_length=1024//4, cmap="gray_r")
    plt.title("Spectrogram")
    plt.tick_params(axis='x', labelbottom=False)
    plt.show()
