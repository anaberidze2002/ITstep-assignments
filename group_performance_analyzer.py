scores = []
print("შეიყვანეთ სტუდენტების ქულები. დასასრულებლად ჩაწერეთ 'stop'.")

while True:
    user_input = input("შეიყვანეთ ქულა: ").strip()
    if user_input.lower() == 'stop':
        break
    try:
        score = float(user_input)
        if 0 <= score <=10:
            scores.append(score)
        else:
            print("ქულა უნდა იყოს 0-დან 10-მდე!")
    except ValueError:
        print("გთხოვთ შეიყვანოთ სწორი რიცხვი ან 'stop")
        
if scores:
    min_score = min(scores)
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)
    
    print("\n" + "="*30)
    print(f"კლასის საშუალო პერფორმანსი:")
    print(f"მინიმალური ქულა: {min_score}")
    print(f"მაქსიმალური ქულა: {max_score}")
    print(f"საშუალო ქულა: {avg_score:.2f}")
    
    sorted_scores = sorted(scores)
    print(f"ქულები ზრდადობით: {sorted_scores}")
    print("\nქულების განმეორების სიხშირე:")
    counted_scores = {}
    for s in sorted_scores:
        if s in counted_scores:
            counted_scores[s] += 1
        else:
            counted_scores[s] = 1
    for key, value in counted_scores.items():
        print(f"ქულა {key} განმეორდა {value}-ჯერ")
else:
    print("\nარცერთი ქულა არ ყოფილა შეყვანილი.")