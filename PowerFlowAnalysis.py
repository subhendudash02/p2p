#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np

class PowerFlow:
    def __init__(self, busdata, linedata):
        self.busdata = busdata
        self.linedata = linedata

    def ybusppg(self):
        fb = self.linedata[:, 0]        # From bus number...
        tb = self.linedata[:, 1]        # To bus number...
        r = self.linedata[:, 2]         # Resistance, R...
        x = self.linedata[:, 3]         # Reactance, X...
        b = self.linedata[:, 4]         # Ground Admittance, B/2...
        a = self.linedata[:, 5]         # Tap setting value..

        z = r + 1j * x             # Z matrix...
        y = 1 / z                  # To get inverse of each element...
        b = 1j * b                 # Make B imaginary...

        nb = len(self.busdata)  # Number of buses
        nl = len(fb)                 # no. of branches...
        Y = np.zeros((nb, nb), dtype=complex)  # Initialise YBus...

        # Formation of the Off Diagonal Elements...
        for k in range(nl):
            Y[int(fb[k]) - 1, int(tb[k]) - 1] -= y[k] / a[k]
            Y[int(tb[k]) - 1, int(fb[k]) - 1] = Y[int(fb[k]) - 1, int(tb[k]) - 1]

        # Formation of Diagonal Elements....
        for m in range(nb):
            for n in range(nl):
                if fb[n] == m + 1:
                    Y[m, m] += y[n] / (a[n] ** 2) + b[n]
                elif tb[n] == m + 1:
                    Y[m, m] += y[n] + b[n]

        return Y
    
    
    def powerflow(self, V, del_, BMva):
        Y = self.ybusppg()  # Calling Ybus program (assuming it's defined)
        lined = self.linedata  # Assuming this function is also defined
        busd = self.busdata  # Assuming this function is defined as well
        Vm = V*np.cos(del_) + 1j*V*np.sin(del_)
        Del = np.rad2deg(del_)  # Bus voltage angles in degrees
        fb = lined[:, 0]  # From bus number
        tb = lined[:, 1]  # To bus number
        b = lined[:, 4]  # Ground admittance
        a = lined[:, 5]  # Tap setting value
        nl = len(fb)  # Number of branches
        Pl = busd[:, 6]  # PLi
        Ql = busd[:, 7]  # QLi
        nb = len(Vm)  # Number of buses
        Iij = np.zeros((nb, nb), dtype=complex)
        Sij = np.zeros((nb, nb), dtype=complex)

        # Bus current injections
        I = Y@Vm
        Im = np.abs(I)
        Ia = np.angle(I)
        # print(fb)
        # print(tb)
        # Line current flows
        for m in range(nb):
            for n in range(nl):
                # print(f"m: {m}, n: {n}")
                # print(f"fb: {fb[n]}, tb: {tb[n]}")
                if fb[n] == m+1:
                    p = int(tb[n])-1
                    Iij[m, p] = -(Vm[m] - Vm[p]) * Y[m, p] + b[n] * Vm[m]
                    Iij[p, m] = -(Vm[p] - Vm[m]) * Y[p, m] + b[n] * Vm[p]
                elif tb[n] == m+1:
                    p = int(fb[n])-1
                    Iij[m, p] = -(Vm[m] - Vm[p]) * Y[p, m] + b[n] * Vm[m]
                    Iij[p, m] = -(Vm[p] - Vm[m]) * Y[m, p] + b[n] * Vm[p]
        #print(Iij)
        Iijr = Iij.real
        Iiji = Iij.imag
        # Line Power Flows
        for m in range(nb):
            for n in range(nb):
                if m != n:
                    Sij[m, n] = Vm[m] * np.conj(Iij[m, n]) * BMva

        # Extract active and reactive power
        Pij = Sij.real
        Qij = Sij.imag
        # Line Losses
        # Lij = np.zeros((n, n), dtype=complex)
        Lij = np.zeros((nb, nb), dtype=complex)
        for m in range(nl):
            p = int(fb[m])-1
            q = int(tb[m])-1
            Lij[p,q] = Sij[p, q] + Sij[q, p]
            Lij[q,p] = Sij[p, q] + Sij[q, p]
        #print(Lij)
        # Extract active and reactive line losses
        Lpij = Lij.real
        Lqij = Lij.imag

        # Bus Power Injections
        Si = np.zeros((nb, 1), dtype=complex)
        for i in range(nb):
            for k in range(nb):
                Si[i] += np.conj(Vm[i]) * Vm[k] * Y[i, k] * BMva

        # Extract active and reactive power injections
        Pi = Si.real
        Qi = -Si.imag
        # Total active and reactive power
        Pg = Pi.T + Pl
        Qg = Qi.T + Ql

        return Lij,Sij,Pij,Qij,Pg,Qg, Pi, Qi, Iij, Pl

    
    def loadflow(self, V, del_, BMva):
        Y = self.ybusppg()  # Calling Ybus program (assuming it's defined)
        lined = self.linedata  # Assuming this function is also defined
        busd = self.busdata  # Assuming this function is defined as well
        Vm = V*np.cos(del_) + 1j*V*np.sin(del_)
        Del = np.rad2deg(del_)  # Bus voltage angles in degrees
        fb = lined[:, 0]  # From bus number
        tb = lined[:, 1]  # To bus number
        b = lined[:, 4]  # Ground admittance
        a = lined[:, 5]  # Tap setting value
        nl = len(fb)  # Number of branches

        Pg = busd[:, 4] / BMva
        Qg = busd[:, 5] / BMva

        Pl = busd[:, 6] / BMva  # PLi
        Ql = busd[:, 7] / BMva # QLi

        Qmin = busd[:, 8] / BMva
        Qmax = busd[:, 9] / BMva

        nbus = len(busd)

        P = Pg - Pl
        Q = Qg - Ql

        Psp = P
        Qsp = Q

        G = np.real(Y)
        B = np.imag(Y)

        pv = np.where(np.logical_or(busd[:, 1] == 2, busd[:, 1] == 3))[0]
        pq = np.where(busd[:, 1] == 3)[0]

        npv = len(pv)
        npq = len(pq)

        Tol = 1
        Iter = 1
        check = True

        while Tol > 1e-8:
            #Tol > 1e-1:

            P = np.zeros(nbus)
            Q = np.zeros(nbus)

            for i in range(nbus):
                for k in range(nbus):
                    P[i] += V[i] * V[k] * (G[i, k] * np.cos(Del[i] - Del[k]) + B[i, k] * np.sin(Del[i] - Del[k]))
                    Q[i] += V[i] * V[k] * (G[i, k] * np.sin(Del[i] - Del[k]) - B[i, k] * np.cos(Del[i] - Del[k]))

            '''
            if Iter <= 7 and Iter >= 2:
                for n in range(1, nbus):
                    if busd[n, 1] == 2:
                        QG = Q[n] + Ql[n]
                        if QG < Qmin[n]:
                            V[n] += 0.01
                        elif QG > Qmax[n]:
                            V[n] -= 0.01
                            '''


            dPa = Psp - P
            dQa = Qsp - Q

            k = 0
            dQ = np.zeros(npq)
            for i in range(nbus):
                if busd[i, 1] == 3:
                    dQ[k] = dQa[i]
                    k += 1
            dP = dPa[1:]
            M = np.concatenate((dP, dQ))

            J1 = np.zeros((nbus - 1, nbus - 1))
            for i in range(nbus - 1):
                ii = pv[i]
                for j in range(nbus - 1):
                    jj = pv[j]
                    if ii == jj:
                        for k in range(nbus):
                            kk = k
                            if ii!=kk:
                                J1[i, i] += V[ii] * V[kk] * (-G[ii, kk] * np.sin(Del[ii] - Del[kk]) +
                                                        B[ii, kk] * np.cos(Del[ii] - Del[kk]))
                    else:
                        J1[i, j] = V[ii] * V[jj] * (G[ii, jj] * np.sin(Del[ii] - Del[jj]) -
                                                   B[ii, jj] * np.cos(Del[ii] - Del[jj]))

            J2 = np.zeros((nbus - 1, npq))
            for i in range(nbus - 1):
                ii = pv[i]
                for j in range(npq):
                    jj = pq[j]
                    if ii == jj:
                        for k in range(nbus):
                            kk = k
                            J2[i, j] += V[kk] * (G[ii, kk] * np.cos(Del[ii] - Del[kk]) + B[ii, kk] * np.sin(Del[ii] - Del[kk]))

                        J2[i,j] += V[ii]*G[ii,ii]
                    else:
                        J2[i, j] = V[ii] * (G[ii, jj] * np.cos(Del[ii] - Del[jj]) +
                                           B[ii, jj] * np.sin(Del[ii] - Del[jj]))

            J3 = np.zeros((npq, nbus - 1))
            for i in range(npq):
                ii = pq[i]
                for j in range(nbus - 1):
                    jj = pv[j]
                    if ii == jj:
                        for k in range(nbus):
                            kk = k
                            if ii!=kk:
                                J3[i, j] += V[ii] * V[kk] * (G[ii, kk] * np.cos(Del[ii] - Del[kk]) +
                                                       B[ii, kk] * np.sin(Del[ii] - Del[kk]))
                    else:
                        J3[i, j] = V[ii] * V[jj] * (-G[ii, jj] * np.cos(Del[ii] - Del[jj]) -
                                                   B[ii, jj] * np.sin(Del[ii] - Del[jj]))


            J4 = np.zeros((npq, npq))
            for i in range(npq):
                ii = pq[i]
                for j in range(npq):
                    jj = pq[j]
                    if ii == jj:
                        for k in range(nbus):
                            kk = k
                            J4[i, j] += V[kk] * (G[ii, kk] * np.sin(Del[ii] - Del[kk]) -
                                                 B[ii, kk] * np.cos(Del[ii] - Del[kk]))

                        J4[i,j] -= V[ii]*B[ii,ii]
                    else:
                        J4[i, j] = V[ii] * (G[ii, jj] * np.sin(Del[ii] - Del[jj]) -
                                           B[ii, jj] * np.cos(Del[ii] - Del[jj]))
                        
            Tol = np.max(np.abs(M))
            
            
            J = np.block([[J1, J2], [J3, J4]])

            X = np.linalg.solve(J, M)  # 4x1 [del2, del3, V2, V3]

            dTh = X[:nbus - 1]
            dV = X[nbus - 1:]

            Del[1:] += dTh
            k = 0
            for i in range(1, nbus):
                if busd[i, 1] == 3:
                    V[i] += dV[k]
                    k += 1

            Iter += 1
            
            if Iter > 10:
                check = False
                break

        Del = np.rad2deg(Del)
        return V, Del, Iter, check


# In[ ]:




