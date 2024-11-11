from qiskit import QuantumCircuit





class surfaceCode:
    
    
    '''
    Initialize a d*d surface code
    '''
    def __init__(self,distance:int) -> None:
        self.__distance=distance
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
        self._stab=[]
        
        
    def get_xy(self,qubit:int)->tuple:
        return qubit//self.__distance,qubit%self.__distance
        
        
    def draw_surface(self)->None:
        pass    
        
        
    '''
    Calculate the satbilizer
    '''    
    def calc_stab(self):
        pass 
    
    
    
        
    
    
    
    
    