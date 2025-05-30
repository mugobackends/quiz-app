from colorama import Fore, Style, init # Optional: for colored output
from lib.models.category import Category
from lib.models.question import Question
from lib.models.answer import Answer
import random

init(autoreset=True) # Initialize Colorama for auto-resetting colors

def print_menu(title, options):
    """Prints a generic menu."""
    print(f"\n{Fore.CYAN}--- {title} ---{Style.RESET_ALL}")
    for i, option in enumerate(options):
        print(f"{Fore.YELLOW}{i+1}. {option}{Style.RESET_ALL}")
    print(f"{Fore.RED}0. Exit{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}--------------------{Style.RESET_ALL}")

def get_user_choice(max_choice):
    """Gets validated integer input from the user."""
    while True:
        try:
            choice = input(f"{Fore.GREEN}Enter your choice (0-{max_choice}): {Style.RESET_ALL}")
            choice_int = int(choice)
            if 0 <= choice_int <= max_choice:
                return choice_int
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number between 0 and {max_choice}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")

def take_quiz_menu():
    """Handles the 'Take Quiz' functionality."""
    categories = Category.get_all()
    if not categories:
        print(f"{Fore.RED}No quiz categories available. Please add some first.{Style.RESET_ALL}")
        return

    category_options = [cat.name for cat in categories]
    print_menu("Select a Quiz Category", category_options)
    
    choice = get_user_choice(len(category_options))
    if choice == 0:
        return

    selected_category = categories[choice - 1]
    print(f"\n{Fore.CYAN}--- Starting Quiz in '{selected_category.name}' Category ---{Style.RESET_ALL}")

    questions = selected_category.questions
    if not questions:
        print(f"{Fore.RED}No questions available in '{selected_category.name}'.{Style.RESET_ALL}")
        return

    random.shuffle(questions) # Randomize question order
    score = 0
    total_questions = len(questions)

    for i, question in enumerate(questions):
        print(f"\n{Fore.BLUE}Question {i+1}/{total_questions}: {question.text}{Style.RESET_ALL}")
        answers = question.answers
        if not answers:
            print(f"{Fore.YELLOW}  (No answers available for this question. Skipping.){Style.RESET_ALL}")
            continue

        random.shuffle(answers) # Randomize answer order
        answer_options = [(ans.text, ans.is_correct) for ans in answers]

        for j, (ans_text, _) in enumerate(answer_options):
            print(f"  {Fore.YELLOW}{j+1}. {ans_text}{Style.RESET_ALL}")

        answer_choice = get_user_choice(len(answer_options))
        if answer_choice == 0:
            print(f"{Fore.YELLOW}Quiz interrupted. Final score: {score}/{total_questions}{Style.RESET_ALL}")
            return

        selected_answer_is_correct = answer_options[answer_choice - 1][1]

        if selected_answer_is_correct:
            print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
            score += 1
        else:
            correct_answer_text = next((a for a, is_corr in answer_options if is_corr), "N/A")
            print(f"{Fore.RED}Incorrect. The correct answer was: {correct_answer_text}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}--- Quiz Finished! ---{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}You scored: {score} out of {total_questions}{Style.RESET_ALL}")
    if total_questions > 0:
        percentage = (score / total_questions) * 100
        print(f"{Fore.MAGENTA}Percentage: {percentage:.2f}%{Style.RESET_ALL}")


def manage_categories_menu():
    """Handles category management."""
    while True:
        options = ["View Categories", "Add Category", "Update Category", "Delete Category"]
        print_menu("Manage Categories", options)
        choice = get_user_choice(len(options))

        if choice == 1: # View Categories
            categories = Category.get_all()
            if not categories:
                print(f"{Fore.YELLOW}No categories found.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}--- All Categories ---{Style.RESET_ALL}")
                for cat in categories:
                    print(f"ID: {cat.id}, Name: {cat.name}")

        elif choice == 2: # Add Category
            name = input(f"{Fore.GREEN}Enter new category name: {Style.RESET_ALL}")
            if name:
                new_cat = Category.create(name)
                if new_cat:
                    print(f"{Fore.GREEN}Category '{new_cat.name}' added successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to add category. Name might already exist.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Category name cannot be empty.{Style.RESET_ALL}")

        elif choice == 3: # Update Category
            categories = Category.get_all()
            if not categories:
                print(f"{Fore.RED}No categories to update.{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.CYAN}--- Select Category to Update ---{Style.RESET_ALL}")
            for cat in categories:
                print(f"ID: {cat.id}, Name: {cat.name}")
            
            try:
                cat_id = int(input(f"{Fore.GREEN}Enter ID of category to update: {Style.RESET_ALL}"))
                category = Category.find_by_id(cat_id)
                if category:
                    new_name = input(f"{Fore.GREEN}Enter new name for '{category.name}': {Style.RESET_ALL}")
                    if new_name:
                        if category.update(new_name):
                            print(f"{Fore.GREEN}Category updated successfully!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Failed to update category.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}New name cannot be empty.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Category not found.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid ID. Please enter a number.{Style.RESET_ALL}")

        elif choice == 4: # Delete Category
            categories = Category.get_all()
            if not categories:
                print(f"{Fore.RED}No categories to delete.{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.CYAN}--- Select Category to Delete ---{Style.RESET_ALL}")
            for cat in categories:
                print(f"ID: {cat.id}, Name: {cat.name}")
            
            try:
                cat_id = int(input(f"{Fore.GREEN}Enter ID of category to delete: {Style.RESET_ALL}"))
                category = Category.find_by_id(cat_id)
                if category:
                    confirm = input(f"{Fore.YELLOW}Deleting '{category.name}' will also delete ALL its questions and answers. Continue? (y/N): {Style.RESET_ALL}").lower()
                    if confirm == 'y':
                        if category.delete():
                            print(f"{Fore.GREEN}Category '{category.name}' deleted successfully!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Failed to delete category.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.BLUE}Deletion cancelled.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Category not found.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid ID. Please enter a number.{Style.RESET_ALL}")

        elif choice == 0:
            break
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")


def manage_questions_menu():
    """Handles question management."""
    while True:
        options = ["View Questions", "Add Question", "Update Question", "Delete Question", "Manage Answers for Question"]
        print_menu("Manage Questions", options)
        choice = get_user_choice(len(options))

        if choice == 1: # View Questions
            questions = Question.get_all()
            if not questions:
                print(f"{Fore.YELLOW}No questions found.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}--- All Questions ---{Style.RESET_ALL}")
                for q in questions:
                    category_name = q.category.name if q.category else "N/A"
                    print(f"ID: {q.id}, Category: {category_name}, Question: {q.text}")
                    for ans in q.answers:
                        correct_status = " (Correct)" if ans.is_correct else ""
                        print(f"  - Answer ID: {ans.id}, Text: {ans.text}{correct_status}")

        elif choice == 2: # Add Question
            categories = Category.get_all()
            if not categories:
                print(f"{Fore.RED}No categories available. Please add a category first.{Style.RESET_ALL}")
                continue

            print(f"\n{Fore.CYAN}--- Select Category for New Question ---{Style.RESET_ALL}")
            for cat in categories:
                print(f"ID: {cat.id}, Name: {cat.name}")
            
            try:
                cat_id = int(input(f"{Fore.GREEN}Enter category ID for the new question: {Style.RESET_ALL}"))
                category = Category.find_by_id(cat_id)
                if not category:
                    print(f"{Fore.RED}Category not found.{Style.RESET_ALL}")
                    continue
                
                question_text = input(f"{Fore.GREEN}Enter new question text: {Style.RESET_ALL}")
                if question_text:
                    new_q = Question.create(question_text, category.id)
                    if new_q:
                        print(f"{Fore.GREEN}Question added successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Failed to add question.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Question text cannot be empty.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid ID. Please enter a number.{Style.RESET_ALL}")

        elif choice == 3: # Update Question
            questions = Question.get_all()
            if not questions:
                print(f"{Fore.RED}No questions to update.{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.CYAN}--- Select Question to Update ---{Style.RESET_ALL}")
            for q in questions:
                print(f"ID: {q.id}, Question: {q.text}")
            
            try:
                q_id = int(input(f"{Fore.GREEN}Enter ID of question to update: {Style.RESET_ALL}"))
                question = Question.find_by_id(q_id)
                if question:
                    new_text = input(f"{Fore.GREEN}Enter new text for '{question.text}' (leave blank to keep current): {Style.RESET_ALL}")
                    new_cat_id_str = input(f"{Fore.GREEN}Enter new category ID (leave blank to keep current): {Style.RESET_ALL}")
                    new_cat_id = int(new_cat_id_str) if new_cat_id_str else None

                    if question.update(new_text=new_text if new_text else None, new_category_id=new_cat_id):
                        print(f"{Fore.GREEN}Question updated successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Failed to update question.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Question not found.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid ID or category ID. Please enter numbers.{Style.RESET_ALL}")

        elif choice == 4: # Delete Question
            questions = Question.get_all()
            if not questions:
                print(f"{Fore.RED}No questions to delete.{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.CYAN}--- Select Question to Delete ---{Style.RESET_ALL}")
            for q in questions:
                    print(f"ID: {q.id}, Question: {q.text}")
            
            try:
                q_id = int(input(f"{Fore.GREEN}Enter ID of question to delete: {Style.RESET_ALL}"))
                question = Question.find_by_id(q_id)
                if question:
                    confirm = input(f"{Fore.YELLOW}Deleting '{question.text}' will also delete ALL its answers. Continue? (y/N): {Style.RESET_ALL}").lower()
                    if confirm == 'y':
                        if question.delete():
                            print(f"{Fore.GREEN}Question deleted successfully!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Failed to delete question.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.BLUE}Deletion cancelled.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Question not found.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid ID. Please enter a number.{Style.RESET_ALL}")

        elif choice == 5: # Manage Answers for Question
            manage_answers_menu()

        elif choice == 0:
            break
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

def manage_answers_menu():
    """Handles answer management for a selected question."""
    questions = Question.get_all()
    if not questions:
        print(f"{Fore.RED}No questions to manage answers for.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}--- Select Question to Manage Answers For ---{Style.RESET_ALL}")
    for q in questions:
        print(f"ID: {q.id}, Question: {q.text}")
    
    try:
        q_id = int(input(f"{Fore.GREEN}Enter ID of question: {Style.RESET_ALL}"))
        question = Question.find_by_id(q_id)
        if not question:
            print(f"{Fore.RED}Question not found.{Style.RESET_ALL}")
            return
        
        while True:
            print(f"\n{Fore.CYAN}--- Managing Answers for: '{question.text}' ---{Style.RESET_ALL}")
            current_answers = question.answers
            if not current_answers:
                print(f"{Fore.YELLOW}No answers currently for this question.{Style.RESET_ALL}")
            else:
                for ans in current_answers:
                    correct_status = " (Correct)" if ans.is_correct else ""
                    print(f"  ID: {ans.id}, Text: {ans.text}{correct_status}")
            
            answer_options = ["Add Answer", "Update Answer", "Delete Answer"]
            print_menu(f"Answers for Q ID {question.id}", answer_options)
            ans_choice = get_user_choice(len(answer_options))

            if ans_choice == 1: # Add Answer
                ans_text = input(f"{Fore.GREEN}Enter new answer text: {Style.RESET_ALL}")
                is_correct_str = input(f"{Fore.GREEN}Is this the correct answer? (y/N): {Style.RESET_ALL}").lower()
                is_correct = (is_correct_str == 'y')
                
                if ans_text:
                    new_ans = question.add_answer(ans_text, is_correct)
                    if new_ans:
                        print(f"{Fore.GREEN}Answer added successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Failed to add answer.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Answer text cannot be empty.{Style.RESET_ALL}")

            elif ans_choice == 2: # Update Answer
                if not current_answers:
                    print(f"{Fore.RED}No answers to update.{Style.RESET_ALL}")
                    continue
                try:
                    ans_id = int(input(f"{Fore.GREEN}Enter ID of answer to update: {Style.RESET_ALL}"))
                    answer_to_update = Answer.find_by_id(ans_id)
                    if answer_to_update and answer_to_update.question_id == question.id:
                        new_ans_text = input(f"{Fore.GREEN}Enter new text for '{answer_to_update.text}' (leave blank to keep current): {Style.RESET_ALL}")
                        new_is_correct_str = input(f"{Fore.GREEN}Is it now correct? (y/N, leave blank to keep current): {Style.RESET_ALL}").lower()
                        
                        new_is_correct = None
                        if new_is_correct_str == 'y':
                            new_is_correct = True
                        elif new_is_correct_str == 'n':
                            new_is_correct = False

                        if answer_to_update.update(new_text=new_ans_text if new_ans_text else None, new_is_correct=new_is_correct):
                            print(f"{Fore.GREEN}Answer updated successfully!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Failed to update answer.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Answer not found for this question.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid ID. Please enter a number.{Style.RESET_ALL}")

            elif ans_choice == 3: # Delete Answer
                if not current_answers:
                    print(f"{Fore.RED}No answers to delete.{Style.RESET_ALL}")
                    continue
                try:
                    ans_id = int(input(f"{Fore.GREEN}Enter ID of answer to delete: {Style.RESET_ALL}"))
                    answer_to_delete = Answer.find_by_id(ans_id)
                    if answer_to_delete and answer_to_delete.question_id == question.id:
                        if answer_to_delete.delete():
                            print(f"{Fore.GREEN}Answer deleted successfully!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Failed to delete answer.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Answer not found for this question.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid ID. Please enter a number.{Style.RESET_ALL}")

            elif ans_choice == 0:
                break
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

    except ValueError:
        print(f"{Fore.RED}Invalid question ID. Please enter a number.{Style.RESET_ALL}")

def main_menu():
    """Displays the main application menu."""
    while True:
        options = ["Take Quiz", "Manage Categories", "Manage Questions"]
        print_menu("Main Menu", options)
        choice = get_user_choice(len(options))

        if choice == 1:
            take_quiz_menu()
        elif choice == 2:
            manage_categories_menu()
        elif choice == 3:
            manage_questions_menu()
        elif choice == 0:
            print(f"{Fore.CYAN}Exiting Quiz App. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")