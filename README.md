# PANE (old ASAP) corollary 

### Fake Haploids
##### This script was used to further test PANE/ASAP with aDNA-like data

Takes a ped file and insert missing data randomly in the available alleles, but in a progressive fashion so that:

-the first 10 individuals (samples 1st to 10th) will have 10% of missing data,  
-the second 10 (samples from 11th to 20th) 20% of missing data,  
-the third 10 (samples from 21st to 30th) 30% of missing data,  
-the fourth 10 (samples from 31st to 40th) 40% of missing data,  
-the fifth 10 (samples from 41st to 50th) 50% of missing data  
If the dataset has more than 50 samples, the loop restarts.  

  
 
It then creates fake haploid samples, in fact duplicating the number of individuals, and mimicking ancient DNA.  


  
Usage: python script.py input.ped output.ped  



### BlockJackkife_PCA
##### This script was used to further test ASAP (prj presented at ESHG23)

This script is currently not meant to be used outside the ASAP project.  

Takes suffix of binary plink files and output 20 plink files with one SNP window removed, prepares also convertf par file for conversion (this step requires a simple bash script 'BED2EIG.sh').
To modify window length, edit line 39 'nblocks' (default is 20). 


### Msprime simulations
###### This script creates 3 simulated groups, two sources and one admixed group
The script was used to create multiple admixed groups that underwent different admixture generation times and a bottleneck after the admixture event. 
