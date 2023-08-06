"""sonusai speech_enh

usage: speech_enh [-hvntxw] [-i MIXID] (-p PREDICT) [-g MINGAIN] INPUT

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture to plot if input is a mixture database.
    -p PREDICT, --predict PREDICT   Predict directory.
    -g MINGAIN, --mingain MINGAIN   Minimum target gain threshold. [default: 0.01]
    -n, --noise                     Extract noise in addition to speech and include metrics.
    -t, --truth                     Calculate extraction using truth and include metrics.
    -x, --nowav                     Do not write WAV files.
    -w, --plot                      Write plots PDF for each mixture.

Run speech enhancement using PFILE model or prediction file and dataset MIXDB SonusAI mixture database directory.

Speech is estimated using a given extraction method on the mixture transform, and optionally noise is also
extracted.

TODO: Plot prediction data PFILE and optionally metrics and truth if feature+truth file is provided. PFILE is an HDF5
file with predict dataset or a WAV with a -m MODEL used to run prediction.

Spectrograms are plotted for truth types energy_f, snr_f, and mapped_snr_f.

INPUT is one of the following:

    * WAV
      Using the given model, generate feature data and run prediction. A model file must be
      provided. The MIXID is ignored. If --energy is specified, plot predict data as energy.

    * directory
      Using the given SonusAI mixture database directory, generate feature and truth data if not found.
      Run prediction if a model is given. The MIXID is required. (--energy is ignored.)

Prediction data will be written to OUTPUT if a model file is given and OUTPUT is specified.

There will be one plot per active truth index. In addition, the top 5 prediction classes are determined and
plotted if needed (i.e., if they were not already included in the truth plots). For plots generated using a
mixture database, then the target will also be displayed. If mixup is active, then each target involved will
be added to the corresponding truth plot.

Inputs:
    MODEL   A SonusAI trained ONNX model file. If a model file is given, prediction data will be
            generated.
    INPUT   A WAV file, or
            a directory containing a SonusAI mixture database

Outputs:
    {INPUT}-plot.pdf or {INPUT}-mix{MIXID}-plot.pdf
    plot.log
    OUTPUT (if MODEL and OUTPUT are both specified)

"""
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from pyaaware import FeatureGenerator

from sonusai import logger
from sonusai.mixture import AudioT
from sonusai.mixture import Feature
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict
from sonusai.mixture import Truth


def abs2(x):
    return x.real ** 2 + x.imag ** 2


def spec_plot(mixture: AudioT,
              feature: Feature,
              predict: Predict = None,
              target: AudioT = None,
              labels: List[str] = None,
              title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    num_plots = 4 if predict is not None else 2
    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[0].plot(x_axis, int16_to_float(mixture), label='Mixture')
    ax[0].set_xlim(x_axis[0], x_axis[-1])
    # ax[0].set_ylim([-1.025, 1.025])
    if target is not None:
        # Plot target time-domain waveform on top of mixture
        color = 'tab:blue'
        ax[0].plot(x - axis, int16_to_float(target), color=color, label='Target')
        ax[0].set_ylabel('magnitude', color=color)
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[0].set_title('Waveform')

    # Plot the spectrogram
    ax[1].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
    ax[1].set_title('Feature')

    if predict is not None:
        # Plot and label the model output scores for the top-scoring classes.
        mean_predict = np.mean(predict, axis=0)
        num_classes = predict.shape[-1]
        top_n = min(10, num_classes)
        top_class_indices = np.argsort(mean_predict)[::-1][:top_n]
        ax[2].imshow(np.transpose(predict[:, top_class_indices]), aspect='auto', interpolation='nearest', cmap='gray_r')
        y_ticks = range(0, top_n)
        ax[2].set_yticks(y_ticks, [labels[top_class_indices[x]] for x in y_ticks])
        ax[2].set_ylim(-0.5 + np.array([top_n, 0]))
        ax[2].set_title('Class Scores')

        # Plot the probabilities
        ax[3].plot(predict[:, top_class_indices])
        ax[3].legend(np.array(labels)[top_class_indices], loc='best')
        ax[3].set_title('Class Probabilities')

    fig.suptitle(title)

    return fig


def spec_energy_plot(mixture: AudioT,
                     feature: Feature,
                     target: AudioT = None,
                     truth_f: Truth = None,
                     predict: Predict = None,
                     tp_title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, int16_to_float(mixture), label='Mixture', color='mistyrose')
    ax[0].set_ylabel('magnitude', color='tab:blue')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    if target is not None:
        # Plot target time-domain waveform on top of mixture
        ax[0].plot(x_axis, int16_to_float(target), label='Target', color='tab:blue')
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[p].set_title('Waveform')

    # Plot the spectrogram
    p += 1
    ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Feature')

    if truth_f is not None:
        p += 1
        ax[p].imshow(np.transpose(truth_f), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth ' + tp_title)

    if predict is not None:
        p += 1
        ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)

    return fig


def spec3_plot(predict: Predict,
               truth_f: Truth = None,
               feature: Feature = None,
               title: str = '') -> plt.figure:
    """Plot up to three spectrograms:
            * feature (optional)
            * prediction
            * truth (optional)
    """
    num_plots = 1
    if truth_f is not None:
        num_plots += 1
    if feature is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot spectrograms
    p = 0
    if feature is not None:
        ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Feature ' + title)
        p += 1

    if num_plots == 1:
        # plt will not make an array if only 1
        ax.imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax.set_title('Predict ' + title)
    else:
        ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + title)

    if truth_f is not None:
        p += 1
        ax[p].imshow(np.transpose(truth_f), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth ' + title)

    return fig


def class_plot(mixture: AudioT,
               target: AudioT = None,
               truth_f: Truth = None,
               predict: Predict = None,
               label: str = '') -> plt.figure:
    """Plot mixture waveform with optional prediction and/or truth together in a single plot.
    The target waveform can optionally be provided, and prediction and truth can have multiple classes.

    Inputs:
        mixture     required, [samples, 1]
        target      optional, list of [samples, 1]
        truth_f     optional, [frames, 1]
        predict     optional, [frames, 1]
        label       optional, label name to use when plotting
    """
    from sonusai import SonusAIError
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    if mixture.ndim != 1:
        raise SonusAIError('Too many dimensions in mixture')

    if target is not None and target.ndim != 1:
        raise SonusAIError('Too many dimensions in target')

    # Set default to 1 frame when there is no truth or predict data
    frames = 1
    if truth_f is not None and predict is not None:
        if truth_f.ndim != 1:
            raise SonusAIError('Too many dimensions in truth_f')
        t_frames = len(truth_f)

        if predict.ndim != 1:
            raise SonusAIError('Too many dimensions in predict')
        p_frames = len(predict)

        frames = min(t_frames, p_frames)
    elif truth_f is not None:
        if truth_f.ndim != 1:
            raise SonusAIError('Too many dimensions in truth_f')
        frames = len(truth_f)
    elif predict is not None:
        if predict.ndim != 1:
            raise SonusAIError('Too many dimensions in predict')
        frames = len(predict)

    samples = (len(mixture) // frames) * frames

    # x-axis in sec
    x_axis = np.arange(samples, dtype=np.float32) / SAMPLE_RATE

    fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the time-domain waveforms then truth/prediction on second axis
    ax.plot(x_axis, int16_to_float(mixture[0:samples]), color='mistyrose', label='Mixture')
    color = 'red'
    ax.set_xlim(x_axis[0], x_axis[-1])
    # ax.set_ylim([-1.025, 1.025])
    ax.set_ylabel(f'Amplitude', color=color)
    ax.tick_params(axis='y', labelcolor=color)

    # Plot target time-domain waveform
    if target is not None:
        ax.plot(x_axis, int16_to_float(target[0:samples]), color='blue', label='Target')

    # instantiate 2nd y-axis that shares the same x-axis
    if truth_f is not None or predict is not None:
        y_label = 'Truth/Predict'
        if truth_f is None:
            y_label = 'Predict'
        if predict is None:
            y_label = 'Truth'

        ax2 = ax.twinx()

        color = 'black'
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim([-0.025, 1.025])
        ax2.set_ylabel(y_label, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        if truth_f is not None:
            ax2.plot(x_axis, expand_frames_to_samples(truth_f, samples), color='green', label='Truth')

        if predict is not None:
            ax2.plot(x_axis, expand_frames_to_samples(predict, samples), color='brown', label='Predict')

    # set only on last/bottom plot
    ax.set_xlabel('time (s)')

    fig.suptitle(label)

    return fig


def mix3_plot(mixture: AudioT,
              target: AudioT = None,
              wav1: AudioT = None,
              wav2: AudioT = None,
              title: str = '') -> plt.figure:
    """Plot mixture waveform with other waveforms (prediction, truth, etc.) together in a second plot.
    The target waveform can optionally be provided which is overlayed on top of mixture.

    Inputs:
        mixture     required, [samples, 1]
        target      optional, list of [samples, 1]
        wav1        optional, [frames, 1]
        wav2        optional, [frames, 1]
        title       optional, plot title
    """
    from sonusai import SonusAIError
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import int16_to_float

    if mixture.ndim != 1:
        raise SonusAIError('Too many dimensions in mixture')

    if target is not None and target.ndim != 1:
        raise SonusAIError('Too many dimensions in target')

    # Set default to 1 frame when there is no truth or wav2 data
    frames = 1
    if wav1 is not None and wav2 is not None:
        if wav1.ndim != 1:
            raise SonusAIError('Too many dimensions in wav1')
        t_frames = len(wav1)

        if wav2.ndim != 1:
            raise SonusAIError('Too many dimensions in wav2')
        p_frames = len(wav2)

        frames = min(t_frames, p_frames)
    elif wav1 is not None:
        if wav1.ndim != 1:
            raise SonusAIError('Too many dimensions in wav1')
        frames = len(wav1)
    elif wav2 is not None:
        if wav2.ndim != 1:
            raise SonusAIError('Too many dimensions in wav2')
        frames = len(wav2)

    samples = (len(mixture) // frames) * frames

    num_plots = 1
    if wav1 is not None or wav2 is not None:
        num_plots += 1

    # x-axis in sec
    x_axis = np.arange(samples, dtype=np.float32) / SAMPLE_RATE

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the mixture and optional truth waveforms
    p = 0
    ax[p].plot(x_axis, int16_to_float(mixture[0:samples]), color='mistyrose', label='Mixture')
    color = 'red'
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    ax[p].set_ylabel(f'Amplitude', color=color)
    ax[p].tick_params(axis='y', labelcolor=color)

    # Plot target time-domain waveform
    if target is not None:
        ax[p].plot(x_axis, int16_to_float(target[0:samples]), color='blue', label='Target')

    # instantiate 2nd plot
    if wav1 is not None or wav2 is not None:
        p += 1
        y_label = 'wav1/wav2'
        if wav1 is None:
            y_label = 'wav2'
        if wav2 is None:
            y_label = 'wav1'

        if wav1 is not None:
            ax[p].plot(x_axis, expand_frames_to_samples(wav1, samples), color='green', label=y_label)

        if wav2 is not None:
            ax[p].plot(x_axis, expand_frames_to_samples(wav2, samples), color='brown', label=y_label)

    # set only on last/bottom plot
    ax[p].set_xlabel('time (s)')

    fig.suptitle(title)

    return fig


def expand_frames_to_samples(x: np.ndarray, samples: int) -> np.ndarray:
    samples_per_frame = samples // len(x)
    return np.reshape(np.tile(np.expand_dims(x, 1), [1, samples_per_frame]), samples)


def calculate_unmapped_snr_f(mapped_snr_f: np.ndarray,
                             snr_db_mean: np.ndarray,
                             snr_db_std: np.ndarray,
                             limit_en: bool = False,
                             upper_thr: float = .9999,
                             lower_thr: float = .0001) -> np.ndarray:
    """Calculate unmapped SNR energy from mapped SNR per bin/class.
    Input mapped_snr_f typically [frames, bins] (bins = num_classes) i.e., truth_f or predict data
    limiter can be applied as min(upper_thr, mapped_snr_f) and max(lower_thr, mapped_snr_f)
    which is useful for metrics that need to avoid +/-Inf.
    Note: verified as exact match inverse of calculate_map_snr_f() without thresholds
          default thresholds of .0001, .9999 are equiv to snr_f of
    """
    import scipy.special as sc

    old_err = np.seterr(divide='ignore', invalid='ignore')
    if limit_en:
        mapped_snr_f = np.maximum(np.minimum(mapped_snr_f, upper_thr), lower_thr)
    snr_db = np.double(snr_db_std) * np.sqrt(2) * sc.erfinv(2 * np.double(mapped_snr_f) - 1)
    unmapped_snr_f = 10 ** ((snr_db + np.double(snr_db_mean)) / 10)
    np.seterr(**old_err)

    return np.float32(unmapped_snr_f)


def mean_square_error(truth_f: Truth, predict: Predict, squared: bool = False) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate mean square error or root-mean-square error between truth_f and predict.
    Typical inputs expected to be size [frames, num_classes|bins]
    Returns: 
        err     mean over both dimensions
        err_c   mean-over-dim0, i.e., a value per class/bin
        err_f   mean-over-dim1, i.e., a value per frame
    """
    sq_err = np.square(truth_f - predict)

    # mean over frames for value per class
    err_c = np.mean(sq_err, axis=0)

    # mean over classes for value per frame
    err_f = np.mean(sq_err, axis=1)

    # mean over all
    err = np.mean(sq_err)

    if not squared:
        err_c = np.sqrt(err_c)
        err_f = np.sqrt(err_f)
        err = np.sqrt(err)

    return err, err_c, err_f


def log_error(truth_f: Truth, predict: Predict) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate log error between truth_f and predict
    Typical inputs expected to be size [frames, num_classes|bins]
    Returns:
        err      mean over both dimensions, scalar value
        err_c    mean-over-dim0 i.e. a value per class/bin
        err_f    mean-over-dim1 i.e. a value per frame
    """
    sq_truth_f = np.real(truth_f * np.conjugate(truth_f))
    sq_predict = np.real(predict * np.conjugate(predict))
    log_err = abs(10 * np.log10((sq_truth_f + np.finfo(np.float32).eps) / (sq_predict + np.finfo(np.float32).eps)))

    # mean over frames for value per class
    err_c = np.mean(log_err, axis=0)

    # mean over classes for value per frame
    err_f = np.mean(log_err, axis=1)

    # mean over all
    err = np.mean(log_err)

    return err, err_c, err_f


def calculate_energy_f_from_audio(audio: AudioT, feature_gen: FeatureGenerator) -> np.ndarray:
    """Calculate energy_f from time-domain audio given specified feature generator."""
    from pyaaware import ForwardTransform

    from sonusai.mixture import MixtureDatabaseConfig
    from sonusai.mixture import get_pad_length
    from sonusai.utils import int16_to_float

    mixdb = MixtureDatabase(MixtureDatabaseConfig(feature=feature_gen.feature_mode,
                                                  num_classes=feature_gen.num_classes,
                                                  truth_mutex=False,
                                                  truth_reduction_function='max'))

    audio = np.pad(array=audio, pad_width=(0, get_pad_length(len(audio), mixdb.feature_step_samples)))

    target_fft = ForwardTransform(N=feature_gen.frame_size * 4, R=feature_gen.frame_size)

    frames = int(len(audio) / mixdb.feature_step_samples)
    bins = feature_gen.bin_end - feature_gen.bin_start + 1
    energy_f = np.zeros((frames, bins), dtype=np.float32)
    idx = 0
    for offset in range(0, len(audio), feature_gen.frame_size):
        energy_f[idx, :] = np.float32(
            target_fft.energy_f(int16_to_float(audio[offset:offset + feature_gen.frame_size])))
        idx += 1

    return energy_f


def calculate_energy_f_from_mixid(mixdb: MixtureDatabase, mixid: int) -> np.ndarray:
    """Calculate energy_f of mixid mixture waveform in mixdb (energy_f = power spectral density)
    Simply re-generate mixture and transform
    Note: only matches direct bin modes:  b**NN****, i.e. blh28bs1, bcr28bs1, ..."""
    from pyaaware import ForwardTransform

    from sonusai.mixture import get_mixture_data_deprecated
    from sonusai.utils import int16_to_float

    mixture, _, target, noise, _, _ = get_mixture_data_deprecated(mixdb=mixdb, mixid=mixid)

    tf = ForwardTransform(N=mixdb.frame_size * 4, R=mixdb.frame_size)
    mix_energy_f = tf.energy_f(int16_to_float(mixture))
    noise_energy_f = tf.energy_f(int16_to_float(noise))
    target_energy_f = tf.energy_f(int16_to_float(target))

    return mix_energy_f, target_energy_f, noise_energy_f


def mmse_stsa(xi: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """Computes the MMSE-STSA gain function.
    Arguments:
        xi      a priori SNR
        gamma   a posteriori SNR
    Returns:
        gain    MMSE-STSA gain function
   """
    from scipy.special import i0
    from scipy.special import i1

    old_err = np.seterr(divide='ignore', invalid='ignore', over='ignore')
    nu = np.multiply(xi, np.divide(gamma, np.add(1, xi)))
    # MMSE-STSA gain function
    gain = np.multiply(np.multiply(np.multiply(np.divide(np.sqrt(np.pi), 2),
                                               np.divide(np.sqrt(nu), gamma)), np.exp(np.divide(-nu, 2))),
                       np.add(np.multiply(np.add(1, nu), i0(np.divide(nu, 2))),
                              np.multiply(nu, i1(np.divide(nu, 2)))))
    # replace by Wiener gain
    idx = np.isnan(gain) | np.isinf(gain)
    # Wiener gain
    gain[idx] = np.divide(xi[idx], np.add(1, xi[idx]))
    np.seterr(**old_err)

    return gain


def speech_est_from_snr_f(mixture_tf: np.ndarray,
                          snr_f: np.ndarray,
                          min_gain: np.ndarray,
                          apost_snr: np.ndarray = None,
                          gfunc: callable = mmse_stsa) -> (np.ndarray, np.ndarray, np.ndarray):
    """Compute speech estimate from transform and estimation/prediction data
    Inputs:
        mixture_tf      mixture transform data ([frames, bins] complex float)
        snr_f           a-priori snr_f prediction or truth_f data [frames, bins]
                        frames can be smaller than mixture_tf frames, calculated gain will be zero-padded
        min_gain        minimum gain
        apost_snr       a-posteriori SNR
        gfunc           gain function type, e.g., 'mmse_stsa'
    Outputs:
        est_tf          speech estimate transform data ([frames, bins] complex float)
        gain            gain data [frames, bins], zero-padded in frame dimension if less than mixture_tf frames
        apost_snr       a-posteriori SNR estimated from snr_f (a-priori snr)
    """
    if apost_snr is None:
        # a-posteriori snr estimate, limited to -120 dB
        apost_snr = np.maximum(snr_f + 1, 1e-12)

    gain = np.maximum(gfunc(snr_f, apost_snr), min_gain)
    gain = np.pad(gain, ((0, mixture_tf.shape[0] - gain.shape[0]), (0, 0)))
    est_tf = mixture_tf * gain

    return est_tf, gain, apost_snr


def noise_est_from_snr_f(mixture_tf: np.ndarray,
                         snr_f: np.ndarray,
                         apost_snr: np.ndarray = None) -> (np.ndarray, np.ndarray, np.ndarray):
    """Compute noise estimate from transform and estimation/prediction data (snr_f)
    Inputs:
        mixture_tf      mixture transform data ([frames, bins] complex float)
        snr_f           a-priori snr_f prediction or truth_f data [frames, bins]
                        frames can be smaller than mixture_tf frames, calculated gain will be zero-padded
        apost_snr       a-posteriori SNR estimated from snr_f (a-priori snr)
                        Calculated internally if not provided
    Outputs:
        est_tf          noise estimate transform data ([frames, bins] complex float)
        gain            gain data [frames, bins], zero-padded in frame dimension if less than mixture_tf frames
        apost_snr       a-posteriori SNR estimated from snr_f (a-priori snr)
    """
    if apost_snr is None:
        # a-posteriori snr estimate, limited to -120 dB
        apost_snr = np.maximum(snr_f + 1, 1e-12)

    gain = (1 / np.square(1 + snr_f) + snr_f / ((1 + snr_f) * apost_snr))
    gain = np.pad(gain, ((0, mixture_tf.shape[0] - gain.shape[0]), (0, 0)))
    est_tf = mixture_tf * gain

    return est_tf, gain, apost_snr


def calculate_pesq(speech_ref: np.ndarray, speech_est: np.ndarray, error_value: float = 0) -> float:
    """Computes the PESQ score of speech estimate audio vs. the clean speech estimate audio.
    Upon error, assigns a value of 0, or user specified value in error_value
    Argument/s:
        speech_ref      speech reference audio, np.ndarray vector of samples.
        speech_est      speech estimated audio, np.ndarray vector of samples.
    Returns:
        score           float value between -0.5 and 4.5.
   """
    from pesq import NoUtterancesError
    from pesq import pesq

    try:
        score = pesq(16000, speech_ref, speech_est, mode='wb')
    except NoUtterancesError as e:
        score = error_value

    return score


def run_sonusai_hypermodel(hypermodel, model, feature):
    """Run hypermodel prediction on non-reshaped feature data."""
    from sonusai.data_generator import get_frames_per_batch
    from sonusai.utils import reshape_inputs
    from sonusai.utils import reshape_outputs

    # Pad with zeros in order to create an entire batches of data
    frames = feature.shape[0]
    frames_per_batch = get_frames_per_batch(hypermodel.batch_size, hypermodel.timesteps)
    padding = frames_per_batch - feature.shape[0] % frames_per_batch
    feature = np.pad(array=feature, pad_width=((0, padding), (0, 0), (0, 0)))
    feature, _ = reshape_inputs(feature=feature,
                                batch_size=hypermodel.batch_size,
                                timesteps=hypermodel.timesteps,
                                flatten=hypermodel.flatten,
                                add1ch=hypermodel.add1ch)
    predict = model.predict(feature, verbose=0)
    predict, _ = reshape_outputs(predict=predict, timesteps=hypermodel.timesteps)
    predict = predict[:frames, :]
    return predict


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixid = args['--mixid']
    predict_dir = args['--predict']
    mingain = float(args['--mingain'])
    noise_estimate_enable = args['--noise']
    truth_estimate_mode = args['--truth']
    disable_wav = args['--nowav']
    plot_en = args['--plot']
    input_name = args['INPUT']

    from os import makedirs
    from os.path import basename
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import h5py
    import keras_tuner as kt
    import pandas as pd
    from matplotlib.backends.backend_pdf import PdfPages
    from pyaaware import ForwardTransform
    from pyaaware import InverseTransform
    from pyaaware import Predict

    from sonusai import SonusAIError
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import calculate_audio_from_transform
    from sonusai.mixture import calculate_transform_from_audio
    from sonusai.mixture import get_mrecords_from_mixids
    from sonusai.utils import check_keras_overrides
    from sonusai.utils import create_ts_name
    from sonusai.utils import float_to_int16
    from sonusai.utils import import_keras_model
    from sonusai.utils import int16_to_float
    from sonusai.utils import write_wav

    output_dir = create_ts_name('speech_enh')
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    create_file_handler(join(output_dir, 'speech_enh.log'))
    update_console_handler(verbose)
    initial_log_messages('speech_enh')

    if not isdir(predict_dir):
        raise SonusAIError(f'{predict_dir} is not a directory')

    # Setup input file (truth)
    logger.info(f'Input:  {input_name}')
    iext = splitext(input_name)[1]
    ipath = splitext(input_name)[0]
    ibase_name = basename(splitext(input_name)[0])
    if iext == '.wav':
        logger.info(f'WAV file input not supported yet.')
        raise SystemExit(1)
    else:
        logger.info(f'Load mixdb from {input_name}')
        mixdb = MixtureDatabase(input_name)
        num_mixtures = len(mixdb.mixtures)
        # Review truth settings, use first target assuming all are the same
        settings = mixdb.targets[0].truth_settings[0]
        logger.info(f'Truth function is {settings.function} (est. from first target)')
        # Set up the transforms
        itf = InverseTransform(N=mixdb.fg.itransform_N, R=mixdb.fg.itransform_R, ttype=mixdb.fg.itransform_ttype)
        ftf = ForwardTransform(N=mixdb.fg.ftransform_N, R=mixdb.fg.ftransform_R, ttype=mixdb.fg.ftransform_ttype)

        logger.debug(f'Setup forward transform with N={ftf.N}, R={ftf.R}, ttype={ftf.ttype}')
        logger.debug(f'Setup inverse transform with N={itf.N}, R={itf.R}, ttype={itf.ttype}')
        mixid_padding = mixdb.mixid_padding
        mixid = mixdb.mixids_to_list(mixid)

    # Setup predict file
    keras_model = None
    onnx_model = None
    pext = splitext(predict_dir)[1]
    pbase_name = basename(splitext(predict_dir)[0])
    if isdir(predict_dir):
        logger.info(f'Prediction is a subdir, assuming it contains a set of prediction .h5 files')
        # TODO
    elif pext == ".wav":
        logger.info(f'Prediction is .wav, attempting model load from:  {model_name}')
        if model_name is not None:
            mbase_name = basename(splitext(model_name)[0])
            try:
                onnx_model = Predict(model_name)
            except Exception as e:
                raise SonusAIError(f'Error loading ONNX model {model_name}, exiting. Msg: {e}')

            logger.debug(f'Model feature name {model.feature}')
            logger.debug(f'Model input shape  {model.input_shape}')
            logger.debug(f'Model output shape {model.output_shape}')
        else:
            raise SonusAIError('Must specify -m .onnx model file when prediction input is .wav')
        output_dir = '.'
    elif pext == ".h5":
        logger.info(f'Prediction file is an HDF5 file, attempting to load predict data')
        with h5py.File(predict_dir, 'r') as f:
            if 'predict' in f:
                predict = np.array(f['predict'])

        if predict.ndim > 2:  # Check if timestep dimension and reshape to remove
            predict = np.reshape(predict, (predict.shape[0] * predict.shape[1], predict.shape[2]))

        # TODO: generate predict_wav here from predict data, assumes transform invertible
        output_dir = '.'
    else:
        # assume it's a SonusAI Keras .py file
        if weights_name is None:
            raise SonusAIError(f'Error: weight file not provided for {predict_dir}, exiting.')
        logger.info('Attempting Sonusai Keras .py hypermodel load')
        try:
            pymodel = import_keras_model(predict_dir)
            hypermodel = pymodel.MyHyperModel()
            if hypermodel.timesteps >= 0:
                timesteps = 1
            else:
                timesteps = 0
            check_keras_overrides(pymodel, mixdb.feature, mixdb.num_classes, timesteps, batch_size)
            hypermodel = pymodel.MyHyperModel(feature=mixdb.feature,
                                              num_classes=mixdb.num_classes,
                                              timesteps=timesteps,
                                              batch_size=batch_size)
            logger.info(f'Building model with batch_size {batch_size} and timesteps {hypermodel.timesteps}')
            keras_model = hypermodel.build_model(kt.HyperParameters())
            logger.info(f'Loading weights from {weights_name}')
            keras_model.load_weights(weights_name)

        except Exception as e:
            logger.exception(f'Error: {predict_dir} hypermodel load or build_model() failed, msg: {e}.')
            raise SystemExit(1)

    basepath = output_dir + '/'

    mrecords = get_mrecords_from_mixids(mixdb, mixid)
    num_mrecords = len(mrecords)

    # Main loop for each mixid run prediction, estimation, metrics
    truth_f = None
    noise_est_f = None
    for mi in range(num_mrecords):
        logger.info(f'Processing mixture {mixid[mi]} ({mi + 1} out of {num_mrecords})')
        # first target index only
        ti = mixdb.mixtures[mi].target_file_index[0]
        # first truth function only
        settings = mixdb.targets[ti].truth_settings[0]
        snr_db_mean = settings.config['snr_db_mean']
        snr_db_std = settings.config['snr_db_std']

        # 1) Generate feature and mixture transform data
        mixture, class_audio, noise, feature, truth_f = get_mixture_data_deprecated(mixdb, mrecords[mi])

        mixture = int16_to_float(mixture)
        mixture_tf = calculate_transform_from_audio(mixture, ftf)

        # TODO: make target, noise, and truth_f optional
        target = int16_to_float(class_audio[0])
        target_tf = calculate_transform_from_audio(target, ftf)

        noise = int16_to_float(noise)
        noise_tf = calculate_transform_from_audio(noise, ftf)

        # 2) Run prediction
        if keras_model is not None:
            predict = run_sonusai_hypermodel(hypermodel, keras_model, feature)
        elif onnx_model is not None:
            # TODO: create function reshape+predict to the onnx model batch, tstep
            predict = model.execute(feature)
        # TODO: add predict data file output

        # 3) Estimate speech and noise tf and .wav
        # Apply default limits for unmapping and metrics
        pred_snr_f = calculate_unmapped_snr_f(predict, snr_db_mean, snr_db_std, True)
        speech_est_f, target_gain, apost_snr = speech_est_from_snr_f(mixture_tf, pred_snr_f, mingain,
                                                                     gfunc='mmse_stsa')
        speech_est_wav = calculate_audio_from_transform(speech_est_f, itf)
        # TODO: make optional if noise enabled cli switch
        noise_est_f, noise_gain, _ = noise_est_from_snr_f(mixture_tf, pred_snr_f, apost_snr)
        noise_est_wav = calculate_audio_from_transform(noise_est_f, itf)

        # 4) Calculate speech and noise metrics (optional, if truth_f avail, and target, noise, etc.)
        if truth_f is not None:
            # SNR est accuracy: spectral distortion metric effectively the rmse of unmapped snr's in db
            truth_f_db = 10 * np.log10(truth_f + np.finfo(np.float32).eps)
            predict_db = 10 * np.log10(pred_snr_f + np.finfo(np.float32).eps)
            sd_snr, sd_snr_bin, sd_snr_frame = mean_square_error(truth_f_db, predict_db)
            # Speech PSD estimation accuracy symmetric mean log-spectral distortion (logerr):
            lerr_sp, lerr_sp_bin, lerr_sp_frame = log_error(target_tf, speech_est_f)
            # Speech intelligibility measure - PESQ
            pesq_speech = calculate_pesq(target, speech_est_wav)
            pesq_mixture = calculate_pesq(target, mixture)
            # pesq improvement
            pesq_impr = pesq_speech - pesq_mixture
            # pesq improvement %
            pesq_impr_pc = pesq_impr / (pesq_mixture + np.finfo(np.float32).eps) * 100
            if noise_est_f is not None:
                lerr_n, lerr_n_bin, lerr_n_frame = log_error(noise_tf, noise_est_f)

            # 5) Save per mixture metric results
            # Single row in table of scalar metrics per mixture
            mtable1_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi', 'PESQi%', 'SNRSD', 'SPLERR', 'NLERR', 'SPFILE', 'NFILE']
            ni = mixdb.mixtures[mi].noise_file_index
            metr1 = [mixdb.mixtures[mi].snr, pesq_mixture, pesq_speech, pesq_impr, pesq_impr_pc, sd_snr, lerr_sp,
                     lerr_n, basename(mixdb.targets[ti].name), basename(mixdb.noises[ni].name)]
            mtab1 = pd.DataFrame([metr1], columns=mtable1_col, index=[mi])
            # Stats of per frame estimation metrics
            efs_table2_col = ['Max', 'Min', 'Avg', 'Median']
            efs_table2_row = ['SNRSD', 'SPLERR', 'NLERR']
            metr2 = [[np.max(sd_snr_frame), np.min(sd_snr_frame), np.mean(sd_snr_frame), np.median(sd_snr_frame)],
                     [np.max(lerr_sp_frame), np.min(lerr_sp_frame), np.mean(lerr_sp_frame), np.median(lerr_sp_frame)],
                     [np.max(lerr_n_frame), np.min(lerr_n_frame), np.mean(lerr_n_frame), np.median(lerr_n_frame)]]
            mtab2 = pd.DataFrame(metr2, columns=efs_table2_col, index=efs_table2_row)

            mtab2flat_col = ['MXSNR', 'SNRSD Max', 'SNRSD Min', 'SNRSD Avg', 'SNRSD Median',
                             'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                             'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
            tmp = np.insert(np.array(metr2), 0, mixdb.mixtures[mi].snr).reshape(1, 13)
            mtab2_flat = pd.DataFrame(tmp, columns=mtab2flat_col, index=[mi])
            if 'all_mtab1' in locals():
                # Update all mixture table
                all_mtab1 = pd.concat([all_mtab1, mtab1])
                all_mtab2 = pd.concat([all_mtab2, mtab2_flat])
            else:
                # create the table if it doesn't exist
                all_mtab1 = mtab1
                all_mtab2 = mtab2_flat

            metric_fname = basepath + mixdb.mixtures[mi].name + '-spenh-metrics.txt'
            with open(metric_fname, 'w') as f:
                print('Speech enhancement metrics:', file=f)
                print(mtab1.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Extraction statistics over {mixture_tf.shape[0]} frames:', file=f)
                print(mtab2.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Target path: {mixdb.targets[ti].name}', file=f)
                print(f'Noise path: {mixdb.noises[ni].name}', file=f)
                # print(f'PESQ improvement: {pesq_impr:0.2f}, {pesq_impr_pc:0.1f}%', file=f)

            # 6) Estimate speech from truth to test the extraction-reconstruction methods, and calc metrics
            if truth_estimate_mode is True:
                truth_snr_f = calculate_unmapped_snr_f(truth_f, snr_db_mean, snr_db_std, True)
                speech_trest_f, tru_target_gain, apost_snr = \
                    speech_est_from_snr_f(mixture_tf, truth_snr_f, mingain, gfunc='mmse_stsa')
                speech_trest_wav = calculate_audio_from_transform(speech_trest_f, itf)
                noise_trest_f, noise_gain, _ = noise_est_from_snr_f(mixture_tf, truth_snr_f, apost_snr)
                noise_trest_wav = calculate_audio_from_transform(noise_trest_f, itf)

                # Speech PSD estimation accuracy symmetric mean log-spectral distortion (logerr):
                lerr_sptr, lerr_sptr_bin, lerr_sptr_frame = log_error(target_tf, speech_trest_f)
                # Speech intelligibility measure - PESQ
                pesq_speechtr = calculate_pesq(target, speech_trest_wav)
                # pesq improvement
                pesq_impr_sptr = pesq_speechtr - pesq_mixture
                # pesq improvement %
                pesq_impr_pctr = pesq_impr_sptr / (pesq_mixture + np.finfo(np.float32).eps) * 100
                lerr_ntr, lerr_ntr_bin, lerr_ntr_frame = log_error(noise_tf, noise_trest_f)

                mtable3_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi', 'PESQi%', 'SPLERR', 'NLERR']
                metr3 = [mixdb.mixtures[mi].snr, pesq_mixture, pesq_speechtr, pesq_impr_sptr, pesq_impr_pctr, lerr_sptr,
                         lerr_ntr]
                mtab3 = pd.DataFrame([metr3], columns=mtable3_col, index=[mi])

                # Stats of per frame estimation metrics
                efs_table4_col = ['Max', 'Min', 'Avg', 'Median']
                efs_table4_row = ['SPLERR', 'NLERR']
                metr4 = [[np.max(lerr_sptr_frame), np.min(lerr_sptr_frame), np.mean(lerr_sptr_frame),
                          np.median(lerr_sptr_frame)],
                         [np.max(lerr_ntr_frame), np.min(lerr_ntr_frame), np.mean(lerr_ntr_frame),
                          np.median(lerr_ntr_frame)]]
                mtab4 = pd.DataFrame(metr4, columns=efs_table4_col, index=efs_table4_row)

                # Append extraction metrics to metrics file:
                with open(metric_fname, 'a') as f:
                    print('', file=f)
                    print('Speech enhancement metrics of extraction method using truth:', file=f)
                    print(mtab3.round(2).to_string(), file=f)
                    print('', file=f)
                    print('Truth extraction statistics over frames:', file=f)
                    print(mtab4.round(2).to_string(), file=f)

                # Append to all mixture table
                mtab4flat_col = ['MXSNR', 'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                                 'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
                # Insert MXSNR
                tmp = np.insert(np.array(metr4), 0, mixdb.mixtures[mi].snr).reshape(1, 9)
                mtab4_flat = pd.DataFrame(tmp, columns=mtab4flat_col, index=[mi])
                if 'all_mtab3' in locals():
                    # Update all mixture table
                    all_mtab3 = pd.concat([all_mtab3, mtab3])
                    all_mtab4 = pd.concat([all_mtab4, mtab4_flat])
                else:
                    # create the table if it doesn't exist
                    all_mtab3 = mtab3
                    all_mtab4 = mtab4_flat

        # 7) write wav files
        if disable_wav is False:
            write_wav(name=basepath + mixdb.mixtures[mi].name + '-mixture.wav', audio=float_to_int16(mixture))
            write_wav(name=basepath + mixdb.mixtures[mi].name + '-speech_est.wav', audio=float_to_int16(speech_est_wav))
            if noise_est_f is not None:
                write_wav(name=basepath + mixdb.mixtures[mi].name + '-noise_est.wav',
                          audio=float_to_int16(noise_est_wav))
            if truth_f is not None:
                write_wav(name=basepath + mixdb.mixtures[mi].name + '-target.wav', audio=float_to_int16(target))
                write_wav(name=basepath + mixdb.mixtures[mi].name + '-noise.wav', audio=float_to_int16(noise))
                if truth_estimate_mode is True:
                    write_wav(name=basepath + mixdb.mixtures[mi].name + '-speech_trest.wav',
                              audio=float_to_int16(speech_trest_wav))
                    write_wav(name=basepath + mixdb.mixtures[mi].name + '-noise_trest.wav',
                              audio=float_to_int16(noise_trest_wav))

        # 8) Write out plot file
        if plot_en is True:
            plot_fname = basepath + mixdb.mixtures[mi].name + '-spenh-plots.pdf'

            # Original size [frames, stride, num_bands]
            # Decimate in the stride dimension
            # Reshape to get frames*decimated_stride, num_bands
            if feature is not None:
                if feature.ndim != 3:
                    raise SonusAIError(f'feature does not have 3 dimensions: frames, stride, num_bands')
                spectrogram = feature[:, -step:, :]
                spectrogram = np.reshape(spectrogram,
                                         (spectrogram.shape[0] * spectrogram.shape[1], spectrogram.shape[2]))
            else:
                spectrogram = None

            with PdfPages(pdf_name) as pdf:
                if mixture is None:
                    pdf.savefig(spec3_plot(predict=10 * np.log10(predict + np.finfo(np.float32).eps),
                                           truth_f=10 * np.log10(truth_f + np.finfo(np.float32).eps),
                                           feature=spectrogram,
                                           title=tfunc_name))
                else:
                    pdf.savefig(spec_energy_plot(mixture=mixture,
                                                 target=target,
                                                 feature=spectrogram,
                                                 truth_f=10 * np.log10(truth_f + np.finfo(np.float32).eps),
                                                 predict=10 * np.log10(predict + np.finfo(np.float32).eps),
                                                 tp_title=tfunc_name))

                    if target_tf is not None:
                        tg_spec = 10 * np.log10(abs2(target_tf) + np.finfo(np.float32).eps)
                        tg_est_spec = 10 * np.log10(abs2(target_est) + np.finfo(np.float32).eps)
                        # n_spec = np.reshape(n_spec,(n_spec.shape[0] * n_spec.shape[1], n_spec.shape[2]))
                        # TODO: change to tg_est when avail
                        pdf.savefig(spec3_plot(predict=tg_est_spec,
                                               truth_f=tg_spec,
                                               feature=spectrogram,
                                               title='target energy_f'))

                    if snr_sd is not None:
                        n_spec = 10 * np.log10(abs2(noise_tf) + np.finfo(np.float32).eps)
                        n_est_spec = 10 * np.log10(abs2(noise_est) + np.finfo(np.float32).eps)
                        pdf.savefig(spec3_plot(predict=n_est_spec,
                                               truth_f=n_spec,
                                               feature=spectrogram,
                                               title='noise energy_f'))

                        pdf.savefig(mix3_plot(mixture=noise_wav_est * 32768,
                                              target=noise,
                                              wav1=snr_sd_frame,
                                              wav2=None,
                                              title='Noise est'))

                        pdf.savefig(mix3_plot(mixture=target_wav_est * 32768,
                                              target=target,
                                              wav1=snr_sd_frame,
                                              wav2=None,
                                              title='Target est'))

            logger.info(f'Wrote plots to {pdf_name}')

    # 9) Done with mixtures, write out summary metrics
    # Calculate SNR summary for
    all_mtab1_sorted = all_mtab1.sort_values(by=['MXSNR', 'SPFILE'])
    all_mtab2_sorted = all_mtab2.sort_values(by=['MXSNR'])
    mtab_snr_summary = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(numeric_only=True).to_frame().T
    mtab_snr_summary_em = all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(numeric_only=True).to_frame().T
    for snri in range(1, len(mixdb.snrs)):
        mtab_snr_summary = pd.concat([mtab_snr_summary,
                                      all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                          numeric_only=True).to_frame().T])
        mtab_snr_summary_em = pd.concat([mtab_snr_summary_em,
                                         all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                             numeric_only=True).to_frame().T])

    if truth_estimate_mode is True:
        all_mtab3_sorted = all_mtab3.sort_values(by=['MXSNR'])
        all_mtab4_sorted = all_mtab4.sort_values(by=['MXSNR'])
        mtab_snr_summary_tr = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        mtab_snr_summary_emtr = all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        for snri in range(1, len(mixdb.snrs)):
            mtab_snr_summary_tr = pd.concat([mtab_snr_summary_tr,
                                             all_mtab3_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                 numeric_only=True).to_frame().T])
            mtab_snr_summary_emtr = pd.concat([mtab_snr_summary_emtr,
                                               all_mtab4_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                   numeric_only=True).to_frame().T])

    if num_mrecords > 1:
        metric_summary_fname = basepath + 'spenh-metrics-summary.txt'
        with open(metric_summary_fname, 'w') as f:
            print(f'Speech enhancement metrics avg over each SNR:', file=f)
            print(mtab_snr_summary.round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats avg over each SNR:', file=f)
            print(mtab_snr_summary_em.round(2).to_string(), file=f)
            print('', file=f)

            print(f'Speech enhancement metrics stats over all {num_mrecords} mixtures:', file=f)
            print(all_mtab1.describe().round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats over all {num_mrecords} mixtures:', file=f)
            print(all_mtab2.describe().round(2).to_string(), file=f)
            print('', file=f)

            if truth_estimate_mode is True:
                print(f'Truth-based speech enhancement metrics avg over each SNR:', file=f)
                print(mtab_snr_summary_tr.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistics stats avg over each SNR:', file=f)
                print(mtab_snr_summary_emtr.round(2).to_string(), file=f)
                print('', file=f)

                print(f'Truth-based speech enhancement metrics stats over all {num_mrecords} mixtures:', file=f)
                print(all_mtab3.describe().round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistic stats over all {num_mrecords} mixtures:', file=f)
                print(all_mtab4.describe().round(2).to_string(), file=f)
                print('', file=f)

            print('Speech enhancement metrics all-mixtures list:', file=f)
            print(all_mtab1.round(2).to_string(), file=f)
            print('', file=f)
            print('Extraction statistics all-mixtures list:', file=f)
            print(all_mtab2.round(2).to_string(), file=f)

            # Write summary to .csv file
            metric_summary_csvfname = basepath + 'spenh-metrics-summary.csv'
            pd.DataFrame([f'Speech enhancement metrics stats over {num_mrecords} mixtures:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab1.describe().round(2).to_csv(metric_summary_csvfname, encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            pd.DataFrame([f'Extraction statistics stats over {num_mrecords} mixtures:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab2.describe().round(2).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            pd.DataFrame(['Speech enhancement metrics of extraction method using truth, stats:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab3.describe().round(2).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            pd.DataFrame(['Truth extraction statistics stats:']).to_csv \
                (metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab4.describe().round(2).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8')
            pd.DataFrame(['']).to_csv(metric_summary_csvfname, mode='a', encoding='utf-8', index=False, header=False)

            metric_spenhcsv_fname = basepath + 'spenh-metrics-lst.csv'
            pd.DataFrame(['Speech enhancement metrics list:']).to_csv \
                (metric_spenhcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab1.round(2).to_csv(metric_spenhcsv_fname, mode='a', encoding='utf-8')

            metric_estatcsv_fname = basepath + 'spenh-metrics-estats-lst.csv'
            pd.DataFrame(['Extraction statistics list:']).to_csv \
                (metric_estatcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
            all_mtab2.round(2).to_csv(metric_estatcsv_fname, mode='a', encoding='utf-8')

            if truth_estimate_mode is True:
                metric_spenhcsv_fname = basepath + 'spenh-metrics-tru-lst.csv'
                pd.DataFrame(['Speech enhancement metrics list:']).to_csv \
                    (metric_spenhcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
                all_mtab3.round(2).to_csv(metric_spenhcsv_fname, mode='a', encoding='utf-8')

                metric_estatcsv_fname = basepath + 'spenh-metrics-estats-tru-lst.csv'
                pd.DataFrame(['Extraction statistics list:']).to_csv \
                    (metric_estatcsv_fname, mode='a', encoding='utf-8', index=False, header=False)
                all_mtab4.round(2).to_csv(metric_estatcsv_fname, mode='a', encoding='utf-8')

    # if output_name:
    #     with h5py.File(name=output_name, mode='w') as f:
    #         f.create_dataset(name='predict', data=predict)
    #         logger.info(f'Wrote predict data to {output_name}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
