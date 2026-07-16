# Bimetallic \(Au_xFe_y\) (\(x + y = 6\)) Clusters as Catalysts in the Oxidation of Methane, by Hydrogen Peroxide, for the \(\mathrm{CH}_3\mathrm{OH}\) Synthesis

This repository hosts the data structures, computational workflows, and analytical pipelines developed during my postdoctoral research. The project focuses on modeling the synergistic catalyst architecture of subnanometric gold-iron clusters for selective methane-to-methanol conversion using hybrid Density Functional Theory (DFT) and structural optimization algorithms.

---

## 📂 Repository Architecture

```text
methane-catalyst-optimization/
├── data/
│   ├── adsorption_structural_descriptors.csv  # Intermetallic bounds & molecule redshift frequencies
│   ├── cluster_reactivity_descriptors.csv     # Quantum electronic core descriptors (VIP, VEA, GAPs)
│   ├── energies.csv                           # Calculated potential energy surface raw files
│   ├── energies_b.csv                         # Ground state spin state multi-structures data
│   ├── Energies_d.csv                         # Zero-point energy corrections calculations
│   ├── datos_quimicos.db                      # Relational SQLite DB hosting full raw geometries
│   ├── resultados_quimica_limpios.db          # Clean SQL tables for production modeling
│   └── mis_logs.db                            # Convergence traces and execution step logs
├── scripts/
│   ├── main.py                                # Master entrypoint for calculation parsers
│   ├── eda_catalyst_properties.py             # Electronic tuning & peroxide linear regression EDA
│   └── population_fitness.py                  # Stochastic initial guess 3D coordinate generator
├── outputs/
│   ├── correlation_matrix.png                 # Saved matrix plot (H2O2 focus)
│   ├── peroxide_linear_regression.png         # Saved backdonation trend scatter-fit
│   ├── Figure_1.png                           # Gas-phase reference diagram
│   ├── Figure_2.png                           # Catalytic mechanism flowchart
│   ├── Figure_3.png                           # Cluster ground-state geometries
│   ├── Figure_4.png                           # Electrostatic potential maps
│   ├── Figure_5.png                           # Reactant adsorption configurations
│   ├── Figure_6.png                           # Elongation & spectrographic trends
│   ├── Figure_7.png                           # Radical activation barriers
│   └── Figure_8.png                           # Transition states & C-O coupling coordinate
└── README.md                                  # Main Documentation Portfolio Portada
```

---

## 📑 Manuscript Content & Abstract

### Abstract
The adsorption and activation of $\mathrm{CH}_4$ and $\mathrm{H}_2\mathrm{O}_2$ molecules over bimetallic $Au_xFe_y$ clusters ($x + y = 6$) for $\mathrm{CH}_3\mathrm{OH}$ formation were studied in the gas phase through the $\mathrm{H}_3\mathrm{C–H} \rightarrow \bullet\mathrm{CH}_3 + \bullet\mathrm{H}$ and $\mathrm{HO–OH} \rightarrow 2\bullet\mathrm{OH}$ bond cleavage processes. Density functional theory (DFT) calculations were performed using the PBE0 functional with the LANL2DZ effective core potential for $Au$ atoms and the Def2TZVP all-electron basis set for $Fe$ and organic atoms. From planar $Au_6$ and $Au_5Fe$ ground state (GS) structures, distorted and compact three-dimensional GS’s forms appear for $Au_2Fe_4$, $Au_3Fe_3$, $Au_2F_4$, $Au_1Fe_5$ and $Fe_6$. 

Charge transfer occurs from $Fe$ to $Au$, thereby favoring the $Fe_y$ sites for nucleophilic $\mathrm{CH}_4/\mathrm{H}_2\mathrm{O}_2$ attacks. Our results show that the whole $\mathrm{CH}_4 + \mathrm{H}_2\mathrm{O}_2 \rightarrow \mathrm{CH}_3\mathrm{OH}$ reaction, in the presence of $Au_xFe_y$ clusters, is clearly spontaneous, since the change of the free energy reaction reaches $\Delta G_{\text{react}} = -2.841\text{ eV}$ in $Au_4Fe_2$. The primary catalytic effect of $Au_xFe_y$ lies in lowering the radical formation energy from $19.60\text{ eV}$ in the gas phase to only $0.227\text{ eV}$ for the 1:1 Au:Fe composition. Computed reaction barriers for the $Au_xFe_y–\mathrm{HO}\bullet + \bullet\mathrm{CH}_3$ coupling step range from $1.349$ to $-0.269\text{ eV}$, indicating a highly favorable pathway. Among all stoichiometries, the $Au_3Fe_3$ shows the most pronounced total catalytic enhancement, highlighting the $Au/Fe$ synergistic role in promoting methane oxidation.

---

### 1. Introduction
Anthropogenic global warming is an undeniable reality, and developing strategies to convert methane into value-added products like methanol is crucial. Subnanometric gold clusters display unexpected catalytic activity arising from quantum size effects and low-coordination surface atoms, while iron clusters provide rich electronic/magnetic profiles ideal for redox reactions. Bimetallic architectures merge these features via structural stabilization, charge redistribution, and spin polarization. This work deciphers the geometric, electronic, and spin-state rules of $Au_xFe_y$ series optimizing targeted $\mathrm{CH}_4$ conversion under mild conditions.

---

### 2. Methodology
* **Initial Sampling Engine (`population_fitness.py`):** Implements a customized stochastic algorithm creating un-optimized atomic geometries in a bounded $6\text{ Å}$ cubic box to bypass structural stagnation in computational workflows.
* **Theory Level:** Gas-phase optimization using the hybrid functional **PBE0** (25% Hartree–Fock exchange). Relativistic effective core potentials (**LANL2DZ**) for $Au$, and triple-$\zeta$ **Def2TZVP** all-electron basis sets for $Fe, C, O, H$.
* **Energy Evaluation:** ZPVE corrections calculated with harmonic frequencies. Transition states ($TS$) verified using synchronous transit-guided quasi-Newton (**STQN/QST2**) routines coupled with the Berny optimization engine.
* **Data Persistence Engine:** Relational databases (`.db` files) store geometric structures, ionization traces (`vip_ev`, `vea_ev`), and convergence parameters via automated SQL transaction scripts.

---

### 3. Results and Discussion

#### 3.1 Reaction Scheme and Catalytic Strategy
In the absence of a catalyst, methane homolytic cracking demands an unfeasible energy envelope of $5.98\text{ eV}$. The introduction of the cluster surface triggers a 6-step mechanism to drop these constraints: (1) Adsorption, (2) Homolytic radical cleavage, (3) Methyl desorption/$\mathrm{H}_2\mathrm{O}$ yield, (4) Radical-coupling $TS$ acquisition, (5) Methanol creation, and (6) Catalytic release.
* **Figure 1:** Reaction steps for the formation of methanol from methane oxidation (Gas-phase control).
* **Figure 2:** Proposed 6-step radical-mediated pathway over $Au_xFe_y$ surface clusters to produce methanol.

#### 3.2 Cluster Properties
* **Geometry (Figure 3):** Ground state forms transition systematically from planar $Au_6$ configurations to highly packed, low-symmetry $3\mathrm{D}$ arrangements for iron-rich regimes.
* **Charge Polarization (Figure 4):** NBO parameters prove a steady intramolecular charge transfer from $Fe \rightarrow Au$, transforming the iron nodes into electron-deficient environments ideal for coordination.

#### 3.3 Catalytic Process: \(\mathrm{CH}_4 + \mathrm{H}_2\mathrm{O}_2 \xrightarrow{Au_xFe_y} \mathrm{CH}_3\mathrm{OH}\)
* **Adsorption Trends (Figure 5 & 6):** Reactants attach strongly to $Fe$ nodes, driving a significant stretching elongation of organic bonds coupled with red-shifts on vibration states.

#### 3.4 Radical Formation & 3.5 C-O Coupling
* **Figure 7:** Energetic activation barriers showing a dramatic drop in dissociation energy down to $0.18\text{ eV}$ for equiatomic allocations.
* **Figure 8 (Linear Profile & Table):** Transition states tracking the actual $\mathrm{C-O}$ bond assembly. This visualization handles the accumulated coordinate trajectory profiles.

---

### 4. Conclusions
* Bimetallic allocations govern the structural, magnetic, and electronic transitions of the active surface.
* $Fe$-heavy distributions maximize intermediate capture but introduce structural distortions, while $Au$-heavy configurations restrict reactant initialization.
* **The Equiatomic Optimum:** $Au_3Fe_3$ provides the lowest effective barriers by merging coordinate flexibility, polarization fields, and clean catalytic desorption.

---

## 🛠️ Replication & Execution

```bash
# Install environment drivers
pip install pandas matplotlib seaborn numpy scipy

# Execute the stochastic cluster geometry modeler
python scripts/population_fitness.py

# Run the Free Energy Profile pipeline (Figure 8 Generator)
python scripts/main.py

# Execute Peroxide Tuning exploratory regression models
python scripts/eda_catalyst_properties.py
```
