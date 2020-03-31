# This code has been tested with Python 3 only
# Python 2 could generate problems with the division using integers
"""@package commstats
Communication statistics module.
Please check the information on the CommunicationStatistics class for more details.
"""

import numpy as np

class CommunicationStatistics():
    """
    Computes multiple communication metrics/statistics over a given communication matrix.

    Parameters
    ----------
    csv_file : string
        Name of the CSV file containing the communication costs matrix.

    Attributes
    ----------
    costs : np.ndarray
        Communication costs matrix.

    Raises
    ------
    ValueError
        If the matrix contains NaNs, negative values, or if the matrix is not square.
    ZeroDivisionError
        If the matrix contains any rows with zeros only.

    Notes
    -----
    Communication statistics considered:
    - CH: communication heterogeneity (Diener et al, Performance Evaluation 2015)
    - CA: communication amount (Diener et al, Performance Evaluation 2015)
    - CB: communication balance (Diener et al, Euro-Par 2015)
    - CC: communication centrality (Bordage and Jeannot, CCGrid 2018)
    - NBC: neighbor communication fraction (Bordage and Jeannot, CCGrid 2018)
    - SP(k): split fraction (Bordage and Jeannot, CCGrid 2018)
    - CHv2: CH as calculated in (Bordage and Jeannot, CCGrid 2018)
    - CBv2: CB as calculated in (Bordage and Jeannot, CCGrid 2018)

    Notation for comments in the methods:
        C: communication cost matrix (size nxn)
        C(x): line x of C
        C(x,y): value of position x,y of C
        sum_i[1..3]X(i) = X(1)+X(2)+X(3)

    References
    ----------
    - Diener et al, Performance Evaluation 2015): Matthias Diener, Eduardo HM Cruz, Laercio L.
    Pilla, Fabrice Dupros, and Philippe OA Navaux. "Characterizing communication and page usage
    of parallel applications for thread and data mapping." Performance Evaluation 88 (2015): 18-36.
    - Diener et al, Euro-Par 2015: Matthias Diener, Eduardo HM Cruz, Marco AZ Alves, Mohammad S.
    Alhakeem, Philippe OA Navaux, and Hans-Ulrich Heiss. "Locality and balance for
    communication-aware thread mapping in multicore systems." In European Conference on
    Parallel Processing, pp. 196-208. Springer, Berlin, Heidelberg, 2015.
    - Bordage and Jeannot, CCGrid 2018: Cyril Bordage, and Emmanuel Jeannot. "Process Affinity,
    Metrics and Impact on Performance: an Empirical Study." In 2018 18th IEEE/ACM International
    Symposium on Cluster, Cloud and Grid Computing (CCGRID), pp. 523-532. IEEE, 2018.
    """

    def __init__(self, csv_file):
        self.costs = np.genfromtxt(csv_file, delimiter=',')
        # Checking if the matrix has any NaNs
        if np.isnan(self.costs).any():
            print("* The communication matrix has NaN values.")
            raise ValueError
        #
        # Checking if there are any negative values
        if np.min(self.costs) < 0.:
            print("* The communication matrix contains negative values.")
            raise ValueError
        #
        # Checking if any rows have only zeroes
        if (np.sum(self.costs, axis=1) == 0.).any():
            print("* The communication matrix has at least one row with zeroes only.")
            raise ZeroDivisionError
        #
        # Checking if the communication matrix is square
        if self.costs.shape[0] != self.costs.shape[1]:
            print("* The communication matrix has to be a square.")
            raise ValueError
        # Besides these errors, we should be fine to continue

    def communication_heterogeneity(self):
        """
        Computes the communication heterogeneity (CH) of a matrix.

        Returns
        -------
        np.float64
            Communication heterogeneity value.

        Notes
        -----
        Given M = 100*C/max(C) (normalized matrix),
        CH = (sum_i sum_j ( sum_k(M(i,k))/n - M(i,j) )^2 )/n^2
        It can also be seen as the sum of the variances for each row
        divided by n.
        """
        dim = self.costs.shape[0]
        norm_costs = 100.*self.costs/np.max(self.costs)   # normalize C
        var_row = np.var(norm_costs, axis=1)      # variance pew row
        stats = np.sum(var_row)/dim
        return stats

    def ch(self):   # pylint: disable=invalid-name
        """
        Short-hand for communication_heterogeneity.

        See Also
        --------
        communication_heterogeneity : Computes the communication heterogeneity of a matrix.
        """
        return self.communication_heterogeneity()

    def communication_amount(self):
        """
        Computes the communication amount (CA) of a matrix.

        Returns
        -------
        np.float64
            Communication amount value.

        Notes
        -----
        CA = sum(C)/n^2
        """
        dim = self.costs.shape[0]
        stats = np.sum(self.costs)/(dim**2)
        return stats

    def ca(self):   # pylint: disable=invalid-name
        """
        Short-hand for communication_amount.

        See Also
        --------
        communication_amount : Computes the communication amount of a matrix.
        """
        return self.communication_amount()

    def communication_balance(self):
        """
        Computes the communication balance (CB) of a matrix.

        Returns
        -------
        np.float64
            Communication balance value.

        Notes
        -----
        Given T(i) = sum(C(i)),
        CB = (max(T)/(sum_i(T(i))/n) - 1)*100
        """
        dim = self.costs.shape[0]
        row_sums = np.sum(self.costs, axis=1) # computes T
        stats = (dim*np.max(row_sums)/np.sum(row_sums) - 1) * 100 # we move 'n' to simplify
        return stats

    def cb(self):   # pylint: disable=invalid-name
        """
        Short-hand for communication_balance.

        See Also
        --------
        communication_balance : Computes the communication balance of a matrix.
        """
        return self.communication_balance()

    def communication_centrality(self):
        """
        Computes the communication centrality (CC) of a matrix.

        Returns
        -------
        np.float64
            Communication centrality value.

        Notes
        -----
        Consider, for simplicity, that C(i,j) = 0 if j<0 or j>=n.
        Given a radius r>0 around i such that at least half of the communication
        costs of process i lie within it,
        r_i = argmin_r( sum_j[i-r..i+r]( C(i,j) ) >= sum(C(i))/2 ),
        CC = sum_i( min(i+r_i,n-1) - max(i-r_i,0) )/n^2
        """
        dim = self.costs.shape[0]
        accum_r = 0.        # value accumulated for each line of C
        for i in range(0, dim):
            row = self.costs[i]   # line of interest
            half_cost = np.sum(row)/2
            radius = 0
            accum = row[i]    # starting value from where we expand
            # Iterate over the line accumulating communication costs
            # until we cover half of its communication cost
            while accum < half_cost:
                radius += 1
                # Checks that we are not surpassing the limits of the row
                if i-radius >= 0:
                    accum += row[i-radius]
                if i+radius < dim:
                    accum += row[i+radius]
            accum_r += min(i+radius, dim-1) - max(i-radius, 0)
        stats = accum_r/(dim**2)
        return stats

    def cc(self):   # pylint: disable=invalid-name
        """
        Short-hand for communication_centrality.

        See Also
        --------
        communication_centrality : Computes the communication centrality of a matrix.
        """
        return self.communication_centrality()

    def neighbor_communication_fraction(self):
        """
        Computes the neighbor communication fraction (NBC) of a matrix.

        Returns
        -------
        np.float64
            Neighbor communication fraction value.

        Notes
        -----
        Consider, for simplicity, that C(i,j) = 0 if j<0 or j>=n.
        NBC = 1 - sum_i( C(i,i-1)+C(i,i+1) )/sum(C)
        """
        accum = 0.
        dim = self.costs.shape[0]
        for i in range(1, dim-1): # Ignoring extremes (below 0, above n)
            accum += self.costs[i, i-1] + self.costs[i, i+1]
        accum += self.costs[0, 1] + self.costs[dim-1, dim-2] # Last extremes missing
        stats = 1 - accum/np.sum(self.costs)
        return stats

    def nbc(self):   # pylint: disable=invalid-name
        """
        Short-hand for neighbor_communication_fraction.

        See Also
        --------
        neighbor_communication_fraction : Computes the neighbor communication fraction of a matrix.
        """
        return self.neighbor_communication_fraction()

    def split_fraction(self, k: int = 2):
        """
        Computes the split fraction for k (SP(k)) of a matrix.

        Parameters
        ----------
        k : int, optional
            Size of the sub-matrix considered (default = 2).

        Returns
        -------
        np.float64
            Split fraction value.

        Raises
        ------
        ValueError
            If the value of k is smaller than 1.

        Notes
        -----
        The split fraction is the amount of communication that is done
        around blocks of k * k processes.
        SP(k) = 1 - sum_s[..n/k-1]sum_l[0..k]sum_m[0..k]C(s*k+l,s*k+m)/sum(C)
        """
        accum = 0.
        dim = self.costs.shape[0]
        if k > 0.:
            for s in range(0, int(dim/k)): # pylint: disable=invalid-name
                # Adds the values of a sub-matrix with sides of size k
                accum += np.sum(self.costs[s*k:(s+1)*k, s*k:(s+1)*k])
        else:
            print("* The value of k has to be greater than zero.")
            raise ValueError
        stats = 1 - accum/np.sum(self.costs)
        return stats

    def sp(self, k: int = 2):   # pylint: disable=invalid-name
        """
        Short-hand for split_fraction.

        See Also
        --------
        split_fraction : Computes the split fraction of a matrix.
        """
        return self.split_fraction(k)

    def communication_heterogeneity_v2(self):
        """
        Computes the communication heterogeneity (CH) of a matrix with a different formula.

        Returns
        -------
        np.float64
            Communication heterogeneity value.

        Notes
        -----
        Given M = C/max(C) (normalized matrix),
        CH = (sum_i sum_j ( sum_k(M(i,k))/n - M(i,j) )^2 )/n^2
        It can also be seen as the sum of the variances for each row
        divided by n.
        """
        dim = self.costs.shape[0]
        norm_costs = self.costs/np.max(self.costs)       # normalize C
        var_row = np.var(norm_costs, axis=1)      # variance pew row
        stats = np.sum(var_row)/dim
        return stats

    def ch_v2(self):   # pylint: disable=invalid-name
        """
        Short-hand for communication_heterogeneity_v2.

        See Also
        --------
        communication_heterogeneity_v2 : Computes the communication heterogeneity of a matrix.
        """
        return self.communication_heterogeneity_v2()

    def communication_balance_v2(self):
        """
        Computes the communication balance (CB) of a matrix with a different formula.

        Returns
        -------
        np.float64
            Communication balance value.

        Notes
        -----
        Given T(i) = sum(C(i)),
        CB = 1 - (sum_i(T(i)/n)/max(T)
        """
        dim = self.costs.shape[0]
        row_sums = np.sum(self.costs, axis=1) # computes T
        stats = 1 - np.sum(row_sums)/(dim*np.max(row_sums)) # we move 'n' to simplify
        return stats

    def cb_v2(self):   # pylint: disable=invalid-name
        """
        Short-hand for communication_balance_v2.

        See Also
        --------
        communication_balance_v2 : Computes the communication balance of a matrix.
        """
        return self.communication_balance_v2()
