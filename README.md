# Ulti Clips

Use Speech-to-Text AI to add annotations to videos of ultimate frisbee with recorded commentary, and then
edit the videos to clips matching selected parameters.

For example, if the audio includes "turnover" whenever one happens, the user can later make a compilation of all the turnovers in their video library.

## Current state
The MWP of using speech recordings and AI to split the video into points and then gluing the clips together remowing the time between points is working.

## Getting Started

### Dependencies

Using [Conda](https://docs.conda.io/en/latest/) for managing Python virtual environments is highly encouraged.

[Conda documentation on installation.](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

#### Video editing

We use a Python interface to [ffmpeg](https://ffmpeg.org/download.html) to process the video files.

[ffmpeg download page](https://ffmpeg.org/download.html)

#### Processing audio files

[WhisperX](https://github.com/m-bain/whisperX) is used to convert audio files into text annotations.

##### Installing WhisperX

Mostly following the [original WhisperX setup](https://github.com/m-bain/whisperX?tab=readme-ov-file#setup-%EF%B8%8F):

> Tested for PyTorch 2.0, Python 3.10 (use other versions at your own risk!)
> GPU execution requires the NVIDIA libraries cuBLAS 11.x and cuDNN 8.x to be installed on the system. Please refer to the [CTranslate2 documentation](https://opennmt.net/CTranslate2/installation.html).

You don't *need* GPU execution. It does speed things up, but a 2015 laptop handles speech-to-text with the `medium` model in almost real time.

###### 1. Create Python3.10 environment

```shell
conda create --name whisperx python=3.10
```

```shell
conda activate whisperx
```

###### 2. Install PyTorch

**Linux and Windows CUDA11.8**:

```shell
conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
```

**CPU only (laptop)**:

```shell
conda install pytorch==2.0.0 torchaudio==2.0.0 cpuonly -c pytorch
```

See other methods [here.](https://pytorch.org/get-started/previous-versions/#v200)

###### 3. Install the WhisperX project repo

```shell
pip install git+https://github.com/m-bain/whisperx.git
```

If already installed, update package to most recent commit

```shell
pip install git+https://github.com/m-bain/whisperx.git --upgrade
```

## Authors

Teemu Säilynoja

## License

This project is licensed under the GNU General Public License v2.0 License - see the [LICENSE](LICENSE) file for details.
