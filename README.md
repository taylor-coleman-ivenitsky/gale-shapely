# Run Instructions

-add the main.py file to a folder of your choice

-run the python code

-you will be prompted with a few input questions

-"Input maximum set size >3 for simulation:" means to input the maximum bipartite set size you wish the simulation to run until (only enter ints)

-"Input number of simulations for each size (recommended 500-1000)" is the number of simulations per bipartite size you wish to run, a higher number will be slower but guarantee smoother results (only enter ints)

-"Input scoring method ('add', 'mult', or 'root'): " is more complicated

- the add scoring method minimizes the sum of the two ranks for each person for each matching. If man i ranks woman j as third and woman j ranks man i as fifth then cost ij is 8.

- the mult scoring method does the same as add but multiplies, so ij would be 15
- the root scoring method sums the sqrt of i and j so the score would be sqrt(3)+sqrt(5)

-only enter one of 'add', 'mult' or 'root' otherwise the program will terminate

-the Man weighting and woman weighting prompts determine how important each gender is in the evaluation

- setting one to zero will only consider the preferences of the other gender
- both to 1 is standard
- anything other than 1 is a custom weighting, this input handles floats

-after taking these prompts in the terminal the simulation will run

-it will print out the average score for each set size and then plot the average and gendered results
