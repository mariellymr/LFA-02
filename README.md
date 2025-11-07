# 🧮 Minimização de Autômatos Finitos Determinísticos (AFD)

Este projeto implementa em **Python** um algoritmo para **minimização de autômatos finitos determinísticos (AFDs)**.  
O objetivo é reduzir o número de estados do autômato mantendo o mesmo comportamento (mesmo conjunto de palavras aceitas).

---

## 📘 Visão geral

A minimização de um AFD consiste em **identificar e fundir estados equivalentes**, ou seja, estados que não podem ser distinguidos por nenhuma cadeia de entrada.  
O processo segue estas etapas:

1. **Leitura do autômato** a partir de um arquivo JSON (`automato.json`);
2. **Remoção de estados inalcançáveis** (que nunca são atingidos a partir do estado inicial);
3. **Particionamento de estados** em grupos equivalentes (estados finais e não finais);
4. **Refinamento das partições**, separando estados que reagem diferente a símbolos de entrada;
5. **Construção do autômato minimizado**, com estados equivalentes fundidos.

---

## ⚙️ Estrutura do arquivo `automato.json`

O arquivo `automato.json` descreve um autômato determinístico no seguinte formato:

```json
{
  "estados": ["q0", "q1", "q2", "q3"],
  "alfabeto": ["0", "1"],
  "transicoes": {
    "q0": { "0": "q1", "1": "q2" },
    "q1": { "0": "q0", "1": "q3" },
    "q2": { "0": "q3", "1": "q0" },
    "q3": { "0": "q3", "1": "q3" }
  },
  "estado_inicial": "q0",
  "estados_finais": ["q0"]
}
```
---

## 🧠 Lógica de minimização usada

O algoritmo segue o método clássico de partição:

1. Divide os estados entre finais e não finais;
2. Para cada símbolo do alfabeto, verifica se dois estados têm transições para grupos diferentes;
3. Se sim, eles são separados em partições distintas;
4. O processo se repete até que não haja mais subdivisões possíveis.
5. O resultado é o autômato minimizado equivalente ao original.