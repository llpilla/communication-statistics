# Communication Statistics scripts/module/library

These Python 3 scripts can be used to compute communication statistics over communication graphs stored as CSV files. For more information about these statistics and their use, please check the [references below](#references). For the specific methods available, check their [list below](#statistics).

This software is made available using the CeCILL-C license. Check the [LICENSE](LICENSE) file for more information.

## Dependencies

We use modules numpy, unittest, and sys in our code. If anything is missing, please use `pip3 install` to install it. 

## How to use

### As a script

Run `run_stats.py` with the communication matrix CSV files as arguments

Example:

```console
$ ./run_stats.py tests/all_1s.csv
```
or
```console
$ python3 run_stats.py tests/all_1s.csv
```

### As a Python module/class

Use `import commstats` or `from commstats import CommunicationStatistics` inside Python 3.

Example:

```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
print('CA = ', mycomm.ca())
```

## How to test

Run `unittest.sh` to run unit tests.

```console
$ ./unittest.sh
```

The directory [bad\_matrices](bad\_matrices/) contains some CSV files that should raise exceptions in the code.

---

## Statistics

All the communication statistics computed by the script were previously proposed in scientific papers. Please check them if you want to understand them better.

Below you can find some notation information to help you understand the statistics. 
They are computed over a communication cost matrix representing the communication graph of the application. 
These costs can be the number of messages or the data volume exchanged, for instance. 
The communication graph must be connected (all rows must have at least one non-zero value).
Negative communication costs are not accepted.

> C: communication cost matrix of dimensions n\*n. Indexes go from 0 to n-1.  
> C(x): row x of C (of size n)  
> C(x,y): element of row x and column y of C  
> Σi C(x,i): sum of all elements of row x (C(x,0)+C(x,1)+...+C(x,n-1))  
> Σi\[1..3\] C(x,i): C(x,1)+C(x,2)+C(x,3)  
> sum(C): sum of all elements of C  
> sum(C(x)): sum of all elements of row x of C  
> max, min, var: maximum, minimum, variance  
> ^2: squared

### CA: Communication Amount \[1\]

Computes the average communication cost of the matrix. Higher values mean that there is more communication happening in the application (the application should benefit more from a careful mapping).

> CA = sum(C) / n^2

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.ca()
mycomm.communication_amount()
```

### CB: Communication Balance \[2\]

Computes the communication balance of the matrix. Higher values mean that the communication is more imbalanced (the application should benefit more from a careful mapping).

> Given T(i) = sum(C(i)),  
> CB = 100 \* (max(T)/(Σi T(i)/n) - 1)

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.cb()
mycomm.communication_balance()
```

### CBv2: Communication Balance as in \[3\]

Computes the communication balance of the matrix. Higher values mean that the communication is more imbalanced (the application should benefit more from a careful mapping).

> Given T(i) = sum(C(i)),  
> CBv2 = 1 - (Σi T(i)/n) / max(T)

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.cb_v2()
mycomm.communication_balance_v2()
```

### CC: Communication Centrality \[3\]

Computes how communication is dispersed from the diagonal. Higher values mean that more communication is off the diagonal (the application should benefit more from a careful mapping).

> Consider, for simplicity, that any values outside a row are equal to 0, i.e.,  
> C(i,j) = 0 if j < 0 or j >= n.  
> Given a radius > 0 around i such at least half of the communication costs of row i lie 
thin it, i.e.,  
> r(i) = argmin r ( Σj\[i-r..i+r\] C(i,j) >= sum(C(i))/2 ),  
> CC = Σi ( min(i+r(i),n-1) - max(i-r(i),0) ) / n^2

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.cc()
mycomm.communication_centrality()
```

### CH: Communication Heterogeneity \[1\]

Computes the communication heterogeneity of the matrix. Higher values mean higher heterogeneity (the application should benefit more from a careful mapping).

> Given the normalized matrix M = 100 \* C/max(C),  
> CH = ΣiΣj ( (Σk M(i,k))/n - M(i,j) )^2 / n^2, or  
> CH = Σi var(M(i)) / n

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.ch()
mycomm.communication_heterogeneity()
```

### CHv2: Communication Heterogeneity as in \[3\]

Computes the communication heterogeneity of the matrix. Higher values mean higher heterogeneity (the application should benefit more from a careful mapping).

> Given the normalized matrix M = C/max(C),  
> CHv2 = ΣiΣj ( (Σk M(i,k))/n - M(i,j) )^2 / n^2, or  
> CHv2 = Σi var(M(i)) / n

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.ch_v2()
mycomm.communication_heterogeneity_v2()
```

### NBC: Neighbor Communication Fraction \[3\]

Computes the fraction of communication that is done between ranking neighbors.
Higher values mean that more communication is done with others besides neighbors (the application should benefit more from a careful mapping).

> Consider, for simplicity, that any values outside a row are equal to 0, i.e.,  
> C(i,j) = 0 if j < 0 or j >= n.  
> NBC = 1 - Σi ( C(i,i-1) + C(i,i+1) ) / sum(C)

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.nbc()
mycomm.neighbor_communication_fraction()
```

### SP(k): Split Fraction \[3\]

Computes the fraction of communication that happens among elements in k\*k blocks.
Higher values mean that more communication happens outside these blocks (the application should benefit more from a careful mapping).

> SP(k) = 1 - Σs\[0..n/k-1\] Σl\[0..k] Σm\[0..k\] C(s\*k+l,s\*k+m) / sum(C)

Use:
```python
from commstats import CommunicationStatistics
mycomm = CommunicationStatistics('tests/all_1s.csv')
mycomm.sp(4)
mycomm.split_fraction(4)
```

---

## References

1. Matthias Diener, Eduardo HM Cruz, Laércio L. Pilla, Fabrice Dupros, and Philippe OA Navaux. "Characterizing communication and page usage of parallel applications for thread and data mapping." Performance Evaluation 88 (2015): 18-36. [Online](https://doi.org/10.1016/j.peva.2015.03.001)
2. Matthias Diener, Eduardo HM Cruz, Marco AZ Alves, Mohammad S. Alhakeem, Philippe OA Navaux, and Hans-Ulrich Heiss. "Locality and balance for communication-aware thread mapping in multicore systems." In European Conference on Parallel Processing, pp. 196-208. Springer, Berlin, Heidelberg, 2015. [Online](https://doi.org/10.1007/978-3-662-48096-0_16)
3. Cyril Bordage, and Emmanuel Jeannot. "Process Affinity, Metrics and Impact on Performance: an Empirical Study." In 2018 18th IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing (CCGRID), pp. 523-532. IEEE, 2018. [Online](https://doi.org/10.1109/CCGRID.2018.00079)


