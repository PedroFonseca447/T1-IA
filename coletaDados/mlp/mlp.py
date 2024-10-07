from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para codificar o tabuleiro em formato numérico (1 para X, -1 para O, 0 para vazio)
def encode_board(board):
    encoded = []
    for cell in board:
        if cell == 'X':
            encoded.append(1)
        elif cell == 'O':
            encoded.append(-1)
        else:
            encoded.append(0)  # Trata null ou vazio como 0
    return encoded

# Treinar o modelo MLP com o dataset fornecido
def train_model(game_data):
    X = game_data.iloc[:, :-1].values  
    y = game_data.iloc[:, -1].values   
    # Definir e treinar a MLP
    mlp = MLPClassifier(hidden_layer_sizes=(5), max_iter=600)
    mlp.fit(X, y)
    return mlp

# Caminho dos arquivos CSV para treinamento
file_path_game = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\DataSetTreino.csv'  # Estados com "X venceu", "O venceu", e "Empate"

# Ler os arquivos CSV
game_data = pd.read_csv(file_path_game, sep=',')

# Treinar o modelo com o dataset principal
mlp = train_model(game_data)

@app.route('/check_winner', methods=['POST'])
def predict_winner():
    data = request.json
    board = data.get('board', [])

    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400

    # Primeiro, verificamos se ainda há espaços vazios, ou seja, o jogo está em andamento
    if '' in board:
        result = 'Em andamento'
    else:
        # Se o tabuleiro estiver completo, codificar o tabuleiro para o modelo
        encoded_board = np.array([encode_board(board)])
        
        # Fazer a previsão com a MLP
        prediction = mlp.predict(encoded_board)[0]

        # Interpretar a previsão
        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            result = 'Empate'
    
    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
