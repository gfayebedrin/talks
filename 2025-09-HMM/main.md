# HMM-RBMs

<img src="figures/hmm1.svg" style="width: 90%; height: auto; display: block; margin: auto;" />

--

Each state $s$ is represented by one $ \mathbf{h}^s $

Note: there are M hidden vectors

--

<img src="figures/hmm2.svg" style="width: 90%; height: auto; display: block; margin: auto;" />

Note: HMM parametrized by $S \times S$ matrix and $S \times M$ vectors

--

<img src="figures/hmm_h_space.svg" style="width: 90%; height: auto; display: block; margin: auto;" />

---

# ARTR
N=500, M=2, S=3

![](figures/ARTR_latent_S3.png)

Note: 
ARTR (500 neurons), M=2 donc plottable, S=3  
clusterisation qui prend en compte la dynamique

---

# Brain slice
N=8000, M=20, S=5

Training time: 15 min

--

![](figures/slice_S5_maps.png)

--

<video controls>
  <source src="figures/slice_S5_data_rec.mp4" type="video/mp4">
</video>

--

<img src="figures/slice_S5_moments.png" style="width: 40%; height: auto; display: block; margin: auto;" />

---

# Whole brain
N=50k, M=100, S=8

Training time: 1h30

--

<img src="figures/whole_brain_slice_S8_maps.png" style="width: 80%; height: auto; display: block; margin: auto;" />

--

<video controls>
  <source src="figures/whole_brain_slice_S8_activity_with_viterbi_states.mp4" type="video/mp4">
</video>

--

<img src="figures/whole_brain_S8_state_frequencies.png" style="width: 100%; height: auto; display: block; margin: auto;" />

---

# About entropy

$$ S(t) = -\sum_s P(s, t) \ln P(s, t) $$

--

$$ \frac{\mathrm dS}{\mathrm dt} = \sigma_\text{irr} - \sigma_\text{env} $$

$$ \sigma_\text{irr} = \frac{1}{2} \sum_{s,s'} [P(s,t)T_{ss'} - P(s',t)T_{s's}] \ln \frac{P(s,t)T_{ss'}}{P(s',t)T_{s's}} $$

$$ \sigma_\text{env} = \left\langle \sum_{s'} T_{ss'} \ln \frac{T_{ss'}}{T_{s's}} \right\rangle_{P(s,t)} $$

Note:
Obtained with master equation  
$\sigma_\text{irr}$ is deviation from detailed balance  
$\sigma_\text{env}$ is KL divergence between forward and backward trajectories $\geq 0$

--

In steady state ($\dot S = 0$),  
entropy production quantifies irreversibility

--

Not to confuse with entropy rate $$ \rho = -\frac{1}{T} \sum_{X \in \text{sequences}} P(X) \ln P(X) $$ which measures randomness of sequences.

--

![](figures/whole_brain_entropy_production.png)

Note: can't really interpret the value itself, but can compare

N=32 : either an artifact / noise, or the model did pick up some irreversibility with 32 states that were not accessible with 16 or 8

--

![](figures/whole_brain_flux_histogram.png)

--

![](figures/whole_brain_flux_histogram_norm.png)

Note: 32 more spread out, consistent with increased entropy production

---

# Remaining work

- More than one $\mathbf{h}^s$ per $s$
  ![](figures/ARTR_S3_K2_hspace.png)
- Multifish ($\to$ geometrical comparison between individuals)