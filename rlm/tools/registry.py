# Tool Registry Implementation
import importlib.util
import tempfile
import os
import sys
import ast
import uuid
import threading
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ToolStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"


class ToolType(Enum):
    ANALYSIS = "analysis"
    TRANSFORMATION = "transformation"
    VALIDATION = "validation"
    GENERATION = "generation"
    UTILITY = "utility"


@dataclass
class ToolParameter:
    name: str
    type_hint: str
    required: bool
    description: str
    default_value: Any = None


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: List[ToolParameter]
    implementation: str
    creator: str
    created_at: datetime
    last_used: datetime
    usage_count: int
    status: ToolStatus
    version: str
    tool_type: ToolType
    compatibility: Dict[str, List[str]]


class ToolRegistry:
    """
    Registry for managing tools that can be created dynamically by agents.
    """

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.shared_tools: List[str] = []
        self.agent_tools: Dict[str, List[str]] = {}
        self.pending_approval: List[str] = []
        self.approved_tools: List[str] = []
        self.tool_modules: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def register_tool(self, tool_def: ToolDefinition) -> bool:
        """Register a new tool in the registry."""
        if not self._validate_implementation(tool_def.implementation):
            return False

        if tool_def.name in self.tools:
            return False

        with self._lock:
            self.tools[tool_def.name] = tool_def

            if tool_def.status == ToolStatus.APPROVED:
                self.approved_tools.append(tool_def.name)
            else:
                self.pending_approval.append(tool_def.name)

            self._load_tool_module(tool_def)

        return True

    def _validate_implementation(self, implementation: str) -> bool:
        """Validate tool implementation for safety and syntax."""
        try:
            ast.parse(implementation)

            dangerous = [
                "__import__",
                "eval",
                "exec",
                "compile",
                "open",
                "input",
                "raw_input",
                "subprocess",
                "os.system",
                "shutil.rmtree",
            ]
            for pattern in dangerous:
                if pattern in implementation:
                    return False
            return True
        except SyntaxError:
            return False

    def _load_tool_module(self, tool_def: ToolDefinition):
        """Load tool implementation as a module."""
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(tool_def.implementation)
                temp_path = f.name

            spec = importlib.util.spec_from_file_location(tool_def.name, temp_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.tool_modules[tool_def.name] = module

            def cleanup():
                import time

                time.sleep(30)
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

            threading.Thread(target=cleanup, daemon=True).start()
        except Exception:
            pass

    def get_tool(self, tool_name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name."""
        return self.tools.get(tool_name)

    def get_tool_function(self, tool_name: str) -> Optional[Callable]:
        """Get the callable function for a tool."""
        if tool_name in self.tool_modules:
            module = self.tool_modules[tool_name]
            if hasattr(module, tool_name):
                return getattr(module, tool_name)
        return None

    def approve_tool(self, tool_name: str) -> bool:
        """Approve a tool for use."""
        if tool_name not in self.tools:
            return False

        with self._lock:
            tool = self.tools[tool_name]
            tool.status = ToolStatus.APPROVED

            if tool_name in self.pending_approval:
                self.pending_approval.remove(tool_name)

            if tool_name not in self.approved_tools:
                self.approved_tools.append(tool_name)

        return True

    def reject_tool(self, tool_name: str) -> bool:
        """Reject a tool."""
        if tool_name not in self.tools:
            return False

        with self._lock:
            tool = self.tools[tool_name]
            tool.status = ToolStatus.REJECTED

            if tool_name in self.pending_approval:
                self.pending_approval.remove(tool_name)

        return True

    def create_dynamic_tool(
        self,
        name: str,
        description: str,
        implementation: str,
        creator_id: str,
        tool_type: ToolType = ToolType.UTILITY,
    ) -> Optional[ToolDefinition]:
        """Create a new tool dynamically from source code."""
        try:
            tree = ast.parse(implementation)
            func_node = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == name:
                    func_node = node
                    break

            if not func_node:
                return None

            parameters = []
            for arg in func_node.args.args[1:]:
                parameters.append(
                    ToolParameter(
                        name=arg.arg,
                        type_hint=str(getattr(arg, "annotation", "Any")),
                        required=True,
                        description=f"Parameter {arg.arg}",
                    )
                )

            tool_def = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters,
                implementation=implementation,
                creator=creator_id,
                created_at=datetime.now(),
                last_used=datetime.now(),
                usage_count=0,
                status=ToolStatus.PENDING,
                version="1.0",
                tool_type=tool_type,
                compatibility={
                    "languages": ["python"],
                    "backends": ["all"],
                    "environments": ["all"],
                },
            )

            if self.register_tool(tool_def):
                return tool_def
            return None

        except Exception:
            return None

    def get_agent_tools(self, agent_id: str) -> List[ToolDefinition]:
        """Get all tools available to an agent."""
        tool_names = set(self.shared_tools)
        if agent_id in self.agent_tools:
            tool_names.update(self.agent_tools[agent_id])
        return [self.tools[n] for n in tool_names if n in self.tools]

    def share_tool(self, tool_name: str, agent_id: str) -> bool:
        """Share a tool with a specific agent."""
        if tool_name not in self.tools:
            return False

        with self._lock:
            if agent_id not in self.agent_tools:
                self.agent_tools[agent_id] = []
            if tool_name not in self.agent_tools[agent_id]:
                self.agent_tools[agent_id].append(tool_name)

        return True

    def make_shared(self, tool_name: str) -> bool:
        """Make a tool available to all agents."""
        if tool_name not in self.tools:
            return False

        with self._lock:
            if tool_name not in self.shared_tools:
                self.shared_tools.append(tool_name)

        return True

    def record_usage(self, tool_name: str):
        """Record that a tool was used."""
        if tool_name in self.tools:
            self.tools[tool_name].usage_count += 1
            self.tools[tool_name].last_used = datetime.now()
