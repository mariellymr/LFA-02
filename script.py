import json

class DFA:
    def __init__(self, states, alphabet, transition, start, final):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition  # dict: (estado, símbolo) -> estado
        self.start = start
        self.final = final

    def _reachable_states(self):
        """Remove estados inalcançáveis."""
        visited = {self.start}
        stack = [self.start]
        while stack:
            s = stack.pop()
            for c in self.alphabet:
                t = self.transition.get((s, c))
                if t and t not in visited:
                    visited.add(t)
                    stack.append(t)
        return visited

    def minimize(self):
        """Executa o algoritmo de minimização (Hopcroft simplificado)."""
        reachable = self._reachable_states()
        states = [s for s in self.states if s in reachable]

        # Partição inicial
        P = [set(self.final), set(states) - set(self.final)]
        W = [set(self.final).copy()]  # Conjuntos a processar

        while W:
            A = W.pop()
            for c in self.alphabet:
                X = {s for s in states if self.transition.get((s, c)) in A}
                for Y in P[:]:
                    inter = X & Y
                    diff = Y - X
                    if inter and diff:
                        P.remove(Y)
                        P.append(inter)
                        P.append(diff)
                        if Y in W:
                            W.remove(Y)
                            W.append(inter)
                            W.append(diff)
                        else:
                            if len(inter) <= len(diff):
                                W.append(inter)
                            else:
                                W.append(diff)

        # Cada conjunto em P é um estado do novo autômato
        new_states = [f"S{i}" for i in range(len(P))]

        # Mapeamento: estado antigo -> novo estado
        mapping = {}
        for i, group in enumerate(P):
            for state in group:
                mapping[state] = new_states[i]

        # Construir novas transições
        new_transition = {}
        for (s, c), t in self.transition.items():
            if s in mapping and t in mapping:
                new_transition[(mapping[s], c)] = mapping[t]

        # Estado inicial e finais no novo autômato
        new_start = mapping[self.start]
        new_final = {mapping[s] for s in self.final if s in mapping}

        return DFA(new_states, self.alphabet, new_transition, new_start, new_final), mapping, P


def carregar_automato_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    transicoes = {}
    for chave, destino in dados["transition"].items():
        # Remove parênteses e divide a chave "(estado,símbolo)"
        chave = chave.strip("()")
        origem, simbolo = chave.split(",")
        transicoes[(origem.strip(), simbolo.strip())] = destino

    return DFA(
        set(dados["states"]),
        set(dados["alphabet"]),
        transicoes,
        dados["start"],
        set(dados["final"])
    )

# Execução principal
if __name__ == "__main__":
    dfa = carregar_automato_json("automato.json")

    print("=== AFD ORIGINAL ===")
    print("Estados:", dfa.states)
    print("Inicial:", dfa.start)
    print("Finais:", dfa.final)
    print("Transições:")
    for (s, c), t in dfa.transition.items():
        print(f"  δ({s}, {c}) -> {t}")

    minimized_dfa, mapping, partitions = dfa.minimize()

    print("\n=== RESULTADO DA MINIMIZAÇÃO ===")
    print("Partições encontradas:")
    for i, group in enumerate(partitions):
        print(f"  S{i}: {group}")

    print("\nMapeamento de estados:")
    for k, v in mapping.items():
        print(f"  {k} -> {v}")

    print("\nNovo AFD minimizado:")
    print("Estados:", minimized_dfa.states)
    print("Inicial:", minimized_dfa.start)
    print("Finais:", minimized_dfa.final)
    print("Transições:")
    for (s, c), t in minimized_dfa.transition.items():
        print(f"  δ({s}, {c}) -> {t}")
