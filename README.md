# SurfaceCode

This is the implementation of surfacecode



# Example


You can initialize a 4*4 surface code object by:

```python
from surface import surfaceCode
surf=surfaceCode(4)
surf.draw_surface()
```


The output looks like

```bash
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
```


To compile the syndrome extraction circuit to qiskit, call


```python
surf.compile_syndrome_circuit()
circuit=surf.get_circuit()
circuit.draw('mpl')
```

You can also print the stabilizer check matrix of the code by:


```python
H=surf.get_check_matrix()
print(H)
```

