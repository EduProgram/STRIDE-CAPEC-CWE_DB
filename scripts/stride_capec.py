import json
from pymongo import MongoClient
import re

# Conectar ao MongoDB
# Certifique-se de substituir 'USUARIO', 'SENHA' e 'CLUSTER' pelos valores corretos
client = MongoClient('mongodb+srv://USUARIO:SENHA.@CLUSTER.mongodb.net/')
db = client['stride_capec_db']


def sanitize_collection_name(name):
    # Remove caracteres inválidos e limita o tamanho
    return re.sub(r'[^\w\-]', '_', name)[:63]

# Função para processar cada CAPEC
def process_capec(name, data, category):
    capec_id = data.get("link", "").split("/")[-1].replace(".html", "")
    children = list(data.get("children", {}).keys())
    return {
        "id": capec_id,
        "name": name,
        "link": data.get("link", ""),
        "category": category,
        "children": children
    }

# Carregar o arquivo JSON
with open('capec-stride-mapping.json', 'r') as file:
    data = json.load(file)

# Processar os dados
stride_mapping = data["CAPEC S.T.R.I.D.E. Mapping"]
stride_categories = stride_mapping.get("children", {})

# Remover todas as coleções existentes
for collection_name in db.list_collection_names():
    db[collection_name].drop()

for category, category_data in stride_categories.items():
    # Criar uma coleção para cada categoria STRIDE com um nome válido
    collection_name = sanitize_collection_name(category.lower())
    collection = db[collection_name]
    
    def process_capecs(capecs, category):
        for capec_name, capec_data in capecs.items():
            capec = process_capec(capec_name, capec_data, category)
            collection.insert_one(capec)
            
            # Processar recursivamente os filhos
            if "children" in capec_data:
                process_capecs(capec_data["children"], category)

    process_capecs(category_data.get("children", {}), category)

# Fechar a conexão
client.close()