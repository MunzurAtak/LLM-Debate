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
- Multiple choice
- Short answer

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

## 2. Universal Question Schema

All generated questions must conform to the following JSON schema.

```json
{
  "domain": "rekenen | taal",
  "subdomain": "string",
  "grade": 3,
  "difficulty": "midden | eind",
  "question_type": "meerkeuze | open",
  "learning_objective": "string",
  "stimulus": "string | null",
  "question": "string",
  "options": ["string", "string", "string", "string"] | null,
  "correct_answer": "string",
  "worked_solution": "string"
} 
```

### Schema Constraints

- `grade` must be an integer between 3 and 8
- `difficulty` must be either `midden` or `eind`
- `question_type` must be:
  - `meerkeuze` → `options` must contain exactly 4 items
  - `open` → `options` must be null
- `correct_answer` must match one of the options for `meerkeuze`
- `stimulus` is required for:
  - Begrijpend lezen
- `worked_solution` must explain the correct answer step-by-step
- All textual fields must be in Dutch

### Rationale

- `learning_objective` enables curriculum alignment and evaluation
- `stimulus` supports text-based comprehension tasks
- `worked_solution` allows correctness checking and transparency
- A single schema ensures comparability across domains