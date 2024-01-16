# Ulti Clips

A tool to annotate videos of ultimate from recorded speech, and then
edit the videos to clips matching selected parameters.

## Getting Started

### Dependencies

We use a Python interface to [ffmpeg](https://ffmpeg.org/download.html) to process the video files, and [whisperX](https://github.com/m-bain/whisperX) to convert audio files into text annotations.

Installing [Conda](https://docs.conda.io/en/latest/) for managing Python virtual environments is also highly encouraged.

### Installing

#### FFMPEG

Just follow the instructions at the [ffmpeg download page](https://ffmpeg.org/download.html).

#### Conda

[Conda documentation on installation.](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

#### WhisperX

Mostly following the [original WhisperX setup](https://github.com/m-bain/whisperX?tab=readme-ov-file#setup-%EF%B8%8F):

> Tested for PyTorch 2.0, Python 3.10 (use other versions at your own risk!)
> GPU execution requires the NVIDIA libraries cuBLAS 11.x and cuDNN 8.x to be installed on the system. Please refer to the [CTranslate2 documentation](https://opennmt.net/CTranslate2/installation.html).

You don't *need* GPU execution. It does speed things up, but a 2015 laptop handles speech-to-text with the `medium` model in almost real time.

##### 1. Create Python3.10 environment

```shell
conda create --name whisperx python=3.10
```

```shell
conda activate whisperx
```

##### 2. Install PyTorch

**Linux and Windows CUDA11.8**:

```shell
conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
```

**CPU only (laptop)**:

```shell
conda install pytorch==2.0.0 torchaudio==2.0.0 cpuonly -c pytorch
```

See other methods [here.](https://pytorch.org/get-started/previous-versions/#v200)

##### 3. Install the WhisperX project repo

```shell
pip install git+https://github.com/m-bain/whisperx.git
```

If already installed, update package to most recent commit

```shell
pip install git+https://github.com/m-bain/whisperx.git --upgrade
```

If wishing to modify this package, clone and install in editable mode:

```shell
git clone https://github.com/m-bain/whisperX.git
cd whisperX
pip install -e .
```

### Running the speech-to-text conversion

* How to run the program
* Step-by-step bullets

```
code blocks for commands
```

### Running the video processing

* How to run the program
* Step-by-step bullets

```
code blocks for commands
```
<!---
## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```
-->

## Authors

Teemu Säilynoja

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details
<!---
## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
--->
