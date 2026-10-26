input_text = "Python არის პროგრამირების ერთ-ერთი ენა. python შესწავლა ai_ის დახმარებით უფრო მარტივია."
search_word = "python"

words_list = input_text.split()
target_lower = search_word.lower()
total_words = len(words_list)

def analyze_text(text:str, target_word:str):
    word_count = 0
    longest_word = "" 
    for w in words_list:
        if w.lower().strip(".,_!?") == target_lower:
            word_count += 1
    for w in words_list:
        clean_word = w.strip(".,!?")
        if len(clean_word) > len(longest_word):
            longest_word = clean_word
    return total_words, word_count, longest_word

final_result = analyze_text(input_text, search_word)

print(final_result)