from flask import Flask, request, render_template
from transition_function import transition_function

# inisialisasi class
class SingleTapeTuringMachine:
    def __init__(self, initial_state, accepting_states, transition_function):
        # inisialisasi variable
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function
        self.reset()
        self.isErrors = False

    def reset(self):
        # inisialisasi tape, head dan state
        self.tape = ['B']
        self.head = 0
        self.state = self.initial_state

    def step(self):
        # mengambil simbol saat ini untuk dicari transisinya
        current_symbol = self.tape[self.head]
        # mencari transisinya berdasarkan state dan current symbol
        action = self.transition_function.get((self.state, current_symbol))

        # kondisi jika aksi tidak ada
        if action is None:
            print("Error, No transition execute")
            return False  # Tidak ada transisi

        next_state, write_symbol, move = action
        self.state = next_state
        self.tape[self.head] = write_symbol

        # kondisi movement
        if move == 'R':
            self.head += 1
            if self.head == len(self.tape):
                self.tape.append('B')
        elif move == 'L':
            if self.head == 0:
                self.tape.insert(0, 'B')
            else:
                self.head -= 1

        return True #transition ada

    def execute(self, input_string):
        self.reset()
        self.tape = list(input_string) + ['B']
        self.head = 0

        while self.state not in self.accepting_states:
            if not self.step():
                self.isErrors = True
                break

    def get_tape(self):
        return ''.join(self.tape).strip('B')
    
    def get_errors(self):
        return self.isErrors

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    result_count = 0
    is_errors = False
    if request.method == "POST":
        input_string = request.form["input_string"]

        initial_state = 'q0'
        accepting_states = {'q_accept'}

        single_tape_turing_machine = SingleTapeTuringMachine(initial_state, accepting_states, transition_function)
        single_tape_turing_machine.execute(input_string)
        result = single_tape_turing_machine.get_tape()
        result_count = result.count('0')
        is_errors = single_tape_turing_machine.get_errors()

    return render_template('index.html', result=result, result_count=result_count, isErrors=is_errors)

if __name__ == "__main__":
    app.run(debug=True)
