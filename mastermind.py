import random

class Mastermind:
    def __init__(self, num_possible_digits=6, num_digits_to_guess=4):
        self.num_possible_digits = num_possible_digits
        self.num_digits_to_guess = num_digits_to_guess
        self.code = self.generate_code()

    def generate_code(self):
        digits = list(range(self.num_possible_digits))
        random.shuffle(digits)
        return digits[:self.num_digits_to_guess]

    def check_guess(self, guess):
        exact_matches = 0
        partial_matches = 0
        for i in range(self.num_digits_to_guess):
            if guess[i] == self.code[i]:
                exact_matches += 1
            elif guess[i] in self.code:
                partial_matches += 1
        return exact_matches, partial_matches