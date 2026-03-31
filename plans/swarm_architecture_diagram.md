# Self-Improving Swarm System - Architecture Diagram

## High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[User Interface]
        VIZ[Real-time Visualizer]
    end
    
    subgraph "Application Layer"
        MAIN[Main Recursive Instance<br/>(Continuous Orchestrator)]
        AGENT1[Agent 1]
        AGENT2[Agent 2]
        AGENTN[Agent N...]
        
        MAIN -- "Spawns at any time during recursion" --> AGENT1
        MAIN -- "Spawns at any time during recursion" --> AGENT2
        MAIN -- "Spawns at any time during recursion" --> AGENTN
    end
    
    subgraph "State Management Layer"
        REDUX[(Redux Store)]
        AGENT_STATE[Agent State Slice]
        TASK_STATE[Task State Slice]
        MSG_STATE[Message State Slice]
        SYS_STATE[System State Slice]
        IMPROVE_STATE[Improvements State Slice]
    end
    
    subgraph "Communication Layer"
        MSG_BUS[Message Bus]
        INBOX[Shared Inbox]
        OUTBOX[Shared Outbox]
    end
    
    subgraph "Tool Management Layer"
        TOOL_REG[Tool Registry]
        DYN_TOOL[Dynamic Tool Creation]
        SELF_IMPROVE[Self-Improvement System]
    end
    
    UI --> MAIN
    VIZ --> REDUX
    
    MAIN <--> REDUX
    AGENT1 <--> REDUX
    AGENT2 <--> REDUX
    AGENTN <--> REDUX
    
    MAIN <--> MSG_BUS
    AGENT1 <--> MSG_BUS
    AGENT2 <--> MSG_BUS
    AGENTN <--> MSG_BUS
    
    MSG_BUS <--> INBOX
    MSG_BUS <--> OUTBOX
    
    MAIN <--> TOOL_REG
    AGENT1 <--> TOOL_REG
    AGENT2 <--> TOOL_REG
    AGENTN <--> TOOL_REG
    
    TOOL_REG <--> DYN_TOOL
    MAIN <--> SELF_IMPROVE
    AGENT1 <--> SELF_IMPROVE
    AGENT2 <--> SELF_IMPROVE
    AGENTN <--> SELF_IMPROVE
    
    REDUX -.-> |State Updates| VIZ
    MSG_BUS -.-> |Real-time Messages| VIZ
```

## Continuous Agent Spawning Flow

```mermaid
sequenceDiagram
    participant U as User
    participant MAIN as Main Instance
    participant A1 as Agent 1
    participant A2 as Agent 2
    participant A3 as Agent 3
    participant MS as Message System
    participant RS as Redux Store
    
    U->>MAIN: Submit Complex Task
    MAIN->>RS: Initialize Task State
    
    loop Main Instance Recursive Loop
        MAIN->>MAIN: Analyze Progress & Needs
        alt Needs Agent 1
            MAIN->>A1: Spawn Agent 1 (Subtask A)
            A1->>RS: Update Agent State
            A1->>MS: Report Progress
        end
        
        alt Needs Agent 2
            MAIN->>A2: Spawn Agent 2 (Subtask B)
            A2->>RS: Update Agent State
            A2->>MS: Report Progress
        end
        
        alt Needs Agent 3
            MAIN->>A3: Spawn Agent 3 (Subtask C)
            A3->>RS: Update Agent State
            A3->>MS: Report Progress
        end
        
        MAIN->>RS: Update Own Progress
        MAIN->>MS: Share Insights
    end
    
    A1->>MS: Task A Completed
    A2->>MS: Task B Completed
    A3->>MS: Task C Completed
    MS->>MAIN: Notify Completions
    MAIN->>RS: Update Overall Status
    
    MAIN->>U: Task Complete
```

## Self-Improvement Contribution Flow

```mermaid
sequenceDiagram
    participant MAIN as Main Instance
    participant A1 as Agent 1
    participant A2 as Agent 2
    participant IMPRV as Improvement System
    participant TOOL as Tool Registry
    participant RS as Redux Store
    
    par Main Instance Improvement
        MAIN->>MAIN: Discover Process Enhancement
        MAIN->>IMPRV: Register Improvement
        MAIN->>TOOL: Add New Tool
        MAIN->>RS: Update System State
    and Agent 1 Improvement
        A1->>A1: Develop Better Algorithm
        A1->>IMPRV: Contribute Improvement
        A1->>TOOL: Share New Tool
        A1->>RS: Update System State
    and Agent 2 Improvement
        A2->>A2: Optimize Resource Usage
        A2->>IMPRV: Contribute Improvement
        A2->>TOOL: Publish Optimization
        A2->>RS: Update System State
    end
    
    IMPRV->>TOOL: Distribute Improvements
    TOOL->>MAIN: Apply New Tools
    TOOL->>A1: Apply New Tools
    TOOL->>A2: Apply New Tools
```

## Redux State Flow

```mermaid
graph LR
    subgraph "Action Sources"
        USER[User Actions]
        MAIN_INST[Main Instance]
        AGENT[Other Agents]
        SYSTEM[System Events]
    end
    
    subgraph "Redux Store"
        A_STATE[Agent State]
        T_STATE[Task State]
        M_STATE[Message State]
        S_STATE[System State]
        I_STATE[Improvements State]
    end
    
    subgraph "State Consumers"
        VIZ_COMM[Visualization]
        AGENT_COMM[Agent Communication]
        LOGGING[Logging System]
    end
    
    USER --> A_STATE
    USER --> T_STATE
    MAIN_INST --> A_STATE
    MAIN_INST --> T_STATE
    MAIN_INST --> I_STATE
    AGENT --> A_STATE
    AGENT --> M_STATE
    AGENT --> I_STATE
    SYSTEM --> S_STATE
    SYSTEM --> T_STATE
    
    A_STATE --> VIZ_COMM
    T_STATE --> VIZ_COMM
    M_STATE --> VIZ_COMM
    S_STATE --> VIZ_COMM
    I_STATE --> VIZ_COMM
    
    M_STATE --> AGENT_COMM
    A_STATE --> AGENT_COMM
    I_STATE --> AGENT_COMM
```

## Component Interaction Matrix

| Component | Main Instance | Agent | Redux | Message System | Visualization | Tool Registry | Improvement System |
|-----------|---------------|-------|-------|----------------|---------------|---------------|-------------------|
| Main Instance | Self (Recursive) | Spawns as needed | Reads/Writes | Sends/Receives | Provides Data | Creates/Uses | Contributes |
| Agent | Receives from | Self | Reads/Writes | Sends/Receives | Provides Data | Creates/Uses | Contributes |
| Redux | Updates State | Updates State | Core | Notifies | Provides State | Updates State | Updates State |
| Message System | Sends/Receives | Sends/Receives | Notifies | Core | Provides Messages | Routes Messages | Coordinates |
| Visualization | Receives Data | Receives Data | Subscribes | Subscribes | Core | Receives Tools | Receives Improvements |
| Tool Registry | Manages | Uses | Updates | Shares | Displays | Core | Integrates |
| Improvement System | Receives | Receives | Updates | Coordinates | Displays | Integrates | Core |

## Continuous Learning Flow for Complex Task Execution

```mermaid
flowchart TD
    START([User Submits Task]) --> MAIN_LOOP[Main Instance Recursive Loop]
    
    MAIN_LOOP --> ANALYZE[Analyze Current Progress]
    ANALYZE --> DECIDE{Need Additional Agent?}
    
    DECIDE -->|Yes| SPAWN[Spawn Specialized Agent]
    DECIDE -->|No| CONTINUE_SELF[Continue Self Processing]
    
    SPAWN --> A1[Agent 1: Subtask A]
    SPAWN --> A2[Agent 2: Subtask B]
    SPAWN --> AN[Agent N: Subtask ...]
    
    A1 --> UPDATE1[Update Redux State]
    A2 --> UPDATE2[Update Redux State]
    AN --> UPDATEN[Update Redux State]
    
    A1 --> COMM1[Communicate via Message System]
    A2 --> COMM2[Communicate via Message System]
    AN --> COMMN[Communicate via Message System]
    
    UPDATE1 --> VIZ[Visualization Updates]
    UPDATE2 --> VIZ
    UPDATEN --> VIZ
    COMM1 --> VIZ
    COMM2 --> VIZ
    COMMN --> VIZ
    
    A1 --> CHECK1{Task Complete?}
    A2 --> CHECK2{Task Complete?}
    AN --> CHECKN{Task Complete?}
    
    CHECK1 -->|No| A1
    CHECK1 -->|Yes| REPORT1[Report Result to Main]
    CHECK2 -->|No| A2
    CHECK2 -->|Yes| REPORT2[Report Result to Main]
    CHECKN -->|No| AN
    CHECKN -->|Yes| REPORTN[Report Result to Main]
    
    REPORT1 --> MAIN_LOOP
    REPORT2 --> MAIN_LOOP
    REPORTN --> MAIN_LOOP
    
    CONTINUE_SELF --> SELF_CHECK{Self Task Complete?}
    SELF_CHECK -->|No| MAIN_LOOP
    SELF_CHECK -->|Yes| COLLECT[Collect All Results]
    
    COLLECT --> SYNTHESIZE[Synthesize Final Result]
    SYNTHESIZE --> COMPLETE([Task Complete])