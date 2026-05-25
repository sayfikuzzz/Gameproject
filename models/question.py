import json
import random
import os


class QuestionManager:
    def __init__(self, filepath="assets/questions.json"):
        self.questions = []
        self.used_indices = []
        self.load(filepath)

    def load(self, filepath):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filepath)
        with open(path, encoding="utf-8") as f:
            self.questions = json.load(f)

    def get_random(self):
        available = [i for i in range(len(self.questions)) if i not in self.used_indices]
        if not available:
            self.used_indices.clear()
            available = list(range(len(self.questions)))

        idx = random.choice(available)
        self.used_indices.append(idx)
        q = self.questions[idx]
        options = q["o"][:]
        correct = q["c"]

        pairs = list(enumerate(options))
        random.shuffle(pairs)
        shuffled = [p[1] for p in pairs]
        new_correct = next(i for i, p in enumerate(pairs) if p[0] == correct)

        return {
            "question": q["q"],
            "options": shuffled,
            "correct": new_correct,
            "category": q.get("t", "")
        }
