# Generative models describe spontaneous brain dynamics across timescales

19/05/2026

---

## Whole-brain imaging in larval zebrafish

<div style="position:relative; width:920px; height:520px; margin:0 auto;">
  <div class="r-svg-layers" data-src="figures/intro/fluo_annotated.svg" data-base="Layer 1" style="position:absolute; left:-0.7%; top:22.6%; width:34.84%; height:66%; overflow:hidden; box-sizing:border-box;"></div>
  <div class="fragment" style="position:absolute; left:33.1%; top:14.8%; width:25.89%; height:85.09%; overflow:hidden; box-sizing:border-box;"><video data-autoplay loop muted data-src="figures/intro/LSM.mp4" style="max-width:100%; max-height:100%;"></video></div>
  <div class="r-svg-layers fragment" data-src="figures/intro/fluo_diag.svg" data-base="Layer 1" style="position:absolute; left:58.3%; top:26.9%; width:40.42%; height:61.11%; overflow:hidden; box-sizing:border-box;"></div>
</div>

Footnote:
Wolf et al. (2015, *Nature Methods*), Panier et al. (2023)

Note:
- Whole-brain light-sheet imaging of larval zebrafish, pan-neuronal GCaMP
- fluorescence → deconvolved / binarized events → ~50 k-neuron raster
- ~50 000 neurons, 30 min @ 2.5 Hz, 6 fish

---

## Spontaneous activity is structured

<img src="figures/intro/SA_def.svg" style="width:80%; display:block; margin:14px auto;" />

<video data-autoplay loop muted data-src="figures/intro/Movie1.mp4" style="max-height:560px; width:auto; display:block; margin:10px auto;"></video>

Note:
- Not noise: structured, metabolically expensive (~20% of energy budget)
- Constrains how the brain responds to stimuli
- We model the distribution P(v) of brain configurations (Boltzmann) → next: RBMs
- **Goal**: find a common temporal organization across individuals

---

## Restricted Boltzmann Machines

<div class="r-svg-layers" data-src="figures/intro/rbm_explanation.svg" data-steps="Layer 1,Layer 2 ; Layer 1,Layer 3,Layer 4 ; Layer 1,Layer 3,Layer 5 ; Layer 1,Layer 6,Layer 7 ; Layer 7,Layer 8" style="width:100%; margin:30px auto;"></div>

Footnote: Van der Plas et al. (2023, *eLife*)

Note:
- Defined as $1 \ll m \ll M$ where $m(t)$ is number of active HUs
- $M \sim 10^2$
- Compositional phase:
  - double-reLU hidden potential
  - $L_1$ regularization on the weights (sparse)
  - Variance of HUs =1, average =0

---

## RBMs reveal cell assemblies

<div style="display:flex; justify-content:center;">
  <div style="position:relative; width:94%;">
    <img src="figures/intro/diag_complex.svg" style="width:100%; height:auto; display:block;" />
    <div style="position:absolute; left:1.5%; bottom:1.5%; display:flex; gap:16px; align-items:flex-end;">
      <figure style="margin:0;"><img src="https://research.wur.nl/files-asset/126634744/GetMedia.ashx_id_123483_ts_1743673080?w=160&f=jpg" style="width:128px; border-radius:8px;" /><figcaption style="font-size:0.42em;">Thijs van der Plas</figcaption></figure>
      <figure style="margin:0;"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd5M6DoNByKuL3ONCGAu2a3WH3Wke_DdHgPQ&s" style="width:128px; border-radius:8px;" /><figcaption style="font-size:0.42em;">Jérôme Tubiana</figcaption></figure>
    </div>
  </div>
</div>

Footnote: Van der Plas et al. (2023, *eLife*)

Note: RBM weights group co-active neurons into cell assemblies that map onto known functional circuits.

---
## Aligning latent spaces across fish

<div style="display:flex; flex-direction:column; align-items:center;">
  <img src="figures/intro/teacher_student.svg" style="width:82%; height:auto; display:block;" />
  <div style="display:flex; gap:24px; align-items:flex-end; margin-top:8px;">
    <figure style="margin:0;"><img src="https://www.labojeanperrin.fr/Documents/Images/People/101.png" style="width:110px; height:110px; object-fit:cover; border-radius:8px;" /><figcaption style="font-size:0.42em;">Mattéo Dommanget-Kott</figcaption></figure>
    <figure style="margin:0;"><img src="https://www.ipht.fr/wp-content/uploads/2024/09/Jorge.jpeg" style="width:110px; height:110px; object-fit:cover; border-radius:8px;" /><figcaption style="font-size:0.42em;">Jorge Fernández de Cossío Díaz</figcaption></figure>
  </div>
</div>

Footnote: Dommanget-Kott et al. (2026, *PNAS*)

Note: Teacher RBM on fish 1; student RBM on fish 2 aligned to the teacher's latent space ($\lambda=0.5$).

--

![LaRBM](figures/intro/LaRBM.svg)

Footnote: Dommanget-Kott (unpublished)

Note: autocorrelation of hidden units decays after several seconds

---

## A state RBM discretizes the dynamics

![sRBM](figures/sRBM/sRBM.svg)
 
Note:
- a likely state in fish 1 is likely in fish 2
- transitions are not well conserved
Here we cluster, then look at dynamics. Mehta and Schwab: clustering like this is coarse graining, describing the neural activity in terms of a composition of neural assemblies.

One limit of the sRBM: because they must be compositional, state definitions are not independant.

---

## State sequences are Markovian enough

<div style="display:flex; align-items:center; justify-content:center; gap:32px; margin-top:14px;">
  <img src="figures/sRBM/markovianity_I1_vs_S.svg" style="width:47%; height:auto;" />
  <img src="figures/sRBM/markovianity_ck_frobenius_S128.svg" style="width:47%; height:auto;" />
</div>

<p style="text-align:center;">$$\hat I(s_{t+1};\, s_{t-1}\mid s_t) \;=\; \sum_{i,j} \hat P(i,j)\; D_{\mathrm{KL}}\!\left(\hat{\mathcal T}^{(2)}_{ij,\cdot}\,\big\|\,\hat{\mathcal T}_{j,\cdot}\right)$$</p>

Note:
- Observed sequences stay close to the Markov null → dynamics are first-order → an HMM is justified.
- The sRBM assigns each time point a state, giving a discrete state sequence $s_t$.
- **Left — Chapman–Kolmogorov:** $\|\hat{\mathcal T}^{k} - \hat{\mathcal T}^{(k)}\|_F$, the $k$-step matrix predicted from one-step transitions vs. the directly estimated $k$-step matrix. Observed (blue) barely exceeds the Markov null (orange).
- **Right:** conditional MI $\hat I(s_{t+1}; s_{t-1}\mid s_t)$ — exactly 0 for a perfect first-order chain. Small observed–null gap; the growth with $S$ is finite-sample bias (present in the null too).
- Both diagnostics: only a tiny departure from Markovianity ⇒ describing the dynamics with a Hidden Markov Model is justified.

---

## Modeling the dynamics with an HMM

<img src="figures/HMM/hmm1.svg" style="width: 90%; height: auto; display: block; margin: auto;" />

--

## The HMM-RBM

Each state $s$ is represented by one hidden vector $\mathbf{h}^s$

<img src="figures/HMM/hmm2.svg" style="width: 90%; height: auto; display: block; margin: auto;" />

Note: HMM parametrized by $S \times S$ transition matrix and $S$ hidden vectors

--

<div class="r-svg-layers" data-src="figures/HMM/hmm-rbm.svg" data-base="Layer 1" data-include="Layer 2,Layer 3,Layer 4" style="width:82%; margin:20px auto;"></div>
 
Note:
One limit of the sRBM: because they must be compositional, state definitions are not independant.
HMM-RBM states can be defined as any point in latent space.
This results in the RBM-HMM being able to distribute data more evenly between states (higher entropy description).

---

## Per-state dwell times are exponential

<img src="figures/HMM/state-seq.svg" style="width:42%; display:block; margin:6px auto 18px;" />

<!-- Are state dwell times exponentially distributed (pure Markov)? -->

![Per-state dwell time](figures/poster/dwell_times_each_state_exp_fit.svg)
<!-- <img src="figures/poster/dwell_times_each_state_exp_fit.svg" style="width: 85%; height: auto; display: block; margin: auto;" /> -->

Note: P-P plot: plots two CDF against each other

--

## Average dwell times follow a Gamma law

<img src="figures/HMM/state-seq.svg" style="width:42%; display:block; margin:6px auto 18px;" />

<!-- $P(\tau) \propto \tau^{K-1} e^{-\tau/D}$ -->

![Average dwell time](figures/poster/dwell_times_avg_gamma_fit.svg)
![Model agreement](figures/poster/dwell_times_model_emp_agreement.svg)

Note:
Q-Q plot: quantile-quantile  
Histogram computed from data, but very good agreement with transition matrix.

--

## Overall dwell times follow a power law

<img src="figures/HMM/state-seq.svg" style="width:42%; display:block; margin:6px auto 18px;" />

![Overall dwell time](figures/poster/dwell_times_overall_power_fit.svg)

Footnote:
$/\mkern-5mu/$ Ponce-Alvarez et al. (2018, *Neuron*), Wang et al. (2025, *eLife*)



Note: Aggregating across all states: overall dwell time distribution follows a power law. This is consistent with a mixture of exponentials with gamma-distributed timescales — i.e. the brain operates across a continuum of timescales.  

German Sumbre paper: Whole-Brain Neuronal Activity Displays Crackling Noise Dynamics 

Quan Wen: The Geometry and Dimensionality of Brain-wide Activity (sample random subsets of neurons to see what changes with scale, find that the structure of the covariance is scale invariant)

---

# How predictable are the dynamics?

<img src="figures/HMM/predictability.svg" style="width: 80%; height: auto; display: block; margin: auto;"/>

$$\mathrm{BCE} = -\frac{1}{N} \sum_i \left[ v_i \log \tilde v_i + (1-v_i)\log(1-\tilde v_i) \right]$$

Note:
Entropy of super simple case where 1 neuron in 50 is active: 0.1  
Predictability is a good measure of performance  
look at $N$ to see what's best (elbow?)

Prediction time scales logarithmically with $N$

---

## All model sizes share one time-scale distribution

<img src="figures/HMM/eigenvalues_time_distributions.svg" style="width:56%; height:auto; display:block; margin:10px auto;" />


Note:
All model sizes sample the **same** distribution of time scales — its exponential tail makes the largest of $S$ draws grow as $\log S$, so prediction time ∝ $\log S$

- $x$-axis: relaxation time scale $\tau = -1/\ln\lambda$ of each transition-matrix eigenvalue $\lambda$; curve = CDF $P(\tau \le \cdot)$.
- Curves for $S = 2^1 \dots 2^7$ collapse → the underlying time-scale distribution is **size-independent**.
- Extreme-value: the maximum of $S$ i.i.d. draws from a distribution with an exponential tail grows like $\log S$.
- Prediction horizon is set by the slowest surviving mode (largest $\tau$) ⇒ $t_\text{pred} \propto \log S$ — explaining the empirical $\log N$ scaling.

---

## Individuality emerges at finer scales

<img src="figures/HMM/individuality.svg" alt="Individuality" style="width:90%; height:auto; display:block; margin:0 auto;" />

Note:
Gray line = one pair of 2 fish.  
Compare transition matrices.

By describing the data at different scales, we find that the brain operates at diﬀerent time scales: a "slow" global structure, well conserved across individuals, that orchestrates "fast" local computations.

---

# Perspectives

![opto](figures/perspectives/opto.png) <!-- .element: style="width:25%" -->
![manifold](figures/perspectives/perturbation_manifold.jpg) <!-- .element: style="width:50%" -->

Footnote:
Image from Jazayeri & Afraz (2017, *Neuron*)

Note:
- Visual stimuli and optogenetic perturbations: are we still predictive? 
- Optogenetics: can we force the system to go where we want? Luca Mazzucato: perturbation result does not depend on starting point.
