print("Starting test...")

from rag_engine import ask_question

print("Imported rag_engine successfully")

answer = ask_question("How to control Canada thistle?", [])

print("Answer type:", type(answer))
print("Answer length:", len(answer) if answer else 0)
print("Answer value:")
print(repr(answer))