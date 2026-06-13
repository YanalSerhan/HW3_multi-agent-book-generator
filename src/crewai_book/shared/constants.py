"""Immutable project-wide constants."""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATE_DIR = PROJECT_ROOT / "src" / "crewai_book" / "latex" / "templates"

# Setup the main output directory
OUTPUT_DIR = Path("output").resolve()

# Fallback missing bibliography entries for seminal VAE/Diffusion papers
MISSING_BIB = r"""
@article{kingma2014autoencoding,
  title={Auto-Encoding Variational Bayes},
  author={Kingma, Diederik P and Welling, Max},
  journal={ICLR},
  year={2014}
}
@article{higgins2017beta,
  title={beta-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework},
  author={Higgins, Irina and Matthey, Loic and Pal, Arka and Burgess, Christopher and Glorot, Xavier and Botvinick, Matthew and Mohamed, Shakir and Lerchner, Alexander},
  journal={ICLR},
  year={2017}
}
@article{sonderby2016ladder,
  title={Ladder Variational Autoencoders},
  author={S{\o}nderby, Casper Kaae and Raiko, Tapani and Maal{\o}e, Lars and S{\o}nderby, S{\o}ren Kaae and Winther, Ole},
  journal={NeurIPS},
  year={2016}
}
@article{tomczak2017vae,
  title={VAE with a VampPrior},
  author={Tomczak, Jakub M and Welling, Max},
  journal={AISTATS},
  year={2018}
}
@article{ho2020denoising,
  title={Denoising Diffusion Probabilistic Models},
  author={Ho, Jonathan and Jain, Ajay and Abbeel, Pieter},
  journal={NeurIPS},
  year={2020}
}
@article{song2020denoising,
  title={Denoising Diffusion Implicit Models},
  author={Song, Jiaming and Meng, Chenlin and Ermon, Stefano},
  journal={ICLR},
  year={2021}
}
@article{song2019generative,
  title={Generative Modeling by Estimating Gradients of the Data Distribution},
  author={Song, Yang and Ermon, Stefano},
  journal={NeurIPS},
  year={2019}
}
@article{nichol2021improved,
  title={Improved Denoising Diffusion Probabilistic Models},
  author={Nichol, Alexander Quinn and Dhariwal, Prafulla},
  journal={ICML},
  year={2021}
}
@article{ramesh2022hierarchical,
  title={Hierarchical Text-Conditional Image Generation with CLIP Latents},
  author={Ramesh, Aditya and Dhariwal, Prafulla and Nichol, Alex and Chu, Casey and Chen, Mark},
  journal={arXiv preprint arXiv:2204.06125},
  year={2022}
}
@article{saharia2022photorealistic,
  title={Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding},
  author={Saharia, Chitwan and Chan, William and Saxena, Saurabh and Li, Lala and Whang, Jay and Denton, Emily and Ghasemipour, Seyed Kamyar Seyed and Ayan, Burcu Karagol and Cer, Daniel and Boston, Sara and others},
  journal={NeurIPS},
  year={2022}
}
@article{bowman2016generating,
  title={Generating Sentences from a Continuous Space},
  author={Bowman, Samuel R and Vilnis, Luke and Vinyals, Oriol and Dai, Andrew M and Jozefowicz, Rafal and Bengio, Samy},
  journal={arXiv preprint arXiv:1511.06349},
  year={2016}
}
"""

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Quality Gates
MIN_VERIFIED_SOURCES = 10
MAX_CRITICAL_HALLUCINATIONS = 0
MIN_READABILITY_FLESCH = 60.0
MIN_PDF_PAGES = 15

# Timeouts & Retries
DEFAULT_API_TIMEOUT = 45.0
DEFAULT_MAX_RETRIES = 3

# Document Settings
DEFAULT_DOCUMENT_CLASS = "memoir"
DEFAULT_BIB_STYLE = "apa"
