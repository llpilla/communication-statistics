# This code has been tested with Python 3 only
# Python 2 could generate problems with the division using integers
import numpy as np

class CommunicationStatistics:
    """
    Class to compute multiple communication metrics/statistics over a given communication matrix
    Statistics considered:
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

    Referenced papers:
    - Diener et al, Performance Evaluation 2015): Matthias Diener, Eduardo HM Cruz, Laércio L. Pilla, Fabrice Dupros, and Philippe OA Navaux. "Characterizing communication and page usage of parallel applications for thread and data mapping." Performance Evaluation 88 (2015): 18-36.
    - Diener et al, Euro-Par 2015: Matthias Diener, Eduardo HM Cruz, Marco AZ Alves, Mohammad S. Alhakeem, Philippe OA Navaux, and Hans-Ulrich Heiss. "Locality and balance for communication-aware thread mapping in multicore systems." In European Conference on Parallel Processing, pp. 196-208. Springer, Berlin, Heidelberg, 2015.
    - Bordage and Jeannot, CCGrid 2018: Cyril Bordage, and Emmanuel Jeannot. "Process Affinity, Metrics and Impact on Performance: an Empirical Study." In 2018 18th IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing (CCGRID), pp. 523-532. IEEE, 2018.
    """

    def __init__(self,csv_file):
        """Reads the communication matrix. Takes a CSV file as argument."""
        self.C = np.genfromtxt(csv_file, delimiter=',')
        # Checking if the matrix has any NaNs
        if np.isnan(self.C).any():
            print("* The communication matrix has NaN values.")
            raise ValueError
        #
        # Checking if there are any negative values
        if np.min(self.C) < 0.:
            print("* The communication matrix contains negative values.")
            raise ValueError
        #
        # Checking if any rows have only zeroes
        if (np.sum(self.C, axis=1) == 0.).any():
            print("* The communication matrix has at least one row with zeroes only.")
            raise ZeroDivisionError
        #
        # Checking if the communication matrix is square
        if self.C.shape[0] != self.C.shape[1]:
            print("* The communication matrix has to be a square.")
            raise ValueError
        # Besides these errors, we should be fine to continue

    def communicationHeterogeneity(self):
        """
        Computes the communication heterogeneity (CH) of a matrix.
        Given M = 100*C/max(C) (normalized matrix),
        CH = (sum_i sum_j ( sum_k(M(i,k))/n - M(i,j) )^2 )/n^2
        It can also be seen as the sum of the variances for each row
        divided by n.
        """
        n = self.C.shape[0]
        M = 100.*self.C/np.max(self.C)   # normalize C
        var_row = np.var(M,axis=1)      # variance pew row
        CH = np.sum(var_row)/n
        return CH

    def CH(self):
        """Check communicationHeterogeneity for information."""
        return self.communicationHeterogeneity()

    def communicationAmount(self):
        """
        Computes the communication amount (CA) of a matrix.
        CA = sum(C)/n^2
        """
        n = self.C.shape[0]
        CA = np.sum(self.C)/(n*n)
        return CA

    def CA(self):
        """Check communicationAmount for information."""
        return self.communicationAmount()

    def communicationBalance(self):
        """
        Computes the communication balance (CB) of a matrix.
        Given T(i) = sum(C(i)),
        CB = (max(T)/(sum_i(T(i))/n) - 1)*100
        """
        n = self.C.shape[0]
        T = np.sum(self.C, axis=1) # computes T
        CB = (n*np.max(T)/np.sum(T) - 1) * 100 # we move 'n' to simplify
        return CB

    def CB(self):
        """Check communicationBalance for information."""
        return self.communicationBalance()

    def communicationCentrality(self):
        """
        Computes the communication centrality (CC) of a matrix.
        Consider, for simplicity, that C(i,j) = 0 if j<0 or j>=n.
        Given a radius r>0 around i such that at least half of the communication
        costs of process i lie within it,
        r_i = argmin_r( sum_j[i-r..i+r]( C(i,j) ) >= sum(C(i))/2 ),
        CC = sum_i( min(i+r_i,n-1) - max(i-r_i,0) )/n^2
        """
        n = self.C.shape[0]
        accum_r = 0.        # value accumulated for each line of C
        for i in range(0,n):
            L = self.C[i]   # line of interest
            half_cost = np.sum(L)/2
            r = 0
            accum = L[i]    # starting value from where we expand
            # Iterate over the line accumulating communication costs
            # until we cover half of its communication cost
            while accum < half_cost:
                r += 1
                # Checks that we are not surpassing the limits of the row
                if i-r >= 0:
                    accum += L[i-r]
                if i+r < n:
                    accum += L[i+r]
            accum_r += min(i+r,n-1) - max(i-r,0)
        CC = accum_r/(n*n)
        return CC

    def CC(self):
        """Check communicationCentrality for information."""
        return self.communicationCentrality()

    def neighborCommunicationFraction(self):
        """
        Computes the neighbor communication fraction (NBC) of a matrix.
        Consider, for simplicity, that C(i,j) = 0 if j<0 or j>=n.
        NBC = 1 - sum_i( C(i,i-1)+C(i,i+1) )/sum(C)
        """
        accum = 0.
        n = self.C.shape[0]
        for i in range(1,n-1): # Ignoring extremes (below 0, above n)
            accum += self.C[i,i-1] + self.C[i,i+1]
        accum += self.C[0,1] + self.C[n-1,n-2] # Last extremes missing
        NBC = 1 - accum/np.sum(self.C)
        return NBC

    def NBC(self):
        """Check neighborCommunicationFraction for information."""
        return self.neighborCommunicationFraction()

    def splitFraction(self,k=2):
        """
        Computes the split fraction for k (SP(k)) of a matrix.
        Takes k as a parameter (default k=2)
        The split fraction is the amount of communication that is done
        around blocks of k × k processes.
        SP(k) = 1 - sum_s[..n/k-1]sum_l[0..k]sum_m[0..k]C(s*k+l,s*k+m)/sum(C)
        """
        accum = 0.
        n = self.C.shape[0]
        if k > 0.:
            for s in range(0,int(n/k)):
                # Adds the values of a sub-matrix with sides of size k
                accum += np.sum(self.C[s*k:(s+1)*k,s*k:(s+1)*k])
        else :
            print("* The value of k has to be greater than zero.")
            raise ValueError
        SP = 1 - accum/np.sum(self.C)
        return SP

    def SP(self,k=1):
        """Check splitFraction for information."""
        return self.splitFraction(k)

    def communicationHeterogeneity_v2(self):
        """
        Computes the communication heterogeneity (CH) of a matrix.
        Given M = C/max(C) (normalized matrix),
        CH = (sum_i sum_j ( sum_k(M(i,k))/n - M(i,j) )^2 )/n^2
        It can also be seen as the sum of the variances for each row
        divided by n.
        """
        n = self.C.shape[0]
        M = self.C/np.max(self.C)       # normalize C
        var_row = np.var(M,axis=1)      # variance pew row
        CH = np.sum(var_row)/n
        return CH

    def CHv2(self):
        """Check communicationHeterogeneity for information."""
        return self.communicationHeterogeneity_v2()

    def communicationBalance_v2(self):
        """
        Computes the communication balance (CB) of a matrix.
        Given T(i) = sum(C(i)),
        CB = 1 - (sum_i(T(i)/n)/max(T)
        """
        n = self.C.shape[0]
        T = np.sum(self.C, axis=1) # computes T
        CB = 1 - np.sum(T)/(n*np.max(T)) # we move 'n' to simplify
        return CB

    def CBv2(self):
        """Check communicationBalance for information."""
        return self.communicationBalance_v2()


