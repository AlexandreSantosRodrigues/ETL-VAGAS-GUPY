print("1. Instalando bibliotecas...")
!pip install selenium webdriver-manager gspread oauth2client pandas > /dev/null

import time
import json
import pandas as pd
import gspread
from kaggle_secrets import UserSecretsClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)


MAPA_ESTADOS = {
    "Acre": ["acre", " ac ", "-ac", "/ac", "(ac)", "rio branco"],
    "Alagoas": ["alagoas", " al ", "-al", "/al", "(al)", "maceio"],
    "Amapá": ["amapá", "amapa", " ap ", "-ap", "/ap", "(ap)", "macapa"],
    "Amazonas": ["amazonas", " am ", "-am", "/am", "(am)", "manaus"],
    "Bahia": ["bahia", " ba ", "-ba", "/ba", "(ba)", "salvador", "camacari", "feira de santana"],
    "Ceará": ["ceará", "ceara", " ce ", "-ce", "/ce", "(ce)", "fortaleza"],
    "Distrito Federal": ["distrito federal", " df ", "-df", "/df", "(df)", "brasilia", "brasília"],
    "Espírito Santo": ["espírito santo", "espirito santo", " es ", "-es", "/es", "(es)", "vitoria", "vitória", "vila velha", "serra - es"],
    "Goiás": ["goiás", "goias", " go ", "-go", "/go", "(go)", "goiania", "aparecida de goiania"],
    "Maranhão": ["maranhão", "maranhao", " ma ", "-ma", "/ma", "(ma)", "sao luis"],
    "Mato Grosso": ["mato grosso", " mt ", "-mt", "/mt", "(mt)", "cuiaba"],
    "Mato Grosso do Sul": ["mato grosso do sul", " ms ", "-ms", "/ms", "(ms)", "campo grande"],
    "Minas Gerais": ["minas gerais", " mg ", "-mg", "/mg", "(mg)", "belo horizonte", "bh", "uberlandia", "contagem", "betim", "juiz de fora"],
    "Pará": ["pará", "para ", " pa ", "-pa", "/pa", "(pa)", "belem"],
    "Paraíba": ["paraíba", "paraiba", " pb ", "-pb", "/pb", "(pb)", "joao pessoa"],
    "Paraná": ["paraná", "parana", " pr ", "-pr", "/pr", "(pr)", "curitiba", "londrina", "maringa", "sao jose dos pinhais"],
    "Pernambuco": ["pernambuco", " pe ", "-pe", "/pe", "(pe)", "recife", "jaboatao", "olinda"],
    "Piauí": ["piauí", "piaui", " pi ", "-pi", "/pi", "(pi)", "teresina"],
    "Rio de Janeiro": ["rio de janeiro", " rj ", "-rj", "/rj", "(rj)", "niteroi", "niterói", "duque de caxias", "nova iguacu"],
    "Rio Grande do Norte": ["rio grande do norte", " rn ", "-rn", "/rn", "(rn)", "natal"],
    "Rio Grande do Sul": ["rio grande do sul", " rs ", "-rs", "/rs", "(rs)", "porto alegre", "caxias do sul", "canoas"],
    "Rondônia": ["rondônia", "rondonia", " ro ", "-ro", "/ro", "(ro)", "porto velho"],
    "Roraima": ["roraima", " rr ", "-rr", "/rr", "(rr)", "boa vista"],
    "Santa Catarina": ["santa catarina", " sc ", "-sc", "/sc", "(sc)", "florianopolis", "blumenau", "joinville", "sao jose - sc"],
    "São Paulo": ["são paulo", "sao paulo", " sp ", " sp,", "-sp", " - sp", "/sp", "/ sp", "(sp)", "barueri", "alphaville", "osasco", "campinas", "guarulhos", "sbc", "bernardo", "santo andre", "sao caetano", "jundiai", "sorocaba", "ribeirao preto", "sao jose dos campos"],
    "Sergipe": ["sergipe", " se ", "-se", "/se", "(se)", "aracaju"],
    "Tocantins": ["tocantins", " to ", "-to", "/to", "(to)", "palmas"]
}

def classificar_local_brasil(texto_completo):
    texto_lower = texto_completo.lower()
    
    if "remoto" in texto_lower or "remote" in texto_lower or "home office" in texto_lower:
        return "Remoto"
    
    for estado_nome, termos in MAPA_ESTADOS.items():
        for termo in termos:
            if termo in texto_lower:
                return estado_nome
                
    return "Outros / Não Identificado"

def identificar_ferramentas(texto_completo):
    texto_lower = texto_completo.lower()
    ferramentas = []
    
    if "power bi" in texto_lower or "pbi" in texto_lower or "powerbi" in texto_lower:
        ferramentas.append("Power BI")
    if "sql" in texto_lower:
        ferramentas.append("SQL")
    if "python" in texto_lower:
        ferramentas.append("Python")
    if "excel" in texto_lower:
        ferramentas.append("Excel")
        
    return ", ".join(ferramentas) if ferramentas else "Geral/Outras"

termos_busca = ["Power BI", "SQL", "Python"]

def buscar_vagas_brasil_corrigido():
    driver = get_driver()
    lista_final = []
    
    print(f"--- INICIANDO ROBÔ (GEOGRAFIA CORRIGIDA) ---")
    
    for termo in termos_busca:
        print(f"\n>> 🔍 Pesquisando: '{termo}'...")
        
        try:
            driver.get("https://portal.gupy.io/")
            time.sleep(3)
            try: driver.find_element(By.XPATH, "//button[contains(text(), 'Aceitar')]").click()
            except: pass

            input_busca = driver.find_element(By.TAG_NAME, "input")
            input_busca.send_keys(Keys.CONTROL + "a")
            input_busca.send_keys(Keys.DELETE)
            time.sleep(0.5)
            input_busca.send_keys(termo)
            time.sleep(1)
            input_busca.send_keys(Keys.RETURN)
            
            print("   ⏳ Carregando...")
            time.sleep(8)
            driver.execute_script("window.scrollTo(0, 1000);")
            
            cards = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="job-list-item"]')
            if len(cards) == 0:
                cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/job/')]")

            print(f"   📋 Cards analisados: {len(cards)}")
            
            for card in cards:
                try:
                    texto_completo = card.text
                    
                    linhas = texto_completo.split('\n')
                    titulo = linhas[0] if len(linhas) > 0 else "Vaga"
                    empresa = linhas[1] if len(linhas) > 1 else "Confidencial"
                    
                    if card.tag_name == 'a': link = card.get_attribute('href')
                    else: link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    local_real = classificar_local_brasil(texto_completo)
                    tools = identificar_ferramentas(texto_completo)
                    
                    lista_final.append({
                        "Vaga": titulo,
                        "Empresa": empresa,
                        "Local": local_real,
                        "Ferramentas": tools,
                        "Link": link,
                        "Data_Coleta": pd.Timestamp.now().strftime('%Y-%m-%d')
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"   Erro: {e}")
            driver.quit()
            driver = get_driver()
            
    driver.quit()
    return pd.DataFrame(lista_final)

df = buscar_vagas_brasil_corrigido()

if not df.empty:
    df_final = df.drop_duplicates(subset=['Link'])
    
    print("\n--- AMOSTRA DA CLASSIFICAÇÃO ---")
    print(df_final[['Vaga', 'Local']].head(10)) 
    print(f"\nTotal: {len(df_final)}")

    try:
        user_secrets = UserSecretsClient()
        creds = json.loads(user_secrets.get_secret("gcp_service_account"))
        gc = gspread.service_account_from_dict(creds)
        sh = gc.open("Vagas_Gupy_RJ") 
        ws = sh.sheet1
        ws.append_rows(df_final.values.tolist())
        print("🚀 SUCESSO! Dados enviados.")
    except Exception as e:
        print(f"Erro Sheets: {e}")
else:
    print("Nenhuma vaga encontrada.")
