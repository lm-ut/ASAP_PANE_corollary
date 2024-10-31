import msprime
import daiquiri
import argparse
import os

parser = argparse.ArgumentParser(description="Perform msprime simulations.")

# Pop Sizes at Gen 0 
parser.add_argument("--pop_size_A", help="Pop Size A",type=int, default = 10000)
parser.add_argument("--pop_size_B", help="Pop Size B",type=int, default = 10000)
parser.add_argument("--pop_size_C", help="Pop Size C",type=int, default = 10000)
parser.add_argument("--pop_size_ANC", help="Pop Size ANC",type=int, default = 10000)

# Admixture proportions
parser.add_argument("--prop_A", help="Prop A",type=float, default = 0.7)
parser.add_argument("--prop_B", help="Prop B",type=float, default = 0.3)

# Admixture Time
parser.add_argument("--admg", help="admg",type=int, default = 250)

# After Bottleneck size
parser.add_argument("--post_btln_size", help="post btln",type=int, default = 1000)

# Bottleneck time
parser.add_argument("--btln_time", help="post btln",type=int, default = 200)

# Ind to sample
parser.add_argument("--ind_sampled", help="ind sampled",type=int, default = 50)

#Output name
parser.add_argument("--output", help="outputname")

args = parser.parse_args()

    
# Parameters
population_size_A = args.pop_size_A  # Population size for A 
population_size_B = args.pop_size_B  # Population size for B
admixture_proportion_A = args.prop_A  # 70% from population A
admixture_proportion_B = args.prop_B # 30% from population B
admixture_time = args.admg  # Admixture event 250 generations ago
initial_size_C = args.pop_size_C  # Initial size of population C after admixture
bottleneck_size_C = args.post_btln_size  # Population C size after bottleneck
bottleneck_time = args.btln_time  # Bottleneck happens 200 generations ago
num_individuals_to_sample = args.ind_sampled  # Number of individuals to sample per
 population

# Simulating the two ancestral populations A and B
demography = msprime.Demography()
demography.add_population(name="A", initial_size=population_size_A)
demography.add_population(name="B", initial_size=population_size_B)
demography.add_population(name="C", initial_size=bottleneck_size_C)
demography.add_population(name="ANC", initial_size=population_size_A,initially_acti
ve=False)

print("BEGIN")
#print(demography)

#Add initial split ANC -> A,B
demography.add_population_split(time=1000, ancestral="ANC", derived=["A", "B"])

# Admixture event: 70% from A and 30% from B to form population C
demography.add_admixture(
    time=admixture_time,
    derived="C",  # Population C is the result of admixture
    ancestral=["A", "B"],  # Populations A and B
    proportions=[admixture_proportion_A, admixture_proportion_B]
)
print("ADD ADMX")
#print(demography)

# Bottleneck event: C reduces from 10,000 to 1,000 individuals 200 generations ago
demography.add_population_parameters_change(
    time=bottleneck_time,
    population="C",
    initial_size=initial_size_C
)
print("ADD BOTTLENECK")


# Sort events to ensure they are time-ordered
demography.sort_events()
print(demography)
print(demography.debug())

# Simulating a tree sequence
daiquiri.setup(level="INFO")
#daiquiri.setup(level="DEBUG")
simulation = msprime.sim_ancestry(
    samples={"A": num_individuals_to_sample,  # Sample 50 from population A
             "B": num_individuals_to_sample,  # Sample 50 from population B
             "C": num_individuals_to_sample},  # Sample 50 from population C
    demography=demography,
    sequence_length=2.5e8,  # Adjust the sequence length as necessary 
    recombination_rate=1.25e-8,  # Recombination rate (adjust if needed)
    random_seed=42
)

# Adding mutations to the tree sequence
mutated_ts = msprime.sim_mutations(simulation, rate=1e-8)
print("Done Mut")

# Writing the output to a VCF file
with open(args.output, "w") as vcf_file:
    mutated_ts.write_vcf(vcf_file)

print("Vcf ready")

