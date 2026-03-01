# Python Vocabulary Quiz

A simple **Python command-line vocabulary quiz** developed as part of a Python coursework project in First Year of Bachelors.

This tool helps users practice English vocabulary by presenting random words with multiple-choice definitions. It demonstrates core Python programming concepts such as file handling, randomness, loops, conditional logic, and user interaction.

---

## 🚀 Features

- Loads vocabulary and definitions from CSV files
- Randomly generates multiple-choice questions
- Provides instant feedback after each answer
- Simple and interactive CLI-based interface
- Lightweight and easy to run

---

## 🧠 How It Works

1. Vocabulary and definition pairs are stored in:
   - `Vocabulary_list.csv`
   - `Vocabulary_set.csv`
2. The script randomly selects words for the quiz session.
3. For each question:
   - 1 correct definition is selected
   - 3 incorrect definitions are randomly chosen as distractors
   - Options are shuffled before displaying
4. The user selects an answer.
5. Immediate feedback is provided.

---

## ▶️ Getting Started

### Prerequisites

- Python 3.x installed on your system

### Installation & Running the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/Ayushi227/python-vocabulary-quiz.git
   ```

2. Navigate into the project directory:
   ```bash
   cd python-vocabulary-quiz
   ```

3. Run the quiz:
   ```bash
   python quiz.py
   ```

4. Follow the on-screen instructions to answer the questions.

---

## 📂 Project Structure

```
.
├── quiz.py                  # Main CLI quiz script
├── Vocabulary_list.csv      # Word-definition dataset
├── Vocabulary_set.csv       # Vocabulary collection
├── templates/               # (Future) web interface templates
├── static/                  # (Future) static files
├── manage.py                # (Future) web backend entry point
└── README.md
```

---

## 🎯 Learning Outcomes

This project demonstrates:

- Reading and parsing CSV files
- Working with lists and dictionaries
- Using the `random` module
- Implementing quiz logic
- Handling user input and validation
- Structuring a Python project

---

## 📈 Future Improvements

- Add scoring summary at the end of the quiz
- Track high scores
- Convert into a web application (Flask/Django)
- Add grammar-checking feature
- Improve UI/UX
- Add difficulty levels

---

## 📌 Acknowledgment

This project was developed as part of academic coursework to apply Python programming concepts in a practical, interactive application.
