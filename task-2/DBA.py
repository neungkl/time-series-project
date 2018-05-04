'''
/*******************************************************************************
 * Copyright (C) 2017 Zahraa Abdallah 
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 ******************************************************************************/ 
This is a python Class for DBA 
Python command: 
    import DBA
    DBA.DBA()


'''

import numpy
import math
from random import *

 # This toy class show the use of DBA.

__author__ ="Zahraa Abdallah"

class DBA(object): 
    
    NIL = -1
    DIAGONAL = 0
    LEFT = 1
    UP = 2
    
	# This attribute is used in order to initialize only once the matrixes
	 
    MAX_SEQ_LENGTH = 2000
  
    # store the cost of the alignment

    costMatrix =[[0 for i in range(2000)] for j in range(2000)]
    
    # store the warping path

    pathMatrix = [[0 for i in range(2000)] for j in range(2000)]
    
    # store the length of the optimal path in each cell

    optimalPathLength = [[0 for i in range(2000)] for j in range(2000)]
    
    def __init__(self):
        sequences =[[0 for i in range(20)] for j in range(100)]
        for i in range(0,len(sequences)): 
          for j in range (0, len(sequences[i])):
              sequences[i][j] = math.cos(random()*j/20.0*math.pi) 
        averageSequence = [0 for i in range (0,len(sequences[0]))]
        choice = int(random()*100)
        
        for j in range (len(averageSequence)):
            averageSequence[j] = sequences[choice][j] 
        
        print(averageSequence)

        averageSequence= self.applyDBA(averageSequence, sequences)
       
        print(averageSequence)

        averageSequence= self.applyDBA(averageSequence, sequences)
        
        print(averageSequence) 

    
    def distanceTo(self, a, b):
        return (a - b) * (a - b)

    def barycenter(self, tab):
        if len(tab) < 1:  
            print("empty double tab")
            return
        sum_ = 0.0
        for o in tab: 
            sum_ += float(o) #to double 
        return sum_/ len(tab)
    
    '''
    	 * Dtw Barycenter Averaging (DBA)
	 * @param C average sequence to update
	 * @param sequences set of sequences to average
    '''
    
    def applyDBA(self, C, sequences): 
        tupleAssociation = []
        res = 0.0
        centerLength = len(C)
        for i in range (0,len(C)) :
            tupleAssociation.append([]) 

        for T in sequences:
            seqLength = len(T)
            self.costMatrix[0][0] = self.distanceTo(C[0], T[0])
            self.pathMatrix[0][0] = self.NIL;
            self.optimalPathLength[0][0] = 0
        
            for i in range(1, centerLength): 
                self.costMatrix[i][0] = self.costMatrix[i - 1][0] + self.distanceTo(C[i], T[0])
                self.pathMatrix[i][0] = self.UP
                self.optimalPathLength[i][0] = i
        
            for j in range(1, seqLength):
                self.costMatrix[0][j] = self.costMatrix[0][j - 1] + self.distanceTo(T[j], C[0])
                self.pathMatrix[0][j] = self.LEFT
                self.optimalPathLength[0][j] = j

            for i in range(1, centerLength): 
                for j in range (1,seqLength):
                    indiceRes = numpy.argmin([self.costMatrix[i - 1][j - 1], self.costMatrix[i][j - 1], self.costMatrix[i - 1][j]])
                    self.pathMatrix[i][j] = indiceRes
                    if indiceRes ==self.DIAGONAL : 
                        res = self.costMatrix[i - 1][j - 1]
                        self.optimalPathLength[i][j] = self.optimalPathLength[i - 1][j - 1] + 1
                    elif indiceRes== self.LEFT :
                        res = self.costMatrix[i][j - 1]
                        self.optimalPathLength[i][j] = self.optimalPathLength[i][j - 1] + 1
                    elif indiceRes== self.UP:
                        res = self.costMatrix[i - 1][j]
                        self.optimalPathLength[i][j] = self.optimalPathLength[i - 1][j] + 1
                    self.costMatrix[i][j] = res + self.distanceTo(C[i], T[j])

            nbTuplesAverageSeq = self.optimalPathLength[centerLength - 1][seqLength - 1] + 1
            i = centerLength - 1
            j = seqLength - 1
        
            for  t in range(nbTuplesAverageSeq-1,-1, -1):
                tupleAssociation[i].append(T[j])
                if self.pathMatrix[i][j]==self.DIAGONAL: 
                    i = i - 1
                    j = j - 1
                elif self.pathMatrix[i][j]==self.LEFT: 
                    j = j - 1
                elif self.pathMatrix[i][j]==self.UP: 
                    i = i - 1
        
        for t in range(0,centerLength): 
            C[t] = self.barycenter(tupleAssociation[t])
        return C


    
   