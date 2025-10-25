import csv
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from db.question_crud import create_question, delete_all_questions
from db.questions import QUESTION


async def export_questions_to_csv(filename: str = "questions.csv"):
    headers = ["question_title", "question_body", "answer", "category", "image_name"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for question_id, question_data in QUESTION.items():
            row_data = {
                "question_title": question_data["question_title"],
                "question_body": question_data["question_body"],
                "answer": question_data["answer"],
                "category": question_data["category"],
                "image_name": question_data["image_name"],
            }
            writer.writerow(row_data)
    
    print(f"Данные экспортированы в {filename}")


async def import_from_csv(filename: str = "questions.csv"):
    if not os.path.exists(filename):
        print(f"{filename} не найден")
        return False
    
    try:
        await delete_all_questions()
        print("Таблица очищена")
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)    
            imported_count = 0
            for row in reader:
                question_data = {
                    "question_title": row["question_title"],
                    "question_body": row["question_body"],
                    "answer": row["answer"],
                    "category": row["category"],
                    "image_name": row["image_name"] if row["image_name"] else None
                }
                await create_question(**question_data)
                imported_count += 1
            
            print(f"Импортировано {imported_count} вопросов из {filename}")
            return True
            
    except Exception as e:
        print(f"Ошибка импортирования CSV: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    async def main():
        # await export_questions_to_csv("questions.csv")
        await import_from_csv("questions.csv")
    asyncio.run(main())
