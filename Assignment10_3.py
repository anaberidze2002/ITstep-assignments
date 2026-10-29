from functools import reduce

names = ["Ana", "Nino", "Luka", "Giorgi", "Mariam"]
scores = [45, 82, 91, 38, 74]

def pair_students(names_list, scores_list):
    return list(zip(names_list, scores_list))

def get_passed_students(paired_data, passing_score=60):
    return list(
        filter(lambda student: student[1] >= passing_score, paired_data)
    )
    
def calculate_average_of_passed(passed_students):
    if not passed_students:
        return 0
    just_scores = list(map(lambda student: student[1], passed_students))
    total_score = reduce(lambda x, y: x + y, just_scores)
    return total_score / len(passed_students)

paired_data = pair_students(names, scores)
print("დაწყვილებული მონაცემები:", paired_data)

passed_students = get_passed_students(paired_data)
print("გადასული სტუენტები:", passed_students)

average_score = calculate_average_of_passed(passed_students)
print("გადასული სტუდენტების საშუალო ქულა:", average_score)