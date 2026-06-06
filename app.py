from rag_engine import ask_question

history = []

while True:
    question = input("Ask your weed question: ")

    if question.lower() == "exit":
        print("Chat stopped")
        break

    answer = ask_question(question, history)

    print("\nAnswer:")
    print(answer)

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})