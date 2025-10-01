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