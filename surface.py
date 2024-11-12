from qiskit import QuantumCircuit
from typing import List
import numpy as np


class stabalizer:
    
    '''
    The stabilzier is a list of typle.
    For example:
          stab=[('X',1),('X',2),('Z',5),('Z',6)] 
          means the stabilizer is X1-X2-Z5-Z6
    '''
    def __init__(self,stab:List[tuple])->None:
        self.__stab=stab


    def __str__(self) -> str:
        strresult=""
        index=0
        for (stype,qubit) in self.__stab:
            strresult=strresult+stype+str(qubit)
            if index<len(self.__stab)-1:
                strresult=strresult+"-"
            index=index+1
        return strresult
    
    
    def get_stab(self)->List[tuple]:
        return self.__stab




class surfaceCode:
    
    
    '''
    Initialize a d*d surface code
    '''
    def __init__(self,distance:int) -> None:
        self._distance=distance
        '''
        A standard surface code has 2*distance**2-1 qubits and distance**2-1 stabilizers
        Following is the dataqubit of a 4*4 surface code                                                                                    
                                    Q1----Q2----Q3----Q4
                                    |    |     |     |
                                    |    |     |     | 
                                    Q5----Q6----Q7----Q8
                                    |    |     |     |
                                    |    |     |     | 
                                    Q9---Q10---Q11---Q12
                                    |    |     |     | 
                                    |    |     |     |
                                    Q13--Q14---Q15---Q16   
        We use the standard coordinate system to represent the qubits.
        Q1: (0,0), Q2: (0,1), Q3: (0,2), Q4: (0,3)                      
        Q5: (1,0), Q6: (1,1), Q7: (1,2), Q8: (1,3)
        Q9: (2,0), Q10:(2,1), Q11:(2,2), Q12:(2,3)
        Q13:(3,0), Q14:(3,1), Q15:(3,2), Q16:(3,3)                                     
        '''
        self._circuit=QuantumCircuit(2*distance**2-1,distance**2-1)
        self._ndataqubits=distance**2
        self._nstab=distance**2-1
        self._nXstab=0
        self._nZstab=0
        self._stab=[]
        self.calc_stab()
        self._Hmatrix=np.zeros((self._nstab, 2*self._ndataqubits),dtype=int)
        self.calculate_H_matrix()
        
    def get_xy(self,qubit:int)->tuple:
        return qubit//self.__distance,qubit%self.__distance
        
        
    def draw_surface(self)->None:
        resultstr=""
        for line in range(self._distance):
            linestr=""
            for column in range(self._distance):
                index=line*self._distance+column+1
                if(column<self._distance-1):
                    if(len(str(index))==1):
                        linestr=linestr+"Q"+str(index)+"----"
                    if(len(str(index))==2):
                        linestr=linestr+"Q"+str(index)+"---"
                else:
                    linestr=linestr+"Q"+str(index)

            if line<self._distance-1:
                linestr=linestr+"\n"
                for column in range(self._distance-1):
                    linestr=linestr+"|     "
                linestr=linestr+"|\n"
                for column in range(self._distance-1):
                    linestr=linestr+"|     "
                linestr=linestr+"|\n"       
            resultstr=resultstr+linestr
        print(resultstr)     
        
    '''
    Calculate the satbilizer
    Each stabilizer is stored in a list.
    For example, S1=[1,2,5,6]
    '''    
    def calc_stab(self):
        '''
        Add X stabilizers in side the boundary
                        Qa------Qa+1
                        |       |
                        |       |
                        Qa+d----Qa+d+1
        line 0: Q1-Q2-Q3-...-Qd
        line 1: Qd+1-Q6-Q7-Q8-...-Q2d
        ...
        line k: Qkd+1-Qkd+2-...-Q(k+1)d
                        
        '''
        d=self._distance
        currentLine=0
        lefttopIndex=1
        while currentLine<d  and lefttopIndex+d+1<=d**2:
            self._stab.append(stabalizer([('X',lefttopIndex),('X',lefttopIndex+1),('X',lefttopIndex+d),('X',lefttopIndex+d+1)]))
            self._nXstab+=1
            if lefttopIndex+2 < (currentLine+1)*d:
                lefttopIndex=lefttopIndex+2
            else:
                currentLine=currentLine+1
                lefttopIndex=lefttopIndex+3
    
        '''
        Add X stabilizers that attached to the top and bottom boundary(Tough boundary)
        '''        
        leftindex=2
        while leftindex+1<=d:
            self._stab.append(stabalizer([('X',leftindex),('X',leftindex+1)]))
            self._nXstab+=1
            leftindex+=2
        leftindex=d*(d-1)+2
        while leftindex+1<=d**2:
            self._stab.append(stabalizer([('X',leftindex),('X',leftindex+1)]))
            self._nXstab+=1
            leftindex+=2
                            
        '''
        Add Z stabilizers inside the boundary
        '''
        currentLine=0
        lefttopIndex=2
        while currentLine<d  and lefttopIndex+d+1<=d**2:
            self._stab.append(stabalizer([('Z',lefttopIndex),('Z',lefttopIndex+1),('Z',lefttopIndex+d),('Z',lefttopIndex+d+1)]))
            self._nZstab+=1
            if lefttopIndex+2 < (currentLine+1)*d:
                lefttopIndex=lefttopIndex+2
            else:
                currentLine=currentLine+1
                lefttopIndex=lefttopIndex+3       

        '''
        Add Z stabilizers that attached to the left and right boundary(Soft boundary)
        '''          
        topindex=1     
        while topindex+d<=(d-1)*d+1:
            self._stab.append(stabalizer([('Z',topindex),('Z',topindex+d)]))
            self._nZstab+=1
            topindex=topindex+2*d
        topindex=d
        while topindex+d<=d**2:
            self._stab.append(stabalizer([('Z',topindex),('Z',topindex+d)]))
            self._nZstab+=1
            topindex=topindex+2*d


    def get_stab_by_index(self,index:int)->stabalizer:
        return self._stab[index]
    
    
    def print_stab(self):
        for s in self._stab:
            print(s)
    

    
    def compile_syndrome_circuit(self):
        synindex=0
        for stab in self._stab:
            tmpstab=stab.get_stab()
            if tmpstab[0][0]=='X':
                self._circuit.h(self._ndataqubits+synindex)
                for (typestr,qubit) in tmpstab:
                        self._circuit.cx(self._ndataqubits+synindex,qubit)
                
                self._circuit.h(self._ndataqubits+synindex)
            else:
                
                for (typestr,qubit) in tmpstab:
                        self._circuit.cx(qubit,self._ndataqubits+synindex)                     
            '''
            Measure the syndrome qubit
            ''' 
            self._circuit.measure(self._ndataqubits+synindex,synindex)
            synindex+=1 
        
        
    def get_circuit(self)->QuantumCircuit:
        return self._circuit
        
        
        
    '''
    Surface code is a CSS code, which means it has X and Z stabilizers.
    We can calculate the check matrix H
    For example, a code with stabilizers: S1=Z1Z2, S2=Z2Z3, S3=X1X2, S4=X2X3 has the following check matrix:
                                Z1  Z2  Z3  X1  X2  X3                                       
                            S1  1   1   0   0   0   0 
                        H=  S2  0   1   1   0   0   0   
                            S3  0   0   0   1   1   0 
                            S4  0   0   0   0   1   1 
                        
    '''                     
    
    def calculate_H_matrix(self):
        stabindex=0
        for stab in self._stab:
            tmpstab=stab.get_stab()
            for (typestr,qubit) in tmpstab:
                if typestr=='Z':
                    self._Hmatrix[stabindex][qubit-1]=1
                else:
                    self._Hmatrix[stabindex][self._ndataqubits+qubit-1]=1
            stabindex+=1
    
    
        
    
    
    
    
    
    
    
if __name__ == '__main__':
    suf=surfaceCode(4)
    suf.calc_stab()
    #suf.draw_surface()
    #suf.print_stab()
    print(suf._Hmatrix)