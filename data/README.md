# 📊 data/ - Arquivos de Dados

**Propósito:** Esta pasta contém todos os arquivos de dados do projeto.

---

## 📋 ARQUIVOS

### **banco_dados_infusao.csv**
- **Descrição:** Dados de medicamentos para cálculo de infusão
- **Usado em:** `views/infusao.py`
- **Formato:** CSV (`;` separador, `,` decimal)
- **Encoding:** Latin-1

### **banco_dados_iot.csv**
- **Descrição:** Dados para calculadora de intubação orotraqueal (IOT)
- **Usado em:** `views/intubacao.py`
- **Formato:** CSV (`;` separador, `,` decimal)
- **Encoding:** Latin-1

---

## 🔄 SINCRONIZAÇÃO

Os dados principais estão em **Google Sheets**. Os CSVs aqui são fallback (backup local) caso a conexão falhe.

**Google Sheet:** https://docs.google.com/spreadsheets/d/15Rxc1tYYmgG7Sikn2UOvz-GFN6jvneMHnA-l-O8keNs/

---

## 📝 COMO USAR

Os arquivos são carregados automaticamente pela função `load_data()` em `utils.py`:

```python
from utils import load_data

# Tenta Google Sheets primeiro, usa CSV se falhar
df = load_data('DB_INFUSAO', 'data/banco_dados_infusao.csv')
```

---

## ⚠️ IMPORTANTE

- **NÃO** delete estes arquivos (são fallback necessário)
- **NÃO** versione arquivos grandes de dados aqui
- **SIM** mantenha CSVs atualizados com o Google Sheets
- **SIM** use encoding Latin-1 para compatibilidade

---

## 🔒 DADOS SENSÍVEIS

Se adicionar dados sensíveis (pacientes reais, etc.):
- ✅ Adicione ao `.gitignore`
- ✅ Use variáveis de ambiente
- ✅ Não faça commit

---

**Última atualização:** Janeiro 2026
