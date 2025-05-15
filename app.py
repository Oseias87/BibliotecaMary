from flask import Flask, request, jsonify
import pandas as pd
from difflib import get_close_matches

app = Flask(__name__)

# Dados iniciais da biblioteca
data = [
    {"Título": "O Código Da Vinci", "Autor": "Dan Brown", "Gênero": "aventura e suspense"},
    {"Título": "Garota Exemplar", "Autor": "Gillian Flynn", "Gênero": ""},
    {"Título": "Como Fazer Amigos e Influenciar Pessoas", "Autor": "Dale Carnegie", "Gênero": ""},
    {"Título": "Orgulho e Preconceito", "Autor": "Jane Austen", "Gênero": ""},
    {"Título": "O Hobbit", "Autor": "J.R.R. Tolkien", "Gênero": ""},
    {"Título": "A Culpa é das Estrelas", "Autor": "John Green", "Gênero": ""},
    {"Título": "O Poder do Hábito", "Autor": "Charles Duhigg", "Gênero": ""},
    {"Título": "A Sutil Arte de Ligar o F*da-se", "Autor": "Mark Manson", "Gênero": "autoajuda com linguagem moderna"},
    {"Título": "O Silêncio dos Inocentes", "Autor": "Thomas Harris", "Gênero": ""},
    {"Título": "As Aventuras de Huckleberry Finn", "Autor": "Mark Twain", "Gênero": ""},
    {"Título": "Dom Casmurro", "Autor": "Machado de Assis", "Gênero": "Romance"},
    {"Título": "Nunca Fui Santo - O Livro oficial do Marcos", "Autor": "Mauro Beting", "Gênero": "Bibliografia"},
    {"Título": "Só por hoje e para sempre Renato Russo Diário do recomeço", "Autor": "Renato Russo", "Gênero": "Bibliografia"},
    {"Título": "Bob Marley - Por ele mesmo", "Autor": "Marco Antonio Cardoso", "Gênero": "Bibliografia"},
    {"Título": "O Senhor dos Anéis", "Autor": "J.R.R. Tolkien", "Gênero": "Fantasia e Aventura"},
    {"Título": "The Walking Dead - A Ascensão do governador", "Autor": "Robert Kirkman e Jay Bonansinga", "Gênero": "Terror"},
    {"Título": "The Walking Dead - O caminho para Woodbury", "Autor": "Robert Kirkman e Jay Bonansinga", "Gênero": ""},
    {"Título": "The Walking Dead - A queda do governador", "Autor": "Robert Kirkman e Jay Bonansinga", "Gênero": "Terror"},
]

# Transformar em DataFrame
df = pd.DataFrame(data)

@app.route('/consulta_livros', methods=['GET'])
def consulta_livros():
    # Ordenar pelo Título
    sorted_data = df.sort_values(by="Título").to_dict(orient="records")
    return jsonify(sorted_data)

@app.route('/consulta_titulo', methods=['GET'])
def consulta_titulo():
    titulo = request.args.get('titulo', '')
    # Busca aproximada pelo título
    matched_titles = get_close_matches(titulo, df['Título'].tolist(), n=5, cutoff=0.3)
    result = df[df['Título'].isin(matched_titles)][["Título", "Autor"]].to_dict(orient="records")
    return jsonify(result)

@app.route('/add_livros', methods=['POST'])
def add_livros():
    titulo = request.args.get('titulo', '')
    autor = request.args.get('autor', '')
    genero = request.args.get('genero', '')

    # Adicionar novo livro ao DataFrame
    global df
    new_entry = {"Título": titulo, "Autor": autor, "Gênero": genero}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    return jsonify({"message": "Livro adicionado com sucesso!", "livro": new_entry})

if __name__ == '__main__':
    app.run(debug=True)