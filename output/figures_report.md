List of Generated Figures:

1. **Filename:** diffusion_process_comparison.png  
   **Caption:**  
   *Comparison of Forward SDE, Reverse SDE, and Probability Flow ODE in diffusion models.*  
   This figure visually summarizes the mathematical forms, purposes, and qualitative sampling complexities of the three key stochastic/deterministic processes underlying diffusion-based generative modeling. The Forward SDE represents the data noising step. The Reverse SDE implements generative sampling with stochastic noise guided by score functions. The Probability Flow ODE offers a deterministic alternative with typically lower sampling complexity. The equations are displayed alongside purposes and complexity levels to aid conceptual understanding.

2. **Filename:** noise_schedules.png  
   **Caption:**  
   *Noise scheduling schemes employed in score-based diffusion models.*  
   This chart illustrates typical continuous noise schedules used to condition neural networks for score matching, including linear, cosine, and sigmoid schedules. Noise level is plotted as a function of diffusion time \(t\). Different scheduling shapes impact the training stability and sample quality in diffusion models. Understanding these schedules informs design choices for noise conditioning and multi-scale training strategies.

3. **Filename:** sampling_steps_quality_tradeoff.png  
   **Caption:**  
   *Trade-off between the number of sampling steps and sample quality across popular score-based generative methods.*  
   The figure plots hypothetical sample quality against the number of sampling steps required, comparing DDPM, Score SDE, and Probability Flow ODE sampling approaches. It demonstrates that fewer sampling steps often correlate with reduced computational cost but may affect sample quality. The Probability Flow ODE method achieves relatively high quality with fewer steps due to deterministic evolution, highlighting efficiency gains in practical diffusion model deployment.

---

These professional figures enhance comprehension of core diffusion model concepts by visualizing mathematical differences, training design choices, and practical sampling trade-offs. They are saved as high-quality PNG files suitable for academic publication and presentation.