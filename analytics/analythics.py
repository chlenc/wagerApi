# modeling creation for 2-event model
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# this class describes behaviour of 2-event selfregulated book
# realisation without weights for events(1:1)
class COEFS():
    def __init__(self,q_1_start = 1.9,q_2_start = 1.9,bet = 1,vig = 0.052, riskAmount = 1000):
        self.q_1_start = q_1_start
        self.q_2_start = q_2_start
        self.q_1 = q_1_start
        self.q_2 = q_2_start
        self.riskAmount = riskAmount 
        self.vig = vig
        self.debtAmount1 = 0
        self.debtAmount2 = 0
        self.betThreshold = 10
        self.betMax = 100
        self.betMin = 1
        self.E = 0 #expected valueq1
        self.xI = []
        self.xII = []
        self.qI = []
        self.qII = []

    def bet(self,event,betAmount):
        if event == 1:
            if betAmount >= self.betMin and betAmount <= self.betThreshold:
                q = self.q_1
                self.qI.append(q)
                self.xI.append(betAmount)
            elif betAmount >self.betThreshold and betAmount <= self.betMax:
                q_1_bigBet = self.calcCoefIfBigBet(event,betAmount)
                self.qI.append(q_1_bigBet)
                self.xI.append(betAmount)   
            else:
                exit("incorrect bet amount")            
        elif event == 2:
            if betAmount >= self.betMin and betAmount <= self.betThreshold:
                q = self.q_2
                self.qII.append(q)
                self.xII.append(betAmount)
            elif betAmount >self.betThreshold and betAmount <= self.betMax:
                q_2_bigBet = self.calcCoefIfBigBet(event,betAmount)
                self.qI.append(q_2_bigBet)
                self.xII.append(betAmount)   
            else:
                exit("incorrect bet amount") 
        self.debtsUpdate()
        self.actualNewCoefs(betAmount)

    def calcCoefIfBigBet(self, event,betAmount):
        if event == 1:
            k =  (1 - self.q_1)/(self.betMax - self.betThreshold)
            b = 1 - k*self.betMax
            q = betAmount*k + b #?
        elif event == 2:
            k =  (1 - self.q_2)/(self.betMax - self.betThreshold)
            b = 1 - k*self.betMax
            q = betAmount*k + b
        return q

    def actualNewCoefs(self,betAmount):
        if self.debtAmount1 < 0:
            k = (1 - self.q_1_start)/(self.riskAmount)
            b = 1 - k*self.riskAmount
            self.q_1 = -k*self.debtAmount1+b
            self.q_2 = self.anotherCoef(self.q_1)
            #print(b,debt1_new,self.q_1,self.q_2)
        elif self.debtAmount2 < 0:
            k =  (1 - self.q_2_start)/(self.riskAmount)
            b = 1 - k*self.riskAmount
            self.q_2 = k*betAmount+b
            self.q_1 = self.anotherCoef(self.q_2)    
        else:
            self.q_1 = self.q_1_start 
            self.q_2 = self.q_2_start

    def debtsUpdate(self):
        paymentToPlayerI = sum([x*y for x,y in zip(self.xI,self.qI)])    
        paymentToPlayerII = sum([x*y for x,y in zip(self.xII,self.qII)])    
        self.debtAmount1 = sum(self.xI) + sum(self.xII) - paymentToPlayerI
        self.debtAmount2 = sum(self.xI) + sum(self.xII) - paymentToPlayerII
        self.E = self.debtAmount1 + self.debtAmount2
    def anotherCoef(self,q):
        return (1+self.vig-1/q)**(-1)

#test cases
coefs = COEFS()
E = []
q = []
for i in range(500):
    event = random.randint(1,2)
    coefs.bet(1,10)
    print(event,"q_1 =", coefs.q_1, "q2 =", coefs.q_2,"debt1 =", coefs.debtAmount1,"debt2 =", coefs.debtAmount2, "E =",coefs.E)
    E.append(coefs.E)
for j in range(1000):
    if j%2 == 0:
        coefs.bet(1,10)
        event = 1
        E.append(coefs.E)
        q.append(coefs.q_1)
        print(event,"q_1 =", coefs.q_1, "q2 =", coefs.q_2,"debt1 =", coefs.debtAmount1,"debt2 =", coefs.debtAmount2, "E =",coefs.E)
    else:
        coefs.bet(2,10)
        event = 2
        E.append(coefs.E)
        q.append(-coefs.q_2)
        print(event,"q_1 =", coefs.q_1, "q2 =", coefs.q_2,"debt1 =", coefs.debtAmount1,"debt2 =", coefs.debtAmount2, "E =",coefs.E) 
plt.plot(np.arange(len(E)),E)
plt.show()
plt.plot(np.arange(len(q)),q) 
plt.show()