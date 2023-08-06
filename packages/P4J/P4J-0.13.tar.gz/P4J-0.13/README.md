# P4J

**Description** 

P4J is a python package for periodicity analysis of irregularly sampled time series based on Information Theoretic objective functions. P4J was developed for astronomical light curves, irregularly sampled time series of stellar magnitude or flux. These routines are build on the concept of **correntropy** [1], a generalized correlation function that incorporates higher order statistics of the process, lifting the assumption of Gaussianity. Correntropy has been used in astronomical time series problems in [2, 4].

**Contents**

- Regression using the Weighted Maximum Correntropy Criterion (WMCC) and Weighted Minimum Error Entropy (WMEE) criterion
- Robust periodogram based on WMCC and WMEE
- Conventional periodogram based on least squares (OLS) and weighted least squares (WLS)
- False alarm probability for periodogram peaks based on extreme value statistics
- Basic synthetic light curve generator

**Instalation**

```
pip install P4J
```

**Example**

https://github.com/phuijse/P4J/blob/master/examples/periodogram_demo.ipynb
https://github.com/phuijse/P4J/blob/master/examples/regression_demo.ipynb

**TODO**

- Cython backend for WMCC and WMEE
- Multidimensional time series support


**Authors** 

- Pablo Huijse <pablo.huijse@gmail.com> (Millennium Institute of Astrophysics and Universidad de Chile)
- Pavlos Protopapas (Harvard Institute of Applied Computational Sciences)
- Pablo A. Estévez (Millennium Institute of Astrophysics and Universidad de Chile)
- Pablo Zegers (Universidad de los Andes, Chile)
- José C. Príncipe (University of Florida)

(P4J = Four Pablos and one Jose)

**References**

1. José C. Príncipe, "Information Theoretic Learning: Renyi's Entropy and Kernel Perspectives", Springer, 2010
2. Pavlos Protopapas et al., "A Novel, Fully Automated Pipeline for Period Estimation in the EROS 2 Data Set", The Astrophysical Journal Supplement, 216 (2), 2015
3. Pablo Huijse et al., "Computational Intelligence Challenges and Applications on Large-Scale Astronomical Time Series Databases", IEEE Mag. Computational Intelligence, 2014
4. Pablo Huijse et al., "An Information Theoretic Algorithm for Finding Periodicities in Stellar Light Curves", IEEE Trans. Signal Processing 60(10), pp. 5135-5145, 2012


