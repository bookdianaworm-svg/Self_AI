from dataclasses import dataclass, field
from typing import Optional


@dataclass
class KanbanTask:
    id: str
    description: str
    task_type: str
    column: str
    runner_id: Optional[str] = None
    priority: str = 'NORMAL'
    created_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    knowledge_id: Optional[str] = None
    similar_knowledge: list = field(default_factory=list)

    # Column constants
    BACKLOG: str = 'BACKLOG'
    READY: str = 'READY'
    IN_PROGRESS: str = 'IN_PROGRESS'
    DONE: str = 'DONE'
    FAILED: str = 'FAILED'

    # Priority constants
    LOW: str = 'LOW'
    NORMAL: str = 'NORMAL'
    HIGH: str = 'HIGH'
    CRITICAL: str = 'CRITICAL'
