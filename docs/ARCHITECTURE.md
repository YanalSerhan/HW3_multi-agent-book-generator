# Architecture of CrewAI Multi-Agent Book Generator

This document outlines the software architecture of the system, constructed following Domain-Driven Design (DDD) principles and strict layered separation.

## 1. System Context Diagram

```mermaid
graph TD
    User([User]) --> CLI[Typer CLI Interface]
    CLI --> Crew[CrewAI Workflow]
    
    Crew --> LLM[(OpenAI/Anthropic APIs)]
    Crew --> Search[(Serper/ArXiv APIs)]
    Crew --> LaTeX[Local LaTeX Compiler]
```

## 2. Container Diagram (Layered Architecture)

The system enforces strict unidirectional dependencies from top to bottom.

```mermaid
graph TD
    subgraph "Application Core"
        Agents[CrewAI Agents & Workflows]
        Services[Service Layer\n(Business Logic)]
        SDK[SDK Layer\n(External Wrappers)]
        Domain[Domain Models\n(Entities & State)]
    end
    
    subgraph "Cross-Cutting"
        Gatekeeper[API Gatekeeper\n(Rate Limiting)]
        Observability[Observability\n(Loguru)]
        Config[Config & Settings]
    end

    Agents --> Services
    Services --> SDK
    SDK --> Gatekeeper
    Services --> Domain
    SDK --> Domain
```

## 3. API Gatekeeper Flow

As mandated by the guidelines, all external API traffic must pass through the ApiGatekeeper.

```mermaid
sequenceDiagram
    participant Agent
    participant SDK Client
    participant ApiGatekeeper
    participant External API
    
    Agent->>SDK Client: Call method (e.g. search_web)
    SDK Client->>ApiGatekeeper: execute(func, args)
    
    Note over ApiGatekeeper: Check internal Queue
    alt Queue Full
        ApiGatekeeper-->>SDK Client: Raise RateLimitExceededError
    else Queue Available
        Note over ApiGatekeeper: Enforce limits (Timestamps)
        ApiGatekeeper->>External API: perform request
        External API-->>ApiGatekeeper: HTTP 200 OK
        ApiGatekeeper-->>SDK Client: Return domain object/data
        SDK Client-->>Agent: Return data
    end
```

## 4. Domain Models

All state passes through Pydantic V2 models with strict validation.

```mermaid
classDiagram
    class Article {
        +String title
        +List~String~ authors
        +String abstract
        +List~Chapter~ chapters
    }
    
    class Chapter {
        +Int number
        +String title
        +List~Section~ sections
    }
    
    class Section {
        +String title
        +String content
        +Int word_count
    }
    
    Article "1" *-- "many" Chapter
    Chapter "1" *-- "many" Section
```
