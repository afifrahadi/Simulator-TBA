from graphviz import Digraph

def state_to_string(state):
    return "".join(sorted(state))

# Inisialisasi variabel dfa_final_states sebagai set
dfa_final_states = set()

# Fungsi epsilon_closure()
def epsilon_closure(states):
    closure = set()
    stack = list(states)
    while stack:
        current_state = stack.pop()
        closure.add(current_state)
        epsilon_transitions = k[s.index(current_state)][-1]  # Transisi epsilon
        for state in epsilon_transitions:
            if state not in closure:
                stack.append(state)
                closure.add(state)
    return closure

# Fungsi move()
def move(states, symbol):
    next_states = set()
    for state in states:
        transitions = k[s.index(state)][t.index(symbol)] 
        next_states.update(transitions)
    epsilon_transitions = epsilon_closure(next_states)
    next_states.update(epsilon_transitions)
    return next_states

# Fungsi get_dfa_states()
def get_dfa_states(nfa_states):
    global dfa_final_states
    dfa_states = []
    queue = [nfa_states]
    while queue:
        current_states = queue.pop(0)
        dfa_states.append(current_states)
        # menambahkan semua final state ke dalam set dfa_final_states
        for state in current_states:
            if state in last:
                dfa_final_states.add(state_to_string(current_states))
                break
        for symbol in t:
            next_states = move(current_states, symbol)
            if next_states not in dfa_states:
                queue.append(next_states)
                dfa_states.append(next_states)
    return dfa_states

# Input pengguna
x = int(input("Enter the number of states: "))
s = [input("Enter the states: ") for i in range(x)]
y = int(input("Enter the number of alphabets: "))
t = [input("Enter the alphabet: ") for j in range(y)]
start = input("Enter the start state: ")
# Mengecek apakah start state valid
if start not in s:
    print("Invalid start state.")
    exit()
last = input("Final States (separated by space): ")

# Matriks k yang berisi transisi antar state NFA
k = [[set() for j in range(len(t) + 1)] for i in range(len(s))]
for i in range(len(s)):
    for j in range(len(t) + 1):
        if j == len(t):  # Transisi epsilon
            k[i][j] = set(input('from ' + s[i] + ' if ε go (separated by space): ').split())
        else:
            k[i][j] = set(input('from ' + s[i] + ' if ' + t[j] + ' go (separated by space): ').split())

# Mendapatkan state DFA
dfa_states = get_dfa_states(epsilon_closure({start}))

# DFA Transition Table
dfa_transitions = {}
for state in dfa_states:
    dfa_transitions[state_to_string(state)] = {}
    for symbol in t:
        next_states = move(state, symbol)
        next_state_string = state_to_string(next_states)
        dfa_transitions[state_to_string(state)][symbol] = next_state_string

# Menampilkan tabel transisi NFA
print("\nNFA Transition Table:")
print("States\t", end="")
for symbol in t + ['ε']:
    print(symbol, "\t", end="")
print()
for i, state in enumerate(s):
    print(state, "\t", end="")
    for j in range(len(t) + 1):
        transitions = k[i][j]
        sorted_transitions = sorted(transitions)  # Sort the transitions for consistent order
        print("".join(sorted_transitions) if sorted_transitions else "-", "\t", end="")
    print()

# Menampilkan tabel transisi DFA
print("\nDFA Transition Table:")
print("States\t", end="")
for symbol in t:
    print(symbol, "\t", end="")
print()
for state, transitions in dfa_transitions.items():
    if(state ==""):print("𝞥\t", end="")
    else:print(state, "\t", end="")
    for symbol in t:
        next_state_string = transitions.get(symbol, None)
        if(next_state_string == ""):print("𝞥\t", end="")
        else: print(next_state_string, "\t", end="")
    print()

# Menampilkan start state 
print("\nStart state of the DFA is : ", state_to_string(dfa_states[0]))
# Menampilkan final states DFA
print("Final states of the DFA are : ", ", ".join(dfa_final_states))

# ==================================================================================
# Buat grafik e-NFA
enfa = Digraph('e-NFA')
enfa.attr(rankdir='LR')


# Tambahkan state
for state in s:
    print(state)
    print(last)
    if state == last:
        enfa.node(state, shape='circle', peripheries='2')
    else:
        enfa.node(state)

# Tambahkan transisi
for i, state in enumerate(s):
    for j in range(len(t) + 1):
        transitions = k[i][j]
        for next_state in transitions:
            enfa.edge(state, next_state, label=t[j] if j < len(t) else 'ε')

enfa.attr('node', shape='none')
enfa.node('')
enfa.edge('', start)

# Simpan grafik e-NFA ke dalam file
enfa_graph = enfa.pipe(format='svg').decode('utf-8')

# Buat grafik DFA
dfa = Digraph('DFA')
dfa.attr(rankdir='LR')

# Tambahkan state
for state in dfa_transitions.keys():
    print("state" + state)
    print(dfa_final_states)
    if state in dfa_final_states:
        dfa.node(state, shape='circle', peripheries='2')  # State accept
    else:
        if (state == ''):
            dfa.node('kosong', shape='circle')
        else:
            dfa.node(state, shape='circle')

# Tambahkan transisi
for state, transitions in dfa_transitions.items():
    for symbol, next_state in transitions.items():
        if next_state == '':
            next_state = "kosong"  # State accept
        if state == '':
            state = "kosong"
        dfa.edge(state, next_state, label=symbol)

dfa.attr('node', shape='none')
dfa.node('')
dfa.edge('', state_to_string(dfa_states[0]))

# Simpan grafik DFA ke dalam file
dfa.render('DFA', format='png', cleanup=True)

print("e-NFA Graph:")
enfa.view()

print("DFA Graph:")
dfa.view()

