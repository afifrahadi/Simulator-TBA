# Afif Imam Rahadi (L0122006)
# Tugas Akhir, Case 2

from graphviz import Digraph
from L0122006_Case2 import *
from transition_function import transition_function

# membuat objek diagraph dengan nama diagram
diagram = Digraph()

# membuat start state dan juga terdapat panah di awalnya
diagram.node('start', shape='none', label='')
diagram.edge('start', 'q0', label='start')

# membuat node untuk semua state
states = set()
for (state, _), (next_state, _, _) in transition_function.items():
    states.add(state)
    states.add(next_state)

for state in states:
    shape = 'doublecircle' if state.startswith('q_accept') else 'circle'
    diagram.node(state, shape=shape)

edges = {}

def replace_blanks(symbols):
    return ''.join(['B' if s == ' ' else s for s in symbols])

for (state, symbols), (next_state, writes, moves) in transition_function.items():
    label_symbols = replace_blanks(symbols)
    label_writes = replace_blanks(writes)
    label = f"{label_symbols} / {label_writes}, {''.join(moves)}"
    if (state, next_state) in edges:
        edges[(state, next_state)].append(label)
    else:
        edges[(state, next_state)] = [label]

# menambahkan label pada setiap egde atau panahnya
for (state, next_state), labels in edges.items():
    combined_label = '\n'.join(labels)
    diagram.edge(state, next_state, label=combined_label)

diagram.render('./images/tm_singletape', format='png', cleanup=True)

diagram.view('./images/tm_singletape')


