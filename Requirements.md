## Requirements
- Calculate scores 
- Higher scores should signal better results
- Score metrics (S)
	- Energy Consumption (A)
	- Potential Energy Generation (B)
	- Effective Energy Generation (D)
	- Potential Savings on improvements (F)
	- Effective Savings (G)
	- Co2 Saved(H) 

## Notes

Is effective energy consumption the same as current energy consumption ?  yes

Potential is prediction of how much it can do ideally and effective is how much it is doing dues to external conditions e.g. weather, sensor faults, equipment differences etc  

the problem very clearly is the difference in potential and real world created so the questions is how you decrease that difference ? 

effective score =  ((-A) + B + F) 
potential score =  ((-A) + D + G)
error margin  =  E + (F - G)

 Since this is the same house in all scenarios it is suggested to add weights to the original equations and then use gradient descent to decrease the error margin of the model.
 

Improved equation
potential score = ((-A) + D(W1) + G(W2))


w_i = w_i - learning_rate × (partial derivative of Loss with respect to w_i)

what is partial derivative of Loss?
a derivative of a multivariable function with respect to one of its variables, while treating all other variables as constants

something like bellow for both weights:
wB = wB + learning_rate × 2 × (D - wB × B) × B



