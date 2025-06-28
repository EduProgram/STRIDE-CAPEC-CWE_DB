import xml.etree.ElementTree as ET
import json
from collections import OrderedDict
import re

def process_text(text):
    # Substituições de caracteres Unicode
    replacements = {
        '\u0435': 'e', '\u0430': 'a', '\u043c': 'm', '\u0440': 'p', '\u043b': 'l',
        '\u0441': 'c', '\u043e': 'o', '\u0456': 'i'
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    
    # Remover quebras de linha e tabulações, substituindo por espaços
    text = re.sub(r'\s+', ' ', text)
    
    # Remover espaços extras
    text = text.strip()
    
    return text

def process_xhtml_elements(element):
    content = []
    # Primeiro, pegar o texto diretamente do elemento, se houver
    if element.text and element.text.strip():
        content.append(process_text(element.text.strip()))

    # Processar os filhos do elemento (se o elemento for um 'p', 'ul' ou 'div', processar seu conteúdo)
    for child in element:
        if child.tag.endswith('p'):
            content.append(process_text(' '.join(child.itertext()).strip()))
        elif child.tag.endswith('ul'):
            ul_content = []
            for li in child.findall('.//{*}li'):
                ul_content.append('- ' + process_text(' '.join(li.itertext()).strip()))
            content.append('\n'.join(ul_content))
        elif child.tag.endswith('div'):
            div_content = process_text(' '.join(child.itertext()).strip())
            if div_content.startswith('-'):
                content.append(div_content)
            else:
                content.append('- ' + div_content)
    return '\n\n'.join(content)

# Função para converter XML em dicionário (mantendo a estrutura do XML e processando os elementos XHTML)
def xml_to_dict(element):
    if element.tag.endswith('br'):
        return '\n'

    if element.tag.endswith('div'):
        content = []
        for item in element.itertext():
            content.append(process_text(item.strip()))
        return '\n'.join(content)

    result = OrderedDict()
    text = process_text(element.text.strip()) if element.text and element.text.strip() else ''
    
    # Processar atributos
    for key, value in element.attrib.items():
        result[f"_{key}"] = value

    # Tratamento especial para 'Technique', 'Resource', 'Mitigation' e 'Example' no CAPEC
    # Tratamento especial para 'Background_Detail', 'Effectiveness_Notes' no CWE
    # Tratamento especial para 'Extended_Description' e 'Note' para ambos
    if element.tag.endswith(('Description', 'Technique', 'Resource', 'Mitigation', 'Example', 'Background_Detail', 'Effectiveness_Notes', 'Extended_Description', 'Note')):
        combined_text = process_xhtml_elements(element)
        if combined_text:
            if element.attrib:
                result['#text'] = combined_text
                return result
            else:
                return combined_text
        elif text:
            if element.attrib:
                result['#text'] = text
                return result
            else:
                return text
        
    for child in element:
        child_tag = child.tag.split('}')[-1]
        child_data = xml_to_dict(child)
        
        if child_tag in result:
            if isinstance(result[child_tag], list):
                result[child_tag].append(child_data)
            else:
                result[child_tag] = [result[child_tag], child_data]
        else:
            result[child_tag] = child_data

    if text:
        if len(result) > 0:
            result['#text'] = text
        else:
            result = text

    # Tratamento especial para 'Demonstrative_Examples' no CWE
    if element.tag.endswith('Demonstrative_Examples'):
        examples = []
        for example in element.findall('./'):
            example_content = []
            for child in example:
                child_tag = child.tag.split('}')[-1]
                child_data = xml_to_dict(child)
                example_content.append({child_tag: child_data})
                # Mudança no nome do 'div', para identificar que é um código
                if isinstance(child_data, dict) and 'div' in child_data:
                    child_data['#code'] = child_data.pop('div')
            examples.append(example_content)
        return examples

    return result

def process_xml_file(xml_file_path, json_file_path):
    ET.register_namespace('', "http://cwe.mitre.org/cwe-6")
    ET.register_namespace('xhtml', "http://www.w3.org/1999/xhtml")

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    xml_dict = xml_to_dict(root)

    json_data = json.dumps(xml_dict, indent=2, ensure_ascii=False)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print(f"Arquivo JSON criado com sucesso: {json_file_path}")

# Processar o arquivo CAPEC
capec_xml_file = 'capec_v3.9.xml'
capec_json_file = 'capec_v3.9.json'
process_xml_file(capec_xml_file, capec_json_file)

# Processar o arquivo CWE
cwe_xml_file = 'cwec_v4.15.xml'
cwe_json_file = 'cwec_v4.15.json'
process_xml_file(cwe_xml_file, cwe_json_file)