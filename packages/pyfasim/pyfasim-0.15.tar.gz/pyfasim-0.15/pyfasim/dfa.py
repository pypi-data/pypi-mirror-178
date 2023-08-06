from automata.fa.dfa import DFA
from IPython.display import display, Image, Math, Latex, HTML
#dot = r'c:\Graphviz7.01\bin\dot.exe'

def __dfa_init(self, txt=None, *, states=None, input_symbols=None, transitions=None, initial_state=None, final_states=None, allow_partial=False):
    """Initialize a complete DFA."""
    if txt:
        name, states, input_symbols, transitions, initial_state, final_states, allow_partial = parse_dfa(txt)
        #print(f"name={name}")
        #self.name = name
        self.__dict__['name'] = name
    super(DFA, self).__init__(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
        allow_partial=allow_partial
    )
    object.__setattr__(self, '_word_cache', [])
    object.__setattr__(self, '_count_cache', [])

def diagram(self):
    pd = self.show_diagram()
    if hasattr(self, 'name'):
        name = self.name
    else:
        name = assign_name(self)
    #pngfile = f"d:/cmfl/code/FA/{name}.png"
    pngfile = f"{name}.png"
    pd.write_png(pngfile)
    #pd.write_png(pngfile, prog=dot)
    display(Image(pngfile))

def compseq(self, w):
    #print(f"input={w}")
    it = self.read_input_stepwise(w, ignore_rejection=True)
    i = 0
    #s =  r"\mathbf{%s}" % (self.initial_state,)
    s =  r"\mathbf{%s}" % (next(it),)
    Q = []
    while True:
        try:
            q = next(it)
            s += r"\xrightarrow{\text{\normalsize\bf\;%s\;}}\mathbf{%s}" % (w[i],q)
            #r"\xrightarrow{\text{\;%s\;}}%s" % (w[i],q)
            #s += r"\xrightarrow{%s}%s" % (w[i],q)
            Q.append(q)
            i += 1
        except Exception as e:
            print(e)
            break
    #print(f"Q={Q}")
    if Q[-1] in self.final_states:
        print(f"ACCEPTED: {w}")
    else:
        print(f"REJECTED: {w}")
    display(HTML("<br/>"))
    display(Latex(f'${s}$'))

def words_of_lengths(self, n1, n2=None):
    W = list(self.words_of_length(n1))
    if n2 is None:
        return W
    for n in range(n1+1, n2+1):
        L = list(self.words_of_length(n))
        W.extend(L)
    return W

def random_words(self, m, n=1):
    words = list()
    for i in range(n):
        w = self.random_word(m)
        words.append(w)
    return words
   

DFA.__init__ = __dfa_init
counter = 0
DFA.diagram = diagram
DFA.compseq = compseq
DFA.words_of_lengths = words_of_lengths
DFA.random_words = random_words

#-------------------------------------------

def parse_dfa(text):
    global counter
    allow_partial = False
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line == '' or line[0] == '#':
            continue
        lines.append(line)
    line = lines.pop(0)
    if line.startswith('name:'):
        _,name = line.split()
        line = lines.pop(0)
    else:
        name = f"dfa{counter}"
        counter += 1
    if line.startswith('states:'):
        states = set(line[7:].split())
    else:
        raise Exception("Expected states line..")
    if not states:
        raise Exception("Empty states list .. !?")
    line = lines.pop(0)
    if line.startswith('input_symbols:'):
        input_symbols = set(line[14:].split())
    else:
        raise Exception("Expected input_symbols line..")
    if not input_symbols:
        raise Exception("Empty input_symbols set .. !?")
    trans = lines.pop(0)
    if not trans == "transitions:":
        raise Exception(f"Expected transitions header line: {trans}")

    tlines = []
    initial_state_line = ""
    for _ in range(len(lines)):
        line = lines.pop(0)
        if 'initial_state:' in line:
            initial_state_line = line
            break
        tlines.append(line)
    if initial_state_line == "":
        raise Exception("Expected initial_state line..")

    delta = dict()
    for line in tlines:
        state, d = _parse_trans_line(line)
        delta[state] = d
    _,initial_state = initial_state_line.split()

    line = lines.pop(0)
    if line.startswith('final_states:'):
        final_states = set(line[13:].split())
    else:
        raise Exception("Expected final_states line..")
    return name, states, input_symbols, delta, initial_state, final_states, allow_partial

def _parse_trans_line(line):
    items = line.replace(':', ' ').split()
    if len(items)%2 == 0:
        raise Exception(f"Invalid transitions line: {line}")
    state = items.pop(0)
    d = dict()
    for i in range(0, len(items), 2):
        symbol,nstate = items[i:i+2]
        d[symbol] = nstate
    return state, d

def assign_name(self):
    global counter
    name = f"dfa{counter}"
    self.__dict__['name'] = name
    counter += 1
    return name

