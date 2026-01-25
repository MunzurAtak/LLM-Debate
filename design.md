# CITO LLM – System Specification

## 0. Global Scope

### 0.1 Education Level
Basisonderwijs

### 0.2 Grades
Groep 3–8

### 0.3 Domains
- Rekenen
- Taal

### 0.4 Subdomains
**Rekenen**
- Getallen en bewerkingen
- Meten en meetkunde
- Verhoudingen
- Verbanden

**Taal**
- Begrijpend lezen
- Spelling
- Woordenschat
- Leestekens

### 0.5 Question Types
- Meerkeuzevraag
- Korte open vraag (Alleen rekenen)

### 0.6 Difficulty Levels
- Midden
- Eind

## 1. System Architecture

### 1.1 Global Controller

The Global Controller is responsible for:
- Receiving structured input parameters (domain, grade, difficulty, subskill, question_type)
- Validating inputs against the global scope
- Routing the request to the appropriate domain module
- Enforcing the universal output schema

The Global Controller does not:
- Contain domain-specific knowledge
- Decide difficulty semantics
- Generate content directly

### 1.2 Domain Modules

### Rekenen Module
Responsibilities:
- Interpret difficulty relative to grade (3–8)
- Enforce rekenen-specific constraints
- Select appropriate subskills
- Generate mathematically valid questions

Owned concepts:
- Arithmetic rules
- Grade-level numerical limits
- Step-by-step solutions

### Taal Module
Responsibilities:
- Interpret difficulty relative to grade
- Enforce language complexity
- Select appropriate linguistic subskills

Submodules:
- Begrijpend lezen
- Spelling
- Woordenschat
- Leestekens

### 1.3 Routing Logic

- All requests pass through the Global Controller
- The domain parameter determines which module is activated
- Subdomain handling occurs within the selected domain module
- Outputs are normalized to the universal schema

### 1.4 Explicit Non-Goals

The system explicitly does not attempt to:
- Model individual students
- Adapt difficulty dynamically
- Score real student answers
- Replace official CITO assessments

## Language Policy

- All system design, code, schemas, and evaluation are written in English.
- All LLM prompts instruct the model to respond in Dutch.
- All generated questions and solutions must be in Dutch.
- Language complexity must be appropriate to the specified grade.
