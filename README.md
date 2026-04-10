# EEG-Blink Dataset

EEG-Blink is a public EEG dataset for blink recognition research. It includes voluntary blinks, involuntary blinks, and an additional set of naturally occurring blink recordings. The data were acquired using a single-channel portable MindBand device and can be used for blink detection, intention recognition, and human-computer interaction studies.

## Dataset Overview

- Number of subjects: 12 (6 male, 6 female)
- Age range: 22 to 40 years, with a mean age of 26 years and a standard deviation of 4.2 years
- Vision and health status: all subjects had normal vision, no history of neurological disease, and no prior EEG experience
- Acquisition device: MindBand portable EEG device with TGAM sensor
- Sampling rate: 512 Hz
- Electrode position: Fp1 (left forehead), with the reference electrode placed on the left earlobe
- Experimental paradigm: time-cued text-based visual stimulation

## Experimental Design

### Main Experiment: Voluntary and Involuntary Blinks

The main experiment used fixed 4 s text-based visual prompts to guide subjects through the blink task. The formal recording process for each subject consisted of two phases: an involuntary blink phase and a voluntary blink phase. The two phases were alternated with a 1-minute rest interval between them. Each phase contained 15 trials, for a total of 30 trials.

- Involuntary blink phase: subjects kept both hands naturally placed and performed blink actions without motor imagery intent when prompts appeared, simulating everyday natural blinking behavior.
- Voluntary blink phase: subjects placed their right hand on the mouse and imagined a mouse-click action while blinking, thereby inducing voluntary blink signals accompanied by motor intent.

Each subject completed a pre-experiment session before the formal recording to become familiar with the procedure and reduce operational errors during data collection.

### Supplementary Experiment: Natural Blinks

To evaluate the detection capability of EEG-Blink in real-world scenarios without prompt guidance, we additionally collected natural blink data. Six subjects from the main experiment were recalled for a free-reading task (4 male, 2 female). No blink prompts were provided during recording. Subjects read articles freely through a computer interface, allowing the capture of natural blink signals under completely unconstrained conditions.

Because natural blinks are random and low-frequency, each trial lasted 1 minute to ensure sufficient valid samples, and each subject completed 15 trials.

## Data Organization

The data are organized by subject in separate folders, with a structure similar to the following:

- `data_subject1/`
- `data_subject2/`
- `...`
- `data_subject12/`

Each subject folder contains subfolders for the experimental conditions:

- `Involuntary Blink/`
- `Voluntary Blink/`
- `Natural Blink/` (available for only some subjects)

Files are typically named in the form "subject ID_trial ID", such as `1_1.TXT` and `10_15.TXT`. Some files may retain the lowercase extension `txt` or uppercase `TXT`; this does not affect the data content.

## Data Format

The raw EEG data are stored as plain text files, and each file corresponds to one trial. The included `eeg_processing.py` script provides a parsing and visualization example that can be used to read the raw files, extract the single-channel signal, and generate processed outputs.

Example output files produced by the script:

- `data_small.txt`: single-channel EEG sequence
- `data_big.txt`: multi-channel or extended-format data

Note: the input and output paths in the script currently use placeholders and must be updated to match the local data location before running.

## Research Use Cases

This dataset can be used for the following tasks:

- Blink detection and blink event localization
- Voluntary vs. involuntary blink classification
- Prompt-free blink detection in natural settings
- Single-channel EEG analysis and human-computer interaction research

## Citation

If you use this dataset in your research, please cite the original publication. If needed, I can also help format the citation as a standard BibTeX entry.

## Contact

For further information, data format details, or citation information, please contact the dataset authors or maintainers.

