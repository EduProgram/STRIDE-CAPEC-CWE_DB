from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient('mongodb+srv://USUARIO:SENHA.@CLUSTER.mongodb.net/')
db_capec = client['capec_database']
db_cwe = client['cwe_database']

# Acessar as coleções
capec_collection = db_capec['attack_patterns']
cwe_collection = db_cwe['Weaknesses']

def print_distinct_options(collection, attribute, description):
    options = collection.distinct(attribute)
    print(f"\nOpções de '{description}':")
    for option in options:
        print(" ", option)

# Usar a função para imprimir as opções distintas (LOCAL_NO_BANCO, NOME_NO_PRINT)
print("Opções possíveis para o CAPEC")
print_distinct_options(capec_collection, 'Abstraction', 'Abstraction')
print_distinct_options(capec_collection, 'Status', 'Status')
print_distinct_options(capec_collection, 'Likelihood_Of_Attack', 'Likelihood_Of_Attack')
print_distinct_options(capec_collection, 'Typical_Severity', 'Typical_Severity')
print_distinct_options(capec_collection, 'Skills_Required.Skill._Level', 'Skill Level')
print_distinct_options(capec_collection, 'Execution_Flow.Attack_Step.Phase', 'Phase of Execution')
print_distinct_options(capec_collection, 'Consequences.Consequence.Scope', 'Scope')
print_distinct_options(capec_collection, 'Consequences.Consequence.Impact', 'Impact')
print_distinct_options(capec_collection, 'Consequences.Consequence.Likelihood', 'Likelihood of Consequence')
print_distinct_options(capec_collection, 'Related_Attack_Patterns.Related_Attack_Pattern._Nature', 'Nature')
print("\n------------------------------------\n")
print("Opções possíveis para o CWE")
print_distinct_options(cwe_collection, 'Abstraction', 'Abstraction')
print_distinct_options(cwe_collection, 'Structure', 'Structure')
print_distinct_options(cwe_collection, 'Status', 'Status')
print_distinct_options(cwe_collection, 'Likelihood_Of_Exploit', 'Likelihood_Of_Exploit')
# print_distinct_options(cwe_collection, 'Modes_Of_Introduction.Introduction.Phase', 'Phase of Introduction')
print_distinct_options(cwe_collection, 'Common_Consequences.Consequence.Scope', 'Scope')
print_distinct_options(cwe_collection, 'Common_Consequences.Consequence.Impact', 'Impact')
print_distinct_options(cwe_collection, 'Common_Consequences.Consequence.Likelihood', 'Likelihood of Consequence')
print_distinct_options(cwe_collection, 'Detection_Methods.Detection_Method.Effectiveness', 'Effectiveness in Detection')
print_distinct_options(cwe_collection, 'Potential_Mitigations.Mitigation.Effectiveness', 'Effectiveness in Mitigation')
print_distinct_options(cwe_collection, 'Related_Weaknesses.Related_Weakness._Nature', 'Nature')
print_distinct_options(cwe_collection, 'Related_Weaknesses.Related_Weakness._Ordinal', 'Ordinal')
print_distinct_options(cwe_collection, 'Weakness_Ordinalities.Weakness_Ordinality.Ordinality', 'Ordinality')
print_distinct_options(cwe_collection, 'Mapping_Notes.Usage', 'Usage')
print_distinct_options(cwe_collection, 'Mapping_Notes.Reasons.Reason._Type', 'Type of Reason')

# Acessar as coleções
capec_views_collection = db_capec['views']
cwe_views_collection = db_cwe['views']

print_distinct_options(capec_views_collection, 'Type', 'Type in CAPEC Views')
print_distinct_options(cwe_views_collection, 'Type', 'Type in CWE Views')