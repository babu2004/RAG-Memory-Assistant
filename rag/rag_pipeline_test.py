from rag_pipeline import answer_question

while True:

    query = input("you: ")

    if query == "exit":
        break

    answer = answer_question(query)

    print("\n Assistant: \n")
    print(answer)