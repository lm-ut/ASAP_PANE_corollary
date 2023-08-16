# ASAP_corollary

### This script was used to further test ASAP (prj presented at ESHG23 and SMBE23)

Takes a ped file and insert missing data randomly in the available alleles, but in a progressive fashion so that:

-the first 10 individuals (samples 1st to 10th) will have 10% of missing data,  
-the second 10 (samples from 11th to 20th) 20% of missing data,  
-the third 10 (samples from 21st to 30th) 30% of missing data,  
-the fourth 10 (samples from 31st to 40th) 40% of missing data,  
-the fifth 10 (samples from 41st to 50th) 50% of missing data  
If the dataset has more than 50 samples, the loop restarts.  

  
 
It then creates fake diploid samples, in fact duplicating the number of individuals, and mimicking ancient DNA.  


  
### Usage: python script.py input.ped output.ped  


  
Questions or issues at ludovica.molinaro@kuleuven.be
