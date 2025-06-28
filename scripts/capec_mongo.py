import json
import codecs
from pymongo import MongoClient
from bson import ObjectId

# Conectar ao MongoDB (alterar as credenciais e o cluster conforme necessário)
# Certifique-se de substituir 'USUARIO', 'SENHA' e 'CLUSTER' pelos valores corretos
client = MongoClient('mongodb+srv://USUARIO:SENHA.@CLUSTER.mongodb.net/')
db = client['capec_database']
collection = db['attack_patterns']

def load_json_file(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Carregar o arquivo JSON
try:
    capec_data = load_json_file('capec_v3.9.json')
except Exception as e:
    print(f"Error loading JSON file: {e}")
    exit(1)

# Limpar a coleção existente
collection.delete_many({})
print("Existing collection cleared.")

def process_field(field):
    if isinstance(field, dict):
        return {k: process_field(v) for k, v in field.items()}
    elif isinstance(field, list):
        return [process_field(item) for item in field]
    else:
        return field

def process_and_insert(data, collection):
    if not isinstance(data, list):
        data = [data]
    
    for item in data:
        document = {}
        for key, value in item.items():
            if key.startswith('_'):
                document[key[1:]] = value
            else:
                document[key] = process_field(value)
        collection.insert_one(document)

# Processar e inserir 'Attack Patterns'
attack_patterns_collection = db['attack_patterns']
attack_patterns_collection.delete_many({})
attack_patterns = capec_data.get('Attack_Patterns', {}).get('Attack_Pattern', [])
process_and_insert(attack_patterns, attack_patterns_collection)
print(f"Inserted {attack_patterns_collection.count_documents({})} attack patterns.")

# Processar e inserir 'Categories'
categories_collection = db['categories']
categories_collection.delete_many({})
categories = capec_data.get('Categories', {}).get('Category', [])
process_and_insert(categories, categories_collection)
print(f"Inserted {categories_collection.count_documents({})} categories.")

# Processar e inserir 'Views'
views_collection = db['views']
views_collection.delete_many({})
views = capec_data.get('Views', {}).get('View', [])
process_and_insert(views, views_collection)
print(f"Inserted {views_collection.count_documents({})} views.")

# Processar e inserir 'External References'
external_references_collection = db['external_references']
external_references_collection.delete_many({})
external_references = capec_data.get('External_References', {}).get('External_Reference', [])
process_and_insert(external_references, external_references_collection)
print(f"Inserted {external_references_collection.count_documents({})} external references.")