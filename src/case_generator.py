#!/usr/bin/env python3
"""Multi-model clinical case generator for medical education.

This is the generation engine described in:

    Duarte, D.H. "Generative AI Framework for Dynamic Clinical Case Synthesis:
    Enhancing Diagnostic Reasoning in Medical Education."
    Submitted to JMIR AI, 2026.

The script implements Stages 1-3 of the framework pipeline:
  Stage 1 — Specialty-aware prompt construction (constrained & unconstrained)
  Stage 2 — Parallel case generation across four LLMs
  Stage 3 — Automated metadata tagging and hierarchical file storage

Generated cases should be evaluated using the MedEd-HalluScore safety audit
rubric (Stage 4) before any educational deployment.

Dependencies:
    pip install openai anthropic google-generativeai groq

Environment variables (set only the keys for models you intend to use):
    OPENAI_API_KEY      — for GPT-4o
    ANTHROPIC_API_KEY   — for Claude 3.5 Sonnet
    GEMINI_API_KEY      — for Gemini 1.5 Pro
    GROQ_API_KEY        — for Llama 3 70B (via Groq)

Usage:
    python3 src/case_generator.py

Output:
    resultados_casos_clinicos/
    └── <model>/
        └── <condition>/
            └── <specialty>/
                └── caso_1.txt ... caso_6.txt

Each text file contains the model name, specialty, prompting condition,
the exact prompt used, and the full generated case text.

See also:
    - Safety audit calculator:   src/halluscore_calculator.py
    - Interactive web calculator: https://douglas360.github.io/meded-halluscore/
    - Toolkit DOI:                https://doi.org/10.5281/zenodo.20100687
"""

from __future__ import annotations

import os
import time
from pathlib import Path

def generate_gpt4o(prompt):
    import openai
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def generate_claude(prompt):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.content[0].text

def generate_gemini(prompt):
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    return response.text

def generate_llama3(prompt):
    # Usando a Groq como provedor rápido para o Llama 3 70B (pode ser adaptado para Together AI ou Ollama local)
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def get_prompt(specialty, condition, index):
    base_prompt = f"Você é um médico especialista em {specialty}. Gere um caso clínico sintético original e detalhado para fins educacionais. Este é o caso #{index} desta série, faça-o único."
    
    if condition == "constrained":
        return f"{base_prompt} O caso DEVE seguir ESTRITAMENTE esta estrutura com os respectivos cabeçalhos:\n1. Identificação do Paciente\n2. Queixa Principal\n3. História da Moléstia Atual\n4. Antecedentes Pessoais e Familiares\n5. Exame Físico\n6. Exames Complementares\nNão inclua o diagnóstico final."
    else:
        return f"{base_prompt} Escreva o caso de forma totalmente livre e narrativa, como se estivesse discutindo com um colega em um corredor de hospital, focando no raciocínio clínico e em detalhes contextuais relevantes. Não use estruturação rígida."

def main():
    specialties = [
        "Cardiologia", "Neurologia", "Oncologia", "Pediatria", 
        "Psiquiatria", "Dermatologia", "Endocrinologia", "Gastroenterologia", 
        "Pneumologia", "Reumatologia", "Nefrologia", "Ortopedia"
    ]
    
    models = {
        "gpt-4o": generate_gpt4o,
        "claude-3.5": generate_claude,
        "gemini-1.5-pro": generate_gemini,
        "llama-3-70b": generate_llama3
    }
    
    conditions = ["constrained", "unconstrained"]
    
    # Para chegar próximo de 600 casos no total:
    # 4 modelos * 12 especialidades * 2 condições = 96 combinações
    # Se gerarmos 6 casos por combinação = 576 casos
    # Se gerarmos 7 casos por combinação = 672 casos
    casos_por_combinacao = 6 
    
    output_dir = Path("resultados_casos_clinicos")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    total_gerado = 0
    
    for model_name, generate_fn in models.items():
        print(f"\n[{model_name}] Iniciando geração...")
        model_dir = output_dir / model_name
        model_dir.mkdir(exist_ok=True)
        
        for condition in conditions:
            condition_dir = model_dir / condition
            condition_dir.mkdir(exist_ok=True)
            
            for specialty in specialties:
                specialty_dir = condition_dir / specialty
                specialty_dir.mkdir(exist_ok=True)
                
                print(f"  -> Gerando para {specialty} ({condition})...")
                for i in range(casos_por_combinacao):
                    prompt = get_prompt(specialty, condition, i+1)
                    filename = specialty_dir / f"caso_{i+1}.txt"
                    
                    # Pular se já existir (útil para continuar se a execução falhar no meio)
                    if filename.exists():
                        continue
                        
                    try:
                        case_text = generate_fn(prompt)
                        
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(f"Modelo: {model_name}\n")
                            f.write(f"Especialidade: {specialty}\n")
                            f.write(f"Condição: {condition}\n")
                            f.write(f"Prompt:\n{prompt}\n\n{'='*50}\n\n")
                            f.write(case_text)
                            
                        total_gerado += 1
                        
                        # Pausa para evitar rate limits das APIs
                        time.sleep(2) 
                    except Exception as e:
                        print(f"    [Erro] Falha ao gerar caso {i+1} para {specialty} com {model_name}: {e}")
                        time.sleep(5) # Pausa maior em caso de erro

    print(f"\nFinalizado! Total de novos casos gerados nesta sessão: {total_gerado}")

if __name__ == "__main__":
    main()
