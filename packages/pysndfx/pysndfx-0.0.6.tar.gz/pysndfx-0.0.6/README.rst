pysndfx `|Build Status| <https://travis-ci.org/carlthome/python-audio-effects>`_
================================================================================

**Apply audio effects such as reverb and EQ directly to audio files or
NumPy ndarrays.**

This is a lightweight Python wrapper for SoX, the Swiss Army knife of
sound processing programs. Supported effects range from EQ, compression
and noise reduction to phasers, reverbs and pitch shifters.

Install
-------

Install with pip as: ``sh pip install pysndfx`` The system must also
have `SoX <http://sox.sourceforge.net/>`_ installed (for Debian-based
operating systems: ``apt install sox``, or with Anaconda as
``conda install -c conda-forge sox``)

Usage
-----

First create an audio effects chain.
``python # Import the package and create an audio effects chain. from pysndfx import AudioEffectsChain apply_audio_fx = (AudioEffectsChain()                      .phaser()                      .reverb())``
Then we can call the effects chain object with paths to audio files, or
directly with NumPy ndarrays. \`\`\`python infile =
'my\_audio\_file.wav' outfile = 'my\_processed\_audio\_file.ogg'

Apply phaser and reverb directly to an audio file.
==================================================

apply\_audio\_fx(infile, outfile)

Or, apply the effects directly to a NumPy ndarray.
==================================================

from librosa import load x, sr = load(infile, sr=None) y =
apply\_audio\_fx(x)

Apply the effects and return the results as a NumPy ndarray.
============================================================

y = apply\_audio\_fx(infile)

Apply the effects to a NumPy ndarray but store the resulting audio to disk.
===========================================================================

apply\_audio\_fx(x, outfile)
``There's also experimental streaming support. Try applying reverb to a microphone input and listening to the results live like this:``sh
python -c "from pysndfx import AudioEffectsChain;
AudioEffectsChain().reverb()(None, None)" \`\`\`

.. |Build
Status| image:: https://travis-ci.org/carlthome/python-audio-effects.svg?branch=master
