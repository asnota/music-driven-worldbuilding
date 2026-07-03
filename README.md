# Music-Driven Worldbuilding: Audio-Reactive HDRI Generation for VR

This repository contains the prototype implementation supporting the research paper:

**“Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI”**

Accepted for presentation at **EVA London 2026 (Electronic Visualisation and the Arts Conference)**.

The project demonstrates a workflow where **AI-generated HDRI environments and music** can be created and integrated into **Unreal Engine 5 VR scenes**, enabling experimental **audio-reactive worldbuilding pipelines**.

The repository includes:

* A **Python/Flask HDRI generation service**
* A **Diffusion-based music audio generative pipeline**
* Integration instructions for **Unreal Engine HDRI environments**
* A **GPU-accelerated workflow using CUDA + PyTorch**

---

# Project Overview

The goal of this project is to explore how **generative multimodal AI can be used to produce immersive virtual environments from multimodal inputs**.

The system generates **HDR panoramic environments (.hdr)** and **music audio files (.wav)** which can then be imported into **Unreal Engine**. The generated HDRI can then be with the **HDRIBackdrop plugin** to create atmospheric VR spaces, while generated music audio can be mapped to audio-reactive Niagara system, translating audio properties into motion patterns and colour.

Potential applications include:

* AI-assisted **worldbuilding**
* **music-responsive virtual environments**
* creative tools for **artists and musicians**

---

# System Architecture

Pipeline overview:

```
Input (music / prompt / parameters)
        ↓
Flask Application
        ↓
Music Generation (.wav)
        ↓
HDRI Image Generation (.hdr)
        ↓
Unreal Engine 5
        ↓
VR Scene with HDRIBackdrop and Niagara system
```

---

# Requirements

## Hardware

Recommended:

* NVIDIA GPU with CUDA support
* Minimum 8GB VRAM

---

## Software

* Python **3.11**
* CUDA-compatible GPU
* Unreal Engine **5.4** and higher

---

# CUDA Setup

First verify that CUDA is installed.

Open **Command Prompt**:

```
nvcc --version
```

If CUDA is missing, install it from:

[https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)

You can also verify GPU support using:

```
nvidia-smi
```

For PyTorch compatibility check:

[https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

---

# Python Environment Setup (uv)

This project uses **uv** for dependency and environment management.

Documentation:
[https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

---

# Setup & Usage

## Prerequisites

- **Git** installed and available on PATH
- **Windows** with an NVIDIA GPU + CUDA 12.8 compatible drivers (for the PyTorch CUDA build)

## 1. Clone the repository

```bash
git clone https://github.com/asnota/music-driven-worldbuilding
cd music-driven-worldbuilding
```
## 2. Run the setup script

From **Command Prompt (cmd)**, run:

```bash
setup.bat
```

This will automatically:

- Install [uv](https://docs.astral.sh/uv/) (if not already installed)
- Install and pin **Python 3.11**
- Create the `.venv` virtual environment and install all dependencies from `pyproject.toml` (`uv sync`)
- Install the **PyTorch CUDA build** and training utilities (`tensorboardX`, `pytorch_lightning`)

When it finishes, the environment is activated and ready.

> **Note:** If `uv` was just installed for the first time, you may need to open a **new** terminal before re-running `setup.bat` so that `uv` is available on your PATH.

## 3. Run inference

Activate the `flask-app` virtual environment and start the Flask app:

```bash
cd flask-app
.venv\Scripts\activate
uv run app.py
```
---

# Running the Flask Application

Once dependencies are installed:

```
uv run app.py
```

The Flask service will start locally and will be available at port 5000: .

Generated **.hdr panoramic environment maps** will be stored into `generated_panorama_web`. 
Generated **.wave music files** will be available in `generated_music` folder inside flask-app.


---

# Unreal Engine Integration

Video reference for workflow:

ToDo

---

## 1. Open your UE5 project

Launch Unreal Engine and open the target project.

---

## 2. Enable HDRIBackdrop Plugin

Navigate to:

```
Edit → Plugins
```

Search for:

```
HDRIBackdrop
```

Enable the plugin and restart the project. 
More information on plugin installation: [https://dev.epicgames.com/documentation/en-us/unreal-engine/hdri-backdrop-visualization-tool-in-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/hdri-backdrop-visualization-tool-in-unreal-engine)

---

## 3. Add HDRIBackdrop Actor

From the top menu:

```
Place Actors Panel
```

Search for:

```
HDRIBackdrop
```

Drag it into the scene.

---

## 4. Import Generated HDRI

Import the generated `.hdr` file into the Unreal project content browser.

---

## 5. Assign HDRI to Scene

1. Select the **HDRIBackdrop actor**
2. In the **Details panel**
3. Assign the imported `.hdr` file to:

```
Cubemap
```

---

## 6. Adjust Exposure

Generated HDRI environments may appear **overexposed**.

Adjust:

```
Intensity
```

inside the HDRIBackdrop actor settings.

---

## 7. Add Audio to the Scene

1. Import an audio file into the UE5 project (`.wav` file).
2. Drag the audio asset from the UE5 **Content Browser** into the scene.
3. The Niagara system included in the scene will automatically react to the audio.
4. Click **Simulate** in the toolbar to preview the audio-reactive effect.

---

# Research Context

This prototype supports the research project:

**Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI**

Accepted for presentation at:

**EVA London 2026 — Electronic Visualisation and the Arts**

The work investigates how **AI-generated HDRI environments can serve as building blocks for immersive, music-driven virtual worlds**.

---

# Repository Structure

```
project-root/
├── flask-app/
│   ├── app.py
│   ├── generated_music/
│   ├── generated_panorama_web/
│   └── Text2Light/
│
├── vr-template/
│
└── README.md
```

---

# Future Work

Planned extensions include:

* real-time **audio-reactive HDRI generation**
* integration with **live music input**
* automated **UE5 pipeline scripting**
* improved **lighting calibration**
* **VR interaction tools**

---

# Citation

If you use this repository in academic work, please cite:

```bibtex
@inproceedings{shvets2026music,
  author    = {Shvets, Anna and Li, Qi and Zhao, Huilai},
  title     = {Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI},
  booktitle = {Electronic Visualisation and the Arts (EVA London 2026)},
  year      = {2026},
  address   = {London, UK}
}
```

---

# License

Research prototype — license to be defined.

---

# Acknowledgement and Original Repository

This repository is a **`uv`-based environment adaptation and experimental extension** of the original project:

**HDRI-and-music-audio-generation**
[https://github.com/QiLi0703/HDRI-and-music-audio-generation.git](https://github.com/QiLi0703/HDRI-and-music-audio-generation.git)

The original repository provides the core implementation for **HDRI generation driven by music/audio inputs using deep generative models**.

This project adapts the original implementation by:

* migrating the environment setup to **`uv` for modern Python dependency management**
* providing a **clean reproducible installation pipeline**
* adding documentation for **Unreal Engine 5 HDRI workflows**

All credit for the **original HDRI generation framework and research implementation** goes to the authors of the original repository.

---

## Original Project

If you want to explore the base implementation, please visit:

**QiLi0703 – HDRI and Music Audio Generation**

[https://github.com/QiLi0703/HDRI-and-music-audio-generation](https://github.com/QiLi0703/HDRI-and-music-audio-generation)

---

## Why This Adaptation?

The original repository relies on a **traditional Python environment setup**, which can be difficult to reproduce across machines.

This adaptation focuses on:

* **reproducible environments**
* **modern dependency management with `uv`**
* easier **GPU configuration**
* integration with **XR workflows (Unreal Engine)**

## Contribution to the Research Project

**Anna Shvets**

* Idea conceptualisation
* Project supervision
* Case study creation with original music composition
* Article writing
* Adaptation of the Flask app generative pipeline to `uv`
* Adaptation of the UE5 project template to HDRIBackdrop

**Qi Li**

* Development of the music generative pipeline for the Flask app
* Creation of the audio-reactive Niagara system with custom HLSL code translating frequency bands into colour
* Literature search on generative music and audio

**Huilai Zhao**

* Development of the HDRI generative pipeline for the Flask app
* Literature search on HDRI generation
