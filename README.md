# Music-Driven Worldbuilding: Audio-Reactive HDRI Generation for VR

This repository contains the prototype implementation supporting the research paper:

**“Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI”**

Accepted for presentation at **EVA London 2026 (Electronic Visualisation and the Arts Conference)** as a **15-minute paper presentation**.

The project demonstrates a workflow where **AI-generated HDRI environments** can be created and integrated into **Unreal Engine 5 VR scenes**, enabling experimental **audio-reactive worldbuilding pipelines**.

The repository includes:

* A **Python/Flask HDRI generation service**
* A **Diffusion-based generative pipeline**
* Integration instructions for **Unreal Engine HDRI environments**
* A **GPU-accelerated workflow using CUDA + PyTorch**

---

# Project Overview

The goal of this project is to explore how **generative AI can be used to produce immersive virtual environments from multimodal inputs**, such as music, text prompts, or symbolic representations.

The system generates **HDR panoramic environments (.hdr)** which can then be imported into **Unreal Engine** and used with the **HDRIBackdrop plugin** to create atmospheric VR spaces.

Potential applications include:

* AI-assisted **worldbuilding**
* **music-responsive virtual environments**
* generative **XR environments**
* creative tools for **artists and designers**

---

# System Architecture

Pipeline overview:

```
Input (music / prompt / parameters)
        ↓
Flask Application
        ↓
Diffusion-based Generation (PyTorch)
        ↓
HDRI Environment (.hdr)
        ↓
Unreal Engine 5
        ↓
VR Scene with HDRIBackdrop
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
* Unreal Engine **5.x**

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

## 1. Install uv

Run in **PowerShell**:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 2. Install Python 3.11

```
uv python install 3.11
uv python pin 3.11
```

---

## 3. Create the Project

```
uv init hdri3
cd hdri3
```

---

## 4. Initialize Environment

Run the application once to initialize the virtual environment:

```
uv run main.py
```

---

# Install Dependencies

## PyTorch (CUDA build)

```
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

---

## Core Dependencies

```
uv add flask psutil scipy diffusers==0.34.0 transformers==4.28.0
```

---

## Additional Libraries

```
uv add opencv-python faiss-cpu omegaconf openexr setuptools==81 termcolor einops ftfy
```

---

## Training / Logging Utilities

```
uv pip install tensorboardX pytorch_lightning
```

---

# Running the Flask Application

Once dependencies are installed:

```
uv run main.py
```

The Flask service will start locally and expose endpoints used for **HDRI generation**.

The application will output generated **.hdr panoramic environment maps**.

---

# Unreal Engine Integration

Video reference for workflow:

[https://youtu.be/5TMncLHoawI](https://youtu.be/5TMncLHoawI)

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

# Research Context

This prototype supports the research project:

**Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI**

Accepted for presentation at:

**EVA London 2026 — Electronic Visualisation and the Arts**

The work investigates how **AI-generated HDRI environments can serve as building blocks for immersive, music-driven virtual worlds**.

---

# Repository Structure

```
hdri3/
│
├── main.py
├── generation/
├── models/
├── outputs/
├── requirements
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

```
Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI
EVA London, 2026
```

---

# License

Research prototype — license to be defined.

---

If you'd like, I can also help you create:

* a **much more polished research-lab README (the kind that gets stars on GitHub)**
* a **diagram of the architecture for the paper**
* a **GitHub repo structure ready for reviewers and open-source release**.
---
Here is the **updated README section** you can add to your repository to clearly acknowledge the original work and explain that this project is a **`uv`-based adaptation**. I integrated it in a natural GitHub style (commonly expected in research repos).

You can place this section **after the Project Overview** or **before the License**.

---

# Acknowledgement and Original Repository

This repository is a **`uv`-based environment adaptation and experimental extension** of the original project:

**HDRI-and-music-audio-generation**
[https://github.com/QiLi0703/HDRI-and-music-audio-generation.git](https://github.com/QiLi0703/HDRI-and-music-audio-generation.git)

The original repository provides the core implementation for **HDRI generation driven by music/audio inputs using deep generative models**.

This project adapts the original implementation by:

* migrating the environment setup to **`uv` for modern Python dependency management**
* providing a **clean reproducible installation pipeline**
* integrating the system into a **Flask-based application**
* adding documentation for **Unreal Engine 5 HDRI workflows**
* supporting the experimental pipeline described in the research paper:

**“Music-Driven Worldbuilding: Audio-Reactive VR Environments Using Multimodal Generative AI”**
(EVA London 2026)

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

