# Conversão de Instâncias DIMACS (.col.b → .col)

Este repositório contém os utilitários necessários para converter arquivos binários de grafos no formato DIMACS (`.col.b`) para o formato texto (`.col`), utilizados em problemas de **coloração de grafos**.

As instâncias podem ser obtidas no site oficial:  
🔗 [https://mat.tepper.cmu.edu/COLOR/instances.html#XXCUL](https://mat.tepper.cmu.edu/COLOR/instances.html#XXCUL)

## 🔧 Requisitos

- Sistema Linux ou WSL  
- Compilador C (`gcc`) e `make` instalados


## ⚙️ Como gerar os executáveis

Na pasta onde está o arquivo `binformat.shar`, execute:

```bash
sh binformat.shar
make
```

Isso criará os utilitários necessários:
- asc2bin
- bin2asc
- showpreamble

## 📄 Como converter as instâncias

Para converter um arquivo binário (.col.b) para o formato texto (.col), use o comando:

```bash
./bin2asc {{nome-do-grafo}}.col.b {{nome-do-grafo}}.col
```

O novo arquivo .col poderá então ser aberto, lido ou processado normalmente.

# 📚 Referência
As instâncias e o formato DIMACS foram obtidos do repositório oficial de coloração de grafos da Carnegie Mellon University:

🔗 [https://mat.tepper.cmu.edu/COLOR/instances.html#XXCUL](https://mat.tepper.cmu.edu/COLOR/instances.html#XXCUL)
