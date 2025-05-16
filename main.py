"""
Mini-Project 2 - Autumn Portugal
I generally followed the pseudocode in this document for the DPDA algorithm: 
https://stanford-cs161.github.io/winter2022/assets/files/lecture17-notes.pdf
"""
import matplotlib.pyplot as plt
import math
import sys
from random import randrange, uniform

n = None
# If use_uniform is True we use the uniform model to generate preferences. If 
# False we use the public/private model to generate preferences.
use_uniform = False
lambda_score = 1

class Entity:
    '''
    Represents a doctor/hospital

    Input:
    id - the unique id of this entity
    public_scores - only used in public/private model but represents the global 
        scores of doctors/hospitals. A doctor would need hospital the public scores 
            and a hospital would need the doctor public scores.
    '''
    def __init__(self, id, public_scores):
        self.id = id
        self.next_preference = 0 # pointer to which doctor/hospital to propose to next
        self.preferences = [i for i in range(n)]
        if (use_uniform):
            self.generate_preferences_uniform()
        else:
            self.private_scores = [uniform(0, 1) for _ in range(n)]
            self.generate_preferences_publicprivate(public_scores)
        self.match = None

    def generate_preferences_uniform(self):
        rankings = [r for r in range(n)]
        for p in range(n):
            self.preferences[p] = rankings.pop(randrange(len(rankings)))

    def generate_preferences_publicprivate(self, public_scores):
        utilty = [0 for _ in range(n)]

        for i in range(n):
            utilty[i] = lambda_score * public_scores[i] + (1 - lambda_score) * self.private_scores[i]

        temp = sorted([(self.preferences[i], utilty[i]) for i in range(n)], key=lambda t: t[1], reverse=True)

        for i in range(n):
            self.preferences[i] = temp[i][0]


def dpda(num):
    global n 
    n = num

    # these aren't needed for uniform, but it's easier to just generate regardless
    hos_public_scores = [uniform(0, 1) for _ in range(n)]
    doc_public_scores = [uniform(0, 1) for _ in range(n)]

    doctors = [Entity(i, hos_public_scores) for i in range(n)]
    hospitals = [Entity(i, doc_public_scores) for i in range(n)]
        
    free_doctors = doctors.copy()

    num_proposals = 0
    while (len(free_doctors) > 0):
        d = free_doctors.pop(0) # Try to match the first doctor but it could be random
        h = hospitals[d.preferences[d.next_preference]]
        d.next_preference += 1
        num_proposals += 1

        if (not h.match):
            h.match = d
            d.match = h
        elif (h.preferences.index(d.id) < h.preferences.index(h.match.id)):
            free_doctors.append(h.match)
            h.match = d
            d.match = h
        else:
            free_doctors.append(d)

    return (num_proposals, doctors, hospitals)

def part_1(num_tests, nums):
    data = []
    for num in nums:
        print(f"Test n = {num}")
        total_proposals = 0
        for i in range(num_tests):
            total_proposals += dpda(num)[0]
        data.append(total_proposals / num_tests)

    nlnn = [num * math.log(num) for num in nums]

    plt.plot(nums, nlnn, color="red")
    plt.bar(nums, data, color="blue")

    plt.title("Average total number of proposals over n")
    plt.xlabel("n")
    plt.ylabel(f"Average number of proposals over {num_tests} tests")
    plt.legend(["n*ln(n)"])

    plt.savefig(f"./part1.png", dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()

def part_2(num_iterations, num):
    data = []

    for i in range(num_iterations):
        print(f"Test {i + 1}")
        data.append(dpda(num)[0])

    plt.hist(data, bins=int(math.sqrt(num_iterations)), color="blue")

    plt.title(f"Distribution of the total number of proposals over {num_iterations} instances for n = {num}")
    plt.xlabel(f"Number of Proposals")
    plt.ylabel(f"Count")

    plt.savefig(f"./part2.png", dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()

def part_3(num_tests, nums):
    doctor_data = []
    hospital_data = []

    for num in nums:
        print(f"Test n = {num}")

        doctor_total_rank_averages = 0
        hospital_total_rank_averages = 0
        for i in range(num_tests):
            dpda_data = dpda(num)
            
            total_rank = 0
            for d in dpda_data[1]:
                total_rank += d.preferences.index(d.match.id) + 1
            doctor_total_rank_averages += total_rank / len(dpda_data[1])

            total_rank = 0
            for h in dpda_data[2]:
                total_rank += h.preferences.index(h.match.id) + 1
            hospital_total_rank_averages += total_rank / len(dpda_data[2])

        doctor_data.append(doctor_total_rank_averages / num_tests)
        hospital_data.append(hospital_total_rank_averages / num_tests)

    # Plot Doctor Data
    lnn = [math.log(num) for num in nums]
    
    plt.plot(nums, lnn, color="red")
    plt.bar(nums, doctor_data, color="blue")

    plt.title("Average rank of doctor's match over n")
    plt.xlabel("n")
    plt.ylabel(f"Average rank of doctor's match over {num_tests} tests")
    plt.legend(["ln(n)"])

    plt.savefig(f"./part3doc.png", dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()

    # Plot Hospital Data
    n_over_lnn = [num / math.log(num) for num in nums]

    plt.plot(nums, n_over_lnn, color="red")
    plt.bar(nums, hospital_data, color="blue")

    plt.title("Average rank of hospital's match over n")
    plt.xlabel("n")
    plt.ylabel(f"Average rank of hospital's match over {num_tests} tests")
    plt.legend(["n/ln(n)"])

    plt.savefig(f"./part3hos.png", dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()

        

def main():
    global use_uniform, lambda_score

    try:
        use_uniform = bool(sys.argv[1])
        lambda_score = float(sys.argv[2])
    except:
        pass

    part_1(num_tests=5, nums=[i * 10 + 10 for i in range(50)])
    part_2(num_iterations=500, num=200)
    part_3(num_tests=5, nums=[i * 10 + 10 for i in range(50)])



if (__name__ == "__main__"):
    main()
