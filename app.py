from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import requests
import sqlite3
from io import BytesIO

app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

# Configura o caminho para o banco de dados SQLite
DB_PATH = os.path.join(app.static_folder, 'db', 'processos.db')

# Certifica-se de que a pasta 'static/db' existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Rota para servir o index.html
@app.route('/')
def index():
    return render_template('index.html')

# Rota para proxy das requisições à API do Escavador
@app.route('/api/processos/<cnj>', methods=['GET'])
def get_processo(cnj):
    url = f"https://api.escavador.com/api/v2/processos/numero_cnj/{cnj}"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return jsonify({'error': 'Processo não encontrado'}), 404
        if not response.ok:
            return jsonify({'error': f'Erro HTTP {response.status_code}: {response.text}'}), response.status_code
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para baixar o banco de dados SQLite
@app.route('/download-db')
def download_db():
    try:
        with open(DB_PATH, 'rb') as f:
            db_data = BytesIO(f.read())
        return send_file(db_data, as_attachment=True, download_name='processos.db', mimetype='application/octet-stream')
    except FileNotFoundError:
        return jsonify({'error': 'Banco de dados não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para salvar os dados no banco de dados SQLite
@app.route('/save-to-db', methods=['POST'])
def save_to_db():
    data = request.json
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Cria as tabelas se não existirem
        cursor.execute('''CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_cnj TEXT UNIQUE,
            titulo_polo_ativo TEXT,
            titulo_polo_passivo TEXT,
            ano_inicio INTEGER,
            data_inicio TEXT,
            estado_origem_nome TEXT,
            estado_origem_sigla TEXT,
            unidade_origem_nome TEXT,
            unidade_origem_cidade TEXT,
            unidade_origem_estado_nome TEXT,
            unidade_origem_estado_sigla TEXT,
            unidade_origem_tribunal_sigla TEXT,
            data_ultima_movimentacao TEXT,
            quantidade_movimentacoes INTEGER,
            fontes_tribunais_estao_arquivadas BOOLEAN,
            data_ultima_verificacao TEXT,
            tempo_desde_ultima_verificacao TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_processo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processo_id INTEGER,
            fonte_id INTEGER,
            processo_fonte_id INTEGER,
            outros_numeros TEXT,
            descricao TEXT,
            nome TEXT,
            sigla TEXT,
            tipo TEXT,
            data_inicio TEXT,
            data_ultima_movimentacao TEXT,
            segredo_justica BOOLEAN,
            arquivado BOOLEAN,
            status_predito TEXT,
            grau INTEGER,
            grau_formatado TEXT,
            fisico BOOLEAN,
            sistema TEXT,
            url TEXT,
            tribunal_id INTEGER,
            tribunal_nome TEXT,
            tribunal_sigla TEXT,
            tribunal_categoria TEXT,
            quantidade_envolvidos INTEGER,
            fontes_data_ultima_verificacao TEXT,
            fontes_quantidade_movimentacoes INTEGER,
            FOREIGN KEY (processo_id) REFERENCES processos(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_capa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fonte_id INTEGER,
            classe TEXT,
            assunto TEXT,
            area TEXT,
            orgao_julgador TEXT,
            situacao TEXT,
            valor_causa_valor TEXT,
            valor_causa_moeda TEXT,
            valor_causa_valor_formatado TEXT,
            data_distribuicao TEXT,
            data_arquivamento TEXT,
            FOREIGN KEY (fonte_id) REFERENCES fontes_processo(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_capa_assuntos_normalizados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fonte_capa_id INTEGER,
            assunto_id INTEGER,
            nome TEXT,
            nome_com_pai TEXT,
            path_completo TEXT,
            categoria_raiz TEXT,
            bloqueado BOOLEAN,
            FOREIGN KEY (fonte_capa_id) REFERENCES fontes_capa(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_capa_informacoes_complementares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fonte_capa_id INTEGER,
            tipo TEXT,
            valor TEXT,
            FOREIGN KEY (fonte_capa_id) REFERENCES fontes_capa(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_envolvidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fonte_id INTEGER,
            nome TEXT,
            quantidade_processos INTEGER,
            tipo_pessoa TEXT,
            prefixo TEXT,
            sufixo TEXT,
            tipo TEXT,
            tipo_normalizado TEXT,
            polo TEXT,
            cpf TEXT,
            cnpj TEXT,
            FOREIGN KEY (fonte_id) REFERENCES fontes_processo(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_envolvidos_advogados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            envolvido_id INTEGER,
            nome TEXT,
            quantidade_processos INTEGER,
            tipo_pessoa TEXT,
            prefixo TEXT,
            sufixo TEXT,
            tipo TEXT,
            tipo_normalizado TEXT,
            polo TEXT,
            cpf TEXT,
            cnpj TEXT,
            FOREIGN KEY (envolvido_id) REFERENCES fontes_envolvidos(id)
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fontes_envolvidos_advogados_oabs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            advogado_id INTEGER,
            uf TEXT,
            tipo TEXT,
            numero INTEGER,
            FOREIGN KEY (advogado_id) REFERENCES fontes_envolvidos_advogados(id)
        )''')

        # Verifica se o processo já existe
        cursor.execute("SELECT id FROM processos WHERE numero_cnj = ?", (data['numero_cnj'],))
        existing = cursor.fetchone()
        if existing:
            return jsonify({'message': f"Processo {data['numero_cnj']} já existe no banco."})

        # Insere os dados do processo
        cursor.execute('''INSERT INTO processos (
            numero_cnj, titulo_polo_ativo, titulo_polo_passivo, ano_inicio, data_inicio,
            estado_origem_nome, estado_origem_sigla, unidade_origem_nome, unidade_origem_cidade,
            unidade_origem_estado_nome, unidade_origem_estado_sigla, unidade_origem_tribunal_sigla,
            data_ultima_movimentacao, quantidade_movimentacoes, fontes_tribunais_estao_arquivadas,
            data_ultima_verificacao, tempo_desde_ultima_verificacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            data.get('numero_cnj', ''),
            data.get('titulo_polo_ativo', ''),
            data.get('titulo_polo_passivo', ''),
            data.get('ano_inicio'),
            data.get('data_inicio', ''),
            data.get('estado_origem', {}).get('nome', ''),
            data.get('estado_origem', {}).get('sigla', ''),
            data.get('unidade_origem', {}).get('nome', ''),
            data.get('unidade_origem', {}).get('cidade', ''),
            data.get('unidade_origem', {}).get('estado', {}).get('nome', ''),
            data.get('unidade_origem', {}).get('estado', {}).get('sigla', ''),
            data.get('unidade_origem', {}).get('tribunal_sigla', ''),
            data.get('data_ultima_movimentacao', ''),
            data.get('quantidade_movimentacoes', 0),
            data.get('fontes_tribunais_estao_arquivadas', False),
            data.get('data_ultima_verificacao', ''),
            data.get('tempo_desde_ultima_verificacao', '')
        ))

        processo_id = cursor.lastrowid

        # Insere as fontes
        if 'fontes' in data and isinstance(data['fontes'], list):
            for fonte in data['fontes']:
                cursor.execute('''INSERT INTO fontes_processo (
                    processo_id, fonte_id, processo_fonte_id, outros_numeros, descricao, nome, sigla, tipo,
                    data_inicio, data_ultima_movimentacao, segredo_justica, arquivado, status_predito,
                    grau, grau_formatado, fisico, sistema, url, tribunal_id, tribunal_nome, tribunal_sigla,
                    tribunal_categoria, quantidade_envolvidos, fontes_data_ultima_verificacao,
                    fontes_quantidade_movimentacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    processo_id,
                    fonte.get('id'),
                    fonte.get('processo_fonte_id'),
                    ','.join(fonte.get('outros_numeros', [])) if isinstance(fonte.get('outros_numeros'), list) else '',
                    fonte.get('descricao', ''),
                    fonte.get('nome', ''),
                    fonte.get('sigla', ''),
                    fonte.get('tipo', ''),
                    fonte.get('data_inicio', ''),
                    fonte.get('data_ultima_movimentacao', ''),
                    fonte.get('segredo_justica', False),
                    fonte.get('arquivado'),
                    fonte.get('status_predito', ''),
                    fonte.get('grau'),
                    fonte.get('grau_formatado', ''),
                    fonte.get('fisico'),
                    fonte.get('sistema', ''),
                    fonte.get('url', ''),
                    fonte.get('tribunal', {}).get('id'),
                    fonte.get('tribunal', {}).get('nome', ''),
                    fonte.get('tribunal', {}).get('sigla', ''),
                    fonte.get('tribunal', {}).get('categoria', ''),
                    fonte.get('quantidade_envolvidos', 0),
                    fonte.get('data_ultima_verificacao', ''),
                    fonte.get('quantidade_movimentacoes', 0)
                ))

                fonte_id = cursor.lastrowid

                # Insere a capa
                if 'capa' in fonte:
                    cursor.execute('''INSERT INTO fontes_capa (
                        fonte_id, classe, assunto, area, orgao_julgador, situacao,
                        valor_causa_valor, valor_causa_moeda, valor_causa_valor_formatado,
                        data_distribuicao, data_arquivamento
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        fonte_id,
                        fonte['capa'].get('classe', ''),
                        fonte['capa'].get('assunto', ''),
                        fonte['capa'].get('area', ''),
                        fonte['capa'].get('orgao_julgador', ''),
                        fonte['capa'].get('situacao', ''),
                        fonte['capa'].get('valor_causa', {}).get('valor', ''),
                        fonte['capa'].get('valor_causa', {}).get('moeda', ''),
                        fonte['capa'].get('valor_causa', {}).get('valor_formatado', ''),
                        fonte['capa'].get('data_distribuicao', ''),
                        fonte['capa'].get('data_arquivamento', '')
                    ))

                    capa_id = cursor.lastrowid

                    # Insere assuntos normalizados
                    if 'assuntos_normalizados' in fonte['capa'] and isinstance(fonte['capa']['assuntos_normalizados'], list):
                        for assunto in fonte['capa']['assuntos_normalizados']:
                            cursor.execute('''INSERT INTO fontes_capa_assuntos_normalizados (
                                fonte_capa_id, assunto_id, nome, nome_com_pai, path_completo, categoria_raiz, bloqueado
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                                capa_id,
                                assunto.get('id'),
                                assunto.get('nome', ''),
                                assunto.get('nome_com_pai', ''),
                                assunto.get('path_completo', ''),
                                assunto.get('categoria_raiz', ''),
                                assunto.get('bloqueado', False)
                            ))

                    # Insere informações complementares
                    if 'informacoes_complementares' in fonte['capa'] and isinstance(fonte['capa']['informacoes_complementares'], list):
                        for info in fonte['capa']['informacoes_complementares']:
                            cursor.execute('''INSERT INTO fontes_capa_informacoes_complementares (
                                fonte_capa_id, tipo, valor
                            ) VALUES (?, ?, ?)''', (
                                capa_id,
                                info.get('tipo', ''),
                                info.get('valor', '')
                            ))

                # Insere os envolvidos
                if 'envolvidos' in fonte and isinstance(fonte['envolvidos'], list):
                    for envolvido in fonte['envolvidos']:
                        cursor.execute('''INSERT INTO fontes_envolvidos (
                            fonte_id, nome, quantidade_processos, tipo_pessoa, prefixo, sufixo, tipo,
                            tipo_normalizado, polo, cpf, cnpj
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                            fonte_id,
                            envolvido.get('nome', ''),
                            envolvido.get('quantidade_processos', 0),
                            envolvido.get('tipo_pessoa', ''),
                            envolvido.get('prefixo', ''),
                            envolvido.get('sufixo', ''),
                            envolvido.get('tipo', ''),
                            envolvido.get('tipo_normalizado', ''),
                            envolvido.get('polo', ''),
                            envolvido.get('cpf', ''),
                            envolvido.get('cnpj', '')
                        ))

                        envolvido_id = cursor.lastrowid

                        # Insere os advogados
                        if 'advogados' in envolvido and isinstance(envolvido['advogados'], list):
                            for advogado in envolvido['advogados']:
                                cursor.execute('''INSERT INTO fontes_envolvidos_advogados (
                                    envolvido_id, nome, quantidade_processos, tipo_pessoa, prefixo, sufixo, tipo,
                                    tipo_normalizado, polo, cpf, cnpj
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                                    envolvido_id,
                                    advogado.get('nome', ''),
                                    advogado.get('quantidade_processos', 0),
                                    advogado.get('tipo_pessoa', ''),
                                    advogado.get('prefixo', ''),
                                    advogado.get('sufixo', ''),
                                    advogado.get('tipo', ''),
                                    advogado.get('tipo_normalizado', ''),
                                    advogado.get('polo', ''),
                                    advogado.get('cpf', ''),
                                    advogado.get('cnpj', '')
                                ))

                                advogado_id = cursor.lastrowid

                                # Insere as informações de OAB
                                if 'oabs' in advogado and isinstance(advogado['oabs'], list):
                                    for oab in advogado['oabs']:
                                        cursor.execute('''INSERT INTO fontes_envolvidos_advogados_oabs (
                                            advogado_id, uf, tipo, numero
                                        ) VALUES (?, ?, ?, ?)''', (
                                            advogado_id,
                                            oab.get('uf', ''),
                                            oab.get('tipo', ''),
                                            oab.get('numero')
                                        ))

        conn.commit()
        conn.close()
        return jsonify({'message': f"Processo {data['numero_cnj']} inserido com sucesso no banco."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)