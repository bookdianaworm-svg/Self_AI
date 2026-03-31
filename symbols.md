# Project Symbols Map


## Overview
- Total branches scanned: 13
- Total Python files: 1092
- Total classes: 2327
- Total functions: 6942

## Branch Summary

### develop
**Purpose**: Development branch
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/agent-framework
**Purpose**: Agent framework implementation
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/backend-diversity
**Purpose**: Backend diversity and multi-language support
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/dynamic-tools
**Purpose**: Dynamic tool discovery and execution
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/messaging-system
**Purpose**: Messaging and communication system
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/redux-state-management
**Purpose**: Redux-style state management
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/self-improvement
**Purpose**: Self-improvement and learning capabilities
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/swarm-orchestration
**Purpose**: Swarm intelligence and orchestration
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/testing-infrastructure
**Purpose**: Testing infrastructure and frameworks
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/verification-system
**Purpose**: Verification and validation system
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### feature/visualization-interface
**Purpose**: Visualization and user interface
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### main
**Purpose**: Main production branch
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

### test-feature
**Purpose**: Test feature branch
**Files**: 84 Python files
**Classes**: 179
**Functions**: 534

## Detailed Symbols by Branch

### develop
**Purpose**: Development branch
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/agent-framework
**Purpose**: Agent framework implementation
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/backend-diversity
**Purpose**: Backend diversity and multi-language support
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/dynamic-tools
**Purpose**: Dynamic tool discovery and execution
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/messaging-system
**Purpose**: Messaging and communication system
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/redux-state-management
**Purpose**: Redux-style state management
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/self-improvement
**Purpose**: Self-improvement and learning capabilities
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/swarm-orchestration
**Purpose**: Swarm intelligence and orchestration
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/testing-infrastructure
**Purpose**: Testing infrastructure and frameworks
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/verification-system
**Purpose**: Verification and validation system
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### feature/visualization-interface
**Purpose**: Visualization and user interface
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### main
**Purpose**: Main production branch
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

### test-feature
**Purpose**: Test feature branch
**Files**: 84
**Classes**: 179
**Functions**: 534

#### File: interactive_ai.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rlm import RLM
- from rlm.logger import RLMLogger
- import json
- import math
- import os
- import time

**Functions**:
- interactive_ai_loop()

#### File: main.py

**Imports**:
- from rlm import RLM
- from rlm.environments import LocalREPL
- from rlm.logger import RLMLogger
- import os

**Functions**:
- main()

#### File: monitor.py

**Imports**:
- from datetime import datetime
- from pathlib import Path
- import json
- import re

**Classes**:
- AIMonitor
  **Methods**:
  - __init__(self)
  - colorize(self, text, color_type)
  - parse_log_line(self, line)
  - display_real_time(self)
  - display_parsed_line(self, parsed)
  - watch_for_ai_thoughts(self)

#### File: monitor_llm_calls.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.layout import Layout
- from rich.live import Live
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- LLMCallMonitor
  **Methods**:
  - __init__(self, log_file_pattern="logs/rlm_*.jsonl")
  - find_latest_log_file(self)
  - parse_llm_query_from_response(self, response_text)
  - monitor_log_file(self)
  - process_log_entry(self, entry)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: monitor_llm_calls_enhanced.py

**Imports**:
- from datetime import datetime
- from rich.console import Console
- from rich.panel import Panel
- from rich.table import Table
- from rich.text import Text
- import json
- import os
- import re
- import threading
- import time

**Classes**:
- EnhancedLLMCallMonitor
  **Methods**:
  - __init__(self)
  - find_latest_files(self)
  - parse_llm_query_from_text(self, text)
  - monitor_rlm_log(self, rlm_file)
  - display_llm_call(self, call)
  - create_dashboard(self)
  - run(self)

#### File: react_tools.py

**Imports**:
- from enum import Enum
- from pathlib import Path
- from pydantic import BaseModel, Field
- from typing import Optional, Dict, Any, List
- import json
- import subprocess

**Classes**:
- ToolName (str, Enum)
- ReActStep (BaseModel)
- ReActResponse (BaseModel)
- ToolExecutor
  **Methods**:
  - __init__(self, base_path: Path)
- ReActAI
  **Methods**:
  - __init__(self, base_path: Path)

#### File: rlm/__init__.py

**Imports**:
- from rlm.core.rlm import RLM
- from rlm.utils.exceptions import (

#### File: rlm/agents/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory

#### File: rlm/agents/prompts/__init__.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (

#### File: rlm/agents/prompts/verification_prompts.py

**Imports**:
- import Mathlib.Data.Real.Basic
- import PhysLib.Physics
- import SciLean.Core

#### File: rlm/agents/verification_agent_factory.py

**Imports**:
- from rlm import RLM
- from rlm.agents.prompts.verification_prompts import (
- from typing import Dict, Any

**Classes**:
- VerificationAgentFactory
  **Methods**:
  - __init__(self, parent_rlm: RLM)

#### File: rlm/clients/__init__.py

**Imports**:
- from dotenv import load_dotenv
- from rlm.clients.anthropic import AnthropicClient
- from rlm.clients.azure_openai import AzureOpenAIClient
- from rlm.clients.base_lm import BaseLM
- from rlm.clients.gemini import GeminiClient
- from rlm.clients.litellm import LiteLLMClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.openai import OpenAIClient
- from rlm.clients.portkey import PortkeyClient
- from rlm.core.types import ClientBackend
- from typing import Any

#### File: rlm/clients/anthropic.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import anthropic

**Classes**:
- AnthropicClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: anthropic.types.Message, model: str)

#### File: rlm/clients/azure_openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- AzureOpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/base_lm.py

**Imports**:
- from abc import ABC, abstractmethod
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- BaseLM (ABC)
  **Methods**:
  - __init__(self, model_name: str, timeout: float = DEFAULT_TIMEOUT, **kwargs)

#### File: rlm/clients/gemini.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from google import genai
- from google.genai import types
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import os

**Classes**:
- GeminiClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: types.GenerateContentResponse, model: str)

#### File: rlm/clients/litellm.py

**Imports**:
- from collections import defaultdict
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import litellm

**Classes**:
- LiteLLMClient (BaseLM)
  **Methods**:
  - _track_cost(self, response, model: str)

#### File: rlm/clients/openai.py

**Imports**:
- from collections import defaultdict
- from dotenv import load_dotenv
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any
- import openai
- import os

**Classes**:
- OpenAIClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: openai.ChatCompletion, model: str)

#### File: rlm/clients/portkey.py

**Imports**:
- from collections import defaultdict
- from portkey_ai import AsyncPortkey, Portkey
- from portkey_ai.api_resources.types.chat_complete_type import ChatCompletions
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary
- from typing import Any

**Classes**:
- PortkeyClient (BaseLM)
  **Methods**:
  - _track_cost(self, response: ChatCompletions, model: str)

#### File: rlm/core/__init__.py

#### File: rlm/core/comms_utils.py

**Imports**:
- from dataclasses import dataclass
- from rlm.core.types import RLMChatCompletion
- from typing import Any
- import json
- import socket
- import struct

**Classes**:
- LMRequest
- LMResponse

#### File: rlm/core/lm_handler.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.comms_utils import LMRequest, LMResponse, socket_recv, socket_send
- from rlm.core.types import RLMChatCompletion, UsageSummary
- from socketserver import StreamRequestHandler, ThreadingTCPServer
- from threading import Thread
- import asyncio
- import time

**Classes**:
- LMRequestHandler (StreamRequestHandler)
  **Methods**:
  - handle(self)
  - async run_all()
- ThreadingLMServer (ThreadingTCPServer)
- LMHandler
  **Methods**:
  - stop(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)

#### File: rlm/core/rlm.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
- from rlm.clients import BaseLM, get_client
- from rlm.core.lm_handler import LMHandler
- from rlm.core.types import (
- from rlm.environments import BaseEnv, SupportsPersistence, get_environment
- from rlm.logger import RLMLogger, VerbosePrinter
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from rlm.utils.exceptions import (
- from rlm.utils.parsing import (
- from rlm.utils.prompts import (
- from rlm.utils.rlm_utils import filter_sensitive_keys
- from rlm.utils.token_utils import count_tokens, get_context_limit
- from typing import Any
- import time

**Classes**:
- RLM
  **Methods**:
  - _spawn_completion_context(self, prompt: str | dict[str, Any])

#### File: rlm/core/types.py

**Imports**:
- from dataclasses import dataclass
- from types import ModuleType
- from typing import Any, Literal
- import json
- import json

**Classes**:
- ModelUsageSummary
  **Methods**:
  - to_dict(self)
- UsageSummary
  **Methods**:
  - to_dict(self)
- RLMChatCompletion
  **Methods**:
  - to_dict(self)
- REPLResult
  **Methods**:
  - __str__(self)
  - to_dict(self)
- CodeBlock
  **Methods**:
  - to_dict(self)
- RLMIteration
  **Methods**:
  - to_dict(self)
- RLMMetadata
  **Methods**:
  - to_dict(self)
- QueryMetadata
  **Methods**:
  - __init__(self, prompt: str | list[str] | dict[Any, Any] | list[dict[Any, Any]])

#### File: rlm/environments/__init__.py

**Imports**:
- from rlm.environments.base_env import (
- from rlm.environments.daytona_repl import DaytonaREPL
- from rlm.environments.docker_repl import DockerREPL
- from rlm.environments.e2b_repl import E2BREPL
- from rlm.environments.local_repl import LocalREPL
- from rlm.environments.modal_repl import ModalREPL
- from rlm.environments.prime_repl import PrimeREPL
- from typing import Any, Literal

#### File: rlm/environments/base_env.py

**Imports**:
- from abc import ABC, abstractmethod
- from dataclasses import dataclass
- from rlm.core.types import REPLResult
- from typing import Any, Protocol, runtime_checkable

**Classes**:
- ToolInfo
- SupportsCustomTools (Protocol)
- BaseEnv (ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, depth: int = 1, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- IsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- NonIsolatedEnv (BaseEnv, ABC)
  **Methods**:
  - __init__(self, persistent: bool = False, **kwargs)
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
- SupportsPersistence (Protocol)

#### File: rlm/environments/constants.py

#### File: rlm/environments/daytona_repl.py

**Imports**:
- from daytona import (
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv, extract_tool_value, validate_custom_tools
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- DaytonaREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/docker_repl.py

**Imports**:
- from http.server import BaseHTTPRequestHandler, HTTPServer
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import NonIsolatedEnv
- import base64
- import dill
- import json
- import os
- import pickle as dill
- import shutil
- import subprocess
- import sys, io, json, base64, traceback, os, requests
- import tempfile
- import textwrap
- import threading
- import time

**Classes**:
- LLMProxyHandler (BaseHTTPRequestHandler)
  **Methods**:
  - log_message(self, *args)
  - do_POST(self)
  - _respond(self, status: int, data: dict)
- DockerREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, *args)
  - __del__(self)

**Functions**:
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(s)
- FINAL_VAR(name)
- SHOW_VARS()

#### File: rlm/environments/e2b_repl.py

**Imports**:
- from e2b_code_interpreter import Sandbox
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- E2BREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)

#### File: rlm/environments/layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from typing import Optional, Dict, Any
- import os
- import psutil
- import subprocess
- import time

**Classes**:
- Layer1Bootstrap
  **Methods**:
  - __init__(self, layer1_path: Optional[str] = None)

#### File: rlm/environments/local_repl.py

**Imports**:
- from collections.abc import Callable
- from contextlib import contextmanager
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import (
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from typing import Any, Optional
- import copy
- import io
- import json
- import os
- import shutil
- import sys
- import tempfile
- import threading
- import time
- import uuid
- import warnings

**Classes**:
- LocalREPL (NonIsolatedEnv)
  **Methods**:
  - setup(self)
  - load_context(self, context_payload: dict | list | str)
  - _capture_output(self)
  - _temp_cwd(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - cleanup(self)
  - __del__(self)

#### File: rlm/environments/modal_repl.py

**Imports**:
- from flask import Flask, request, jsonify
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import modal
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- ModalREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/environments/prime_repl.py

**Imports**:
- from dotenv import load_dotenv
- from flask import Flask, request, jsonify
- from prime_sandboxes import (
- from rlm.core.comms_utils import LMRequest, send_lm_request, send_lm_request_batched
- from rlm.core.types import REPLResult, RLMChatCompletion
- from rlm.environments.base_env import IsolatedEnv
- from rlm.environments.constants import APT_PACKAGES, PIP_PACKAGES
- from typing import Any
- import base64
- import base64
- import dill
- import io
- import json
- import json
- import json
- import os
- import pickle as dill
- import requests
- import requests
- import sys
- import textwrap
- import threading
- import threading
- import time
- import traceback
- import uuid

**Classes**:
- PrimeREPL (IsolatedEnv)
  **Methods**:
  - setup(self)
  - _wait_for_broker(self, max_attempts: int = 30)
  - _poll_broker(self)
  - load_context(self, context_payload: dict | list | str)
  - cleanup(self)
  - __enter__(self)
  - __exit__(self, exc_type, exc_val, exc_tb)
  - __del__(self)

**Functions**:
- health()
- enqueue()
- get_pending()
- respond()
- llm_query(prompt, model=None)
- llm_query_batched(prompts, model=None)
- load_state()
- save_state(state)
- serialize_locals(state)
- FINAL_VAR(variable_name)
- SHOW_VARS()

#### File: rlm/logger/__init__.py

**Imports**:
- from rlm.logger.rlm_logger import RLMLogger
- from rlm.logger.verbose import VerbosePrinter

#### File: rlm/logger/rlm_logger.py

**Imports**:
- from datetime import datetime
- from rlm.core.types import RLMIteration, RLMMetadata
- import json
- import os
- import uuid

**Classes**:
- RLMLogger
  **Methods**:
  - __init__(self, log_dir: str | None = None, file_name: str = "rlm")

#### File: rlm/logger/verbose.py

**Imports**:
- from rich.console import Console, Group
- from rich.panel import Panel
- from rich.rule import Rule
- from rich.style import Style
- from rich.table import Table
- from rich.text import Text
- from rlm.core.types import CodeBlock, RLMIteration, RLMMetadata
- from typing import Any

**Classes**:
- VerbosePrinter
  **Methods**:
  - __init__(self, enabled: bool = True)

#### File: rlm/redux/__init__.py

**Imports**:
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/middleware/__init__.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware

#### File: rlm/redux/middleware/verification_middleware.py

**Imports**:
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import VerificationActions
- from typing import Callable, Any

**Classes**:
- VerificationMiddleware
  **Methods**:
  - __init__(self, store)
  - _handle_load_layer1(self, action: dict)
  - _handle_verify_theorem(self, action: dict)
  - set_agent_factory(self, agent_factory: VerificationAgentFactory)

#### File: rlm/redux/slices/__init__.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- from rlm.redux.slices.verification_slice import (

#### File: rlm/redux/slices/routing_slice.py

**Imports**:
- from dataclasses import dataclass
- from enum import Enum
- from typing import Any, Dict, List, Optional

**Classes**:
- RoutingDecisionType (Enum)
- RoutingDecision
- BackendMetrics
- RoutingState
  **Methods**:
  - __post_init__(self)
- RoutingActions
  **Methods**:
  - routing_decision_made(decision: RoutingDecision)
  - routing_started(subtask_id: str)
  - routing_completed(subtask_id: str, result: dict)
  - backend_metrics_updated(backend_id: str, metrics: dict)

#### File: rlm/redux/slices/verification_slice.py

**Imports**:
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional, Dict, List

**Classes**:
- VerificationStatus (Enum)
- Layer1State
- TheoremVerification
- VerificationState
- VerificationActions

#### File: rlm/routing/__init__.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor, MetricsStore
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute

#### File: rlm/routing/backend_factory.py

**Imports**:
- from rlm.clients import BaseLM, get_client
- from rlm.core.types import ClientBackend
- from typing import Any, Dict

**Classes**:
- BackendFactory
  **Methods**:
  - __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/backend_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict, Optional
- import os
- import re
- import yaml

**Classes**:
- BackendRoute
- TaskDescriptor
- BackendRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)
- MetricsStore
  **Methods**:
  - __init__(self)

#### File: rlm/routing/environment_factory.py

**Imports**:
- from rlm.core.types import EnvironmentType
- from rlm.environments import BaseEnv, get_environment
- from typing import Any, Dict

**Classes**:
- EnvironmentFactory
  **Methods**:
  - __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None)

#### File: rlm/routing/environment_router.py

**Imports**:
- from dataclasses import dataclass
- from typing import Any, Dict
- import os
- import yaml

**Classes**:
- EnvironmentRoute
- EnvironmentRouter
  **Methods**:
  - __init__(self, config_path: str | None = None)

#### File: rlm/routing/task_descriptor.py

**Imports**:
- from typing import Any, Callable, Dict

#### File: rlm/utils/__init__.py

#### File: rlm/utils/exceptions.py

**Classes**:
- BudgetExceededError (Exception)
  **Methods**:
  - __init__(self, spent: float, budget: float, message: str | None = None)
- TimeoutExceededError (Exception)
- TokenLimitExceededError (Exception)
- ErrorThresholdExceededError (Exception)
- CancellationError (Exception)
  **Methods**:
  - __init__(self, partial_answer: str | None = None, message: str | None = None)

#### File: rlm/utils/parsing.py

**Imports**:
- from rlm.core.types import REPLResult, RLMIteration
- from rlm.environments.base_env import BaseEnv
- from typing import TYPE_CHECKING
- import re

**Functions**:
- convert_context_for_repl(context)

#### File: rlm/utils/prompts.py

**Imports**:
- from rlm.core.types import QueryMetadata
- from rlm.environments.base_env import format_tools_for_prompt
- from typing import Any
- import math
- import textwrap

#### File: rlm/utils/rlm_utils.py

**Imports**:
- from typing import Any

#### File: rlm/utils/token_utils.py

**Imports**:
- from typing import Any
- import tiktoken

#### File: tail_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys
- import time

**Functions**:
- tail_log(log_file)

#### File: test_reflection.py

**Imports**:
- import json
- import subprocess
- import time

**Functions**:
- test_simple_reflection()
- test_complex_reflection()

#### File: tests/__init__.py

#### File: tests/agents/__init__.py

#### File: tests/agents/test_verification_agent_factory.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationAgentFactoryInitialization
  **Methods**:
  - test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock)
  - test_init_without_parent_rlm(self)
- TestAutoformalizationAgentCreation
  **Methods**:
  - test_create_autoformalization_agent(self, mock_rlm_class)
  - test_autoformalization_agent_tools(self, mock_rlm_class)
- TestVerifierAgentCreation
  **Methods**:
  - test_create_verifier_agent(self, mock_rlm_class)
  - test_verifier_agent_tools(self, mock_rlm_class)
- TestPhysicistAgentCreation
  **Methods**:
  - test_create_physicist_agent(self, mock_rlm_class)
  - test_physicist_agent_tools(self, mock_rlm_class)
- TestCrossCheckAgentCreation
  **Methods**:
  - test_create_cross_check_agent(self, mock_rlm_class)
  - test_cross_check_agent_tools(self, mock_rlm_class)
- TestAgentConfiguration
  **Methods**:
  - test_backend_inheritance(self, mock_rlm_class)
  - test_depth_inheritance(self, mock_rlm_class)
  - test_max_depth_inheritance(self, mock_rlm_class)
  - test_logger_inheritance(self, mock_rlm_class)
  - test_verbose_disabled(self, mock_rlm_class)
- TestMultipleAgentCreation
  **Methods**:
  - test_create_multiple_agents(self, mock_rlm_class)
- TestErrorHandling
  **Methods**:
  - test_rlm_creation_exception(self, mock_rlm_class)
  - test_create_agent_with_none_research_output(self, mock_rlm_class)

#### File: tests/agents/test_verification_prompts.py

**Imports**:
- from rlm.agents.prompts.verification_prompts import (
- import pytest

**Classes**:
- TestAutoformalizationPrompt
  **Methods**:
  - test_autoformalization_prompt_exists(self)
  - test_autoformalization_prompt_content(self)
  - test_autoformalization_prompt_responsibilities(self)
  - test_autoformalization_prompt_output_format(self)
  - test_autoformalization_prompt_tools(self)
- TestVerifierPrompt
  **Methods**:
  - test_verifier_prompt_exists(self)
  - test_verifier_prompt_content(self)
  - test_verifier_prompt_responsibilities(self)
  - test_verifier_prompt_tools(self)
  - test_verifier_prompt_output_format(self)
- TestPhysicistPrompt
  **Methods**:
  - test_physicist_prompt_exists(self)
  - test_physicist_prompt_content(self)
  - test_physicist_prompt_responsibilities(self)
  - test_physicist_prompt_constraints(self)
  - test_physicist_prompt_tools(self)
  - test_physicist_prompt_output_format(self)
- TestCrossCheckPrompt
  **Methods**:
  - test_cross_check_prompt_exists(self)
  - test_cross_check_prompt_content(self)
  - test_cross_check_prompt_responsibilities(self)
  - test_cross_check_prompt_tools(self)
- TestPromptConsistency
  **Methods**:
  - test_all_prompts_use_lean(self)
  - test_all_prompts_use_layer1(self)
  - test_all_prompts_specify_output_format(self)
  - test_all_prompts_mention_tools(self)
- TestPromptQuality
  **Methods**:
  - test_prompts_are_reasonable_length(self)
  - test_prompts_use_clear_language(self)
  - test_prompts_include_examples(self)
- TestEdgeCases
  **Methods**:
  - test_prompts_are_not_empty(self)
  - test_prompts_are_strings(self)
  - test_prompts_contain_printable_characters(self)

#### File: tests/conftest.py

**Imports**:
- from pathlib import Path
- from rlm.agents.verification_agent_factory import VerificationAgentFactory
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
- from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from tests.mock_lm import MockLM, MockLMWithResponse
- from typing import Any, Dict
- from unittest.mock import MagicMock, patch
- import os
- import pytest
- import tempfile

**Functions**:
- pytest_configure(config)
- mock_parent_rlm()
- mock_lean_kernel()
- mock_haskell_compiler()
- caplog_with_level(caplog)

#### File: tests/environments/__init__.py

#### File: tests/environments/test_layer1_bootstrap.py

**Imports**:
- from pathlib import Path
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1BootstrapInitialization
  **Methods**:
  - test_init_with_default_path(self)
  - test_init_with_custom_path(self, temp_dir: Path)
  - test_init_with_none_path(self)
  - test_default_layer1_path_exists(self)
  - test_initial_state(self)
- TestLayer1Loading
  **Methods**:
  - test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_failure(self, mock_lean)
  - test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean)
  - test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean)
- TestLeanKernelLoading
  **Methods**:
  - test_load_lean_kernel_success(self, mock_subprocess)
  - test_load_lean_kernel_failure(self, mock_subprocess)
  - test_load_lean_kernel_timeout(self, mock_subprocess)
- TestPhysLibLoading
  **Methods**:
  - test_load_physlib_success(self)
  - test_load_physlib_with_missing_files(self, temp_dir: Path)
- TestHaskellCompilerSetup
  **Methods**:
  - test_compile_haskell_types_success(self, mock_subprocess)
  - test_compile_haskell_types_failure(self, mock_subprocess)
  - test_compile_haskell_types_timeout(self, mock_subprocess)
- TestVersionRetrieval
  **Methods**:
  - test_get_mathlib_version(self)
  - test_get_physlib_version(self)
- TestMemoryUsage
  **Methods**:
  - test_get_memory_usage(self, mock_psutil)
  - test_get_memory_usage_with_exception(self, mock_psutil)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_partial_failure(self, mock_lean)
  - test_load_layer1_with_invalid_path(self)
- TestEdgeCases
  **Methods**:
  - test_multiple_load_calls(self)
  - test_load_time_tracking(self)

#### File: tests/environments/test_local_repl_layer1.py

**Imports**:
- from rlm.environments.local_repl import LocalREPL
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerifyLeanTool
  **Methods**:
  - test_verify_lean_tool_exists(self)
  - test_verify_lean_simple_code(self, mock_bootstrap)
  - test_verify_lean_with_syntax_error(self, mock_bootstrap)
  - test_verify_lean_complex_theorem(self, mock_bootstrap)
- TestCheckHaskellTypesTool
  **Methods**:
  - test_check_haskell_types_tool_exists(self)
  - test_check_haskell_types_simple(self, mock_bootstrap)
  - test_check_haskell_types_with_dimensional_units(self, mock_bootstrap)
- TestGetLayer1AxiomsTool
  **Methods**:
  - test_get_layer1_axioms_returns_list(self, mock_bootstrap)
  - test_get_layer1_axioms_with_filter(self, mock_bootstrap)
  - test_get_layer1_axioms_before_loading(self, mock_bootstrap)
- TestProveTheoremTool
  **Methods**:
  - test_prove_theorem_simple(self, mock_bootstrap)
  - test_prove_theorem_with_tactics(self, mock_bootstrap)
  - test_prove_theorem_unprovable(self, mock_bootstrap)
- TestLayer1Integration
  **Methods**:
  - test_enable_layer1_flag(self)
  - test_layer1_bootstrap_initialization(self, mock_bootstrap)
  - test_layer1_tools_in_custom_tools(self)
- TestErrorHandling
  **Methods**:
  - test_verify_lean_with_none_input(self, mock_bootstrap)
  - test_prove_theorem_with_empty_string(self, mock_bootstrap)
  - test_layer1_tools_without_layer1_enabled(self, mock_bootstrap)
- TestCleanup
  **Methods**:
  - test_cleanup_releases_resources(self, mock_bootstrap)
- TestEdgeCases
  **Methods**:
  - test_verify_lean_with_very_long_code(self, mock_bootstrap)
  - test_multiple_layer1_tool_calls(self, mock_bootstrap)

**Functions**:
- test_check_haskell_types_with_type_error(self, mock_bootstrap)

#### File: tests/fixtures/__init__.py

#### File: tests/fixtures/sample_tasks.py

**Imports**:
- from rlm.routing.backend_router import TaskDescriptor
- from typing import Any, Dict, List

#### File: tests/integration/__init__.py

#### File: tests/integration/test_backend_routing_flow.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter, TaskDescriptor
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendRoutingFlow
  **Methods**:
  - test_complete_backend_routing_flow(self, mock_route, mock_get_client)
  - test_backend_routing_with_overrides(self, mock_get_client)
  - test_backend_routing_metrics_tracking(self, mock_get_client)
  - test_backend_routing_with_fallback(self, mock_get_client)
- TestBackendRoutingErrorHandling
  **Methods**:
  - test_backend_routing_with_client_error(self, mock_get_client)
  - test_backend_routing_with_execution_error(self, mock_get_client)
- TestBackendRoutingEdgeCases
  **Methods**:
  - test_backend_routing_with_empty_prompt(self, mock_get_client)
  - test_backend_routing_with_very_long_prompt(self, mock_get_client)
  - test_backend_routing_concurrent_calls(self, mock_get_client)
- TestBackendRoutingIntegration
  **Methods**:
  - test_backend_routing_with_task_descriptor(self, mock_get_client)
  - test_backend_routing_with_depth(self, mock_get_client)

#### File: tests/integration/test_combined_routing.py

**Imports**:
- from rlm.routing.backend_factory import BackendFactory
- from rlm.routing.backend_router import BackendRouter
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestCombinedRoutingFlow
  **Methods**:
  - test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment)
  - test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingConflicts
  **Methods**:
  - test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment)
  - test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingErrorHandling
  **Methods**:
  - test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment)
  - test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment)
- TestCombinedRoutingEdgeCases
  **Methods**:
  - test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment)
  - test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment)

#### File: tests/integration/test_environment_routing_flow.py

**Imports**:
- from rlm.routing.environment_factory import EnvironmentFactory
- from rlm.routing.environment_router import EnvironmentRouter
- from rlm.routing.task_descriptor import default_task_descriptor_fn
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentRoutingFlow
  **Methods**:
  - test_complete_environment_routing_flow(self, mock_route, mock_get_environment)
  - test_environment_routing_with_lean_access(self, mock_get_environment)
  - test_environment_routing_with_internet_access(self, mock_get_environment)
  - test_environment_routing_with_sensitive_data(self, mock_get_environment)
- TestEnvironmentRoutingErrorHandling
  **Methods**:
  - test_environment_routing_with_creation_error(self, mock_get_environment)
  - test_environment_routing_with_execution_error(self, mock_get_environment)
- TestEnvironmentRoutingEdgeCases
  **Methods**:
  - test_environment_routing_with_empty_prompt(self, mock_get_environment)
  - test_environment_routing_with_very_long_prompt(self, mock_get_environment)
  - test_environment_routing_concurrent_calls(self, mock_get_environment)
- TestEnvironmentRoutingSecurity
  **Methods**:
  - test_security_override_routing_decision(self, mock_get_environment)
  - test_security_with_public_data(self, mock_get_environment)
- TestEnvironmentRoutingIntegration
  **Methods**:
  - test_environment_routing_with_task_descriptor(self, mock_get_environment)
  - test_environment_routing_with_depth(self, mock_get_environment)

#### File: tests/integration/test_layer1_verification_flow.py

**Imports**:
- from rlm.environments.layer1_bootstrap import Layer1Bootstrap
- from rlm.redux.slices.verification_slice import (
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestLayer1LoadingFlow
  **Methods**:
  - test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean)
  - test_layer1_loading_failure_flow(self, mock_lean)
  - test_layer1_loading_cached_flow(self)
- TestTheoremVerificationFlow
  **Methods**:
  - test_theorem_verification_success_flow(self, mock_factory)
  - test_theorem_verification_failure_flow(self, mock_factory)
- TestLayer1VerificationIntegration
  **Methods**:
  - test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean)
  - test_verification_without_layer1_loaded(self, mock_factory, mock_lean)
- TestLayer1VerificationErrorHandling
  **Methods**:
  - test_layer1_load_error_propagation(self, mock_lean)
  - test_verification_agent_creation_error(self, mock_factory)
- TestLayer1VerificationEdgeCases
  **Methods**:
  - test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean)
  - test_multiple_theorem_verifications(self, mock_factory)
  - test_verification_with_duplicate_theorem_id(self, mock_factory)
- TestLayer1VerificationQueue
  **Methods**:
  - test_verification_queue_management(self, mock_factory)

#### File: tests/mock_lm.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.core.types import ModelUsageSummary, UsageSummary

**Classes**:
- MockLM (BaseLM)
  **Methods**:
  - __init__(self, model_name: str = "mock-model")
- MockLMWithResponse (BaseLM)
  **Methods**:
  - __init__(self, responses: dict[str, str], model_name: str = "mock-with-response")

#### File: tests/redux/__init__.py

#### File: tests/redux/test_routing_slice.py

**Imports**:
- from rlm.redux.slices.routing_slice import (
- import pytest

**Classes**:
- TestRoutingState
  **Methods**:
  - test_routing_state_initialization(self)
  - test_routing_state_with_values(self)
  - test_routing_state_post_init(self)
- TestRoutingDecision
  **Methods**:
  - test_routing_decision_creation(self)
  - test_routing_decision_type_enum(self)
- TestBackendMetrics
  **Methods**:
  - test_backend_metrics_creation(self)
  - test_backend_metrics_calculations(self)
- TestRoutingActions
  **Methods**:
  - test_routing_decision_made_action(self)
  - test_routing_started_action(self)
  - test_routing_completed_action(self)
  - test_backend_metrics_updated_action(self)
- TestRoutingReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_routing_decision_made(self)
  - test_reducer_routing_started(self)
  - test_reducer_routing_completed(self)
  - test_reducer_backend_metrics_updated(self)
  - test_reducer_unknown_action(self)
  - test_reducer_immutability(self)
- TestStateTransitions
  **Methods**:
  - test_routing_flow_state_transitions(self)
  - test_multiple_routing_decisions(self)

#### File: tests/redux/test_verification_middleware.py

**Imports**:
- from rlm.redux.middleware.verification_middleware import VerificationMiddleware
- from rlm.redux.slices.verification_slice import VerificationActions
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestVerificationMiddlewareInitialization
  **Methods**:
  - test_init_with_store(self)
  - test_init_without_store(self)
- TestMiddlewareCallPattern
  **Methods**:
  - test_middleware_returns_function(self)
  - test_middleware_returns_dispatch(self)
- TestLayer1LoadingHandling
  **Methods**:
  - test_handle_load_layer1_success(self, mock_bootstrap)
  - test_handle_load_layer1_failure(self, mock_bootstrap)
  - test_handle_load_layer1_with_custom_path(self, mock_bootstrap)
  - test_handle_load_layer1_exception(self, mock_bootstrap)
- TestTheoremVerificationHandling
  **Methods**:
  - test_handle_verify_theorem_success(self, mock_factory)
  - test_handle_verify_theorem_failure(self, mock_factory)
  - test_handle_verify_theorem_with_payload(self, mock_factory)
  - test_handle_verify_theorem_exception(self, mock_factory)
- TestActionInterception
  **Methods**:
  - test_intercepts_load_layer1_request(self, mock_bootstrap)
  - test_intercepts_verify_theorem_request(self, mock_factory)
  - test_passes_through_other_actions(self)
- TestErrorHandling
  **Methods**:
  - test_load_layer1_with_bootstrap_error(self, mock_bootstrap)
  - test_verify_theorem_with_factory_error(self, mock_factory)
  - test_middleware_continues_on_error(self)
- TestAgentFactoryIntegration
  **Methods**:
  - test_agent_factory_initialization(self, mock_factory)
  - test_agent_factory_reuse(self, mock_factory)
- TestEdgeCases
  **Methods**:
  - test_middleware_with_none_action(self)
  - test_middleware_with_empty_action(self)
  - test_multiple_load_layer1_requests(self, mock_bootstrap)
  - test_multiple_verify_theorem_requests(self, mock_factory)

#### File: tests/redux/test_verification_slice.py

**Imports**:
- from rlm.redux.slices.verification_slice import (
- import pytest

**Classes**:
- TestVerificationStatus
  **Methods**:
  - test_verification_status_values(self)
- TestLayer1State
  **Methods**:
  - test_layer1_state_initialization(self)
  - test_layer1_state_with_values(self)
  - test_layer1_state_with_error(self)
- TestTheoremVerification
  **Methods**:
  - test_theorem_verification_initialization(self)
  - test_theorem_verification_with_values(self)
  - test_theorem_verification_with_error(self)
- TestVerificationState
  **Methods**:
  - test_verification_state_initialization(self)
  - test_verification_state_with_values(self)
- TestVerificationActions
  **Methods**:
  - test_load_layer1_request_action(self)
  - test_load_layer1_success_action(self)
  - test_load_layer1_failure_action(self)
  - test_verify_theorem_request_action(self)
  - test_verify_theorem_success_action(self)
  - test_verify_theorem_failure_action(self)
- TestVerificationReducer
  **Methods**:
  - test_reducer_initial_state(self)
  - test_reducer_load_layer1_request(self)
  - test_reducer_load_layer1_success(self)
  - test_reducer_load_layer1_failure(self)
  - test_reducer_verify_theorem_request(self)
  - test_reducer_verify_theorem_success(self)
  - test_reducer_verify_theorem_failure(self)
  - test_reducer_unknown_action(self)
- TestStateTransitions
  **Methods**:
  - test_layer1_loading_flow(self)
  - test_theorem_verification_flow(self)
  - test_multiple_theorem_verifications(self)
  - test_layer1_failure_then_retry(self)
- TestEdgeCases
  **Methods**:
  - test_verify_theorem_without_layer1_loaded(self)
  - test_verify_theorem_with_duplicate_id(self)

#### File: tests/routing/__init__.py

#### File: tests/routing/test_backend_factory.py

**Imports**:
- from rlm.clients.base_lm import BaseLM
- from rlm.routing.backend_factory import BackendFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestBackendFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestBackendClientCreation
  **Methods**:
  - test_get_backend_with_config(self, mock_get_client)
  - test_get_backend_with_default_kwargs(self, mock_get_client)
  - test_get_backend_with_no_config_or_default(self, mock_get_client)
  - test_get_backend_config_merging(self, mock_get_client)
- TestBackendIdMapping
  **Methods**:
  - test_map_rlm_internal_to_openai(self)
  - test_map_claude_agent_to_anthropic(self)
  - test_map_openai_gpt_to_openai(self)
  - test_map_gemini_to_gemini(self)
  - test_map_portkey_to_portkey(self)
  - test_map_litellm_to_litellm(self)
  - test_map_unknown_to_openai(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_client_exception_propagation(self, mock_get_client)
  - test_get_client_with_none_backend_id(self, mock_get_client)
  - test_get_client_with_empty_backend_id(self, mock_get_client)
- TestMultipleBackends
  **Methods**:
  - test_create_multiple_backends(self, mock_get_client)
  - test_reuse_backend_config(self, mock_get_client)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)

#### File: tests/routing/test_backend_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor
- from unittest.mock import MagicMock, patch
- import pytest
- import tempfile

**Classes**:
- TestBackendRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestConfigLoading
  **Methods**:
  - test_load_config_from_file(self, temp_dir: Path)
- TestRouteMatching
  **Methods**:
  - test_route_simple_code_task(self, backend_router_with_config)
  - test_route_proof_synthesis_task(self, backend_router_with_config)
  - test_route_cost_sensitive_task(self, backend_router_with_config)
  - test_route_with_no_matching_rule(self, backend_router_with_config)
  - test_route_with_overrides(self, backend_router_with_config)
- TestMetricsTracking
  **Methods**:
  - test_record_backend_call(self, backend_router_with_config)
  - test_record_failed_backend_call(self, backend_router_with_config)
  - test_get_backend_metrics(self, backend_router_with_config)
  - test_metrics_aggregation(self, backend_router_with_config)
- TestAdaptiveOverrides
  **Methods**:
  - test_adaptive_override_based_on_metrics(self, backend_router_with_config)
  - test_adaptive_override_with_high_latency(self, backend_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, backend_router_with_config)
  - test_route_with_extreme_complexity(self, backend_router_with_config)
  - test_route_with_zero_latency_budget(self, backend_router_with_config)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)
- test_metrics_store_initialization(self)
- test_default_config_structure(self)
- test_default_config_has_fallback(self)

#### File: tests/routing/test_environment_factory.py

**Imports**:
- from rlm.environments.base_env import BaseEnv
- from rlm.routing.environment_factory import EnvironmentFactory
- from unittest.mock import MagicMock, patch
- import pytest

**Classes**:
- TestEnvironmentFactoryInitialization
  **Methods**:
  - test_init_with_no_configs(self)
  - test_init_with_configs(self)
  - test_init_with_none_configs(self)
- TestEnvironmentInstanceCreation
  **Methods**:
  - test_get_environment_with_config(self, mock_get_environment)
  - test_get_environment_with_default_kwargs(self, mock_get_environment)
  - test_get_environment_with_no_config_or_default(self, mock_get_environment)
  - test_get_environment_config_merging(self, mock_get_environment)
- TestEnvironmentIdMapping
  **Methods**:
  - test_map_local_to_local(self)
  - test_map_docker_to_docker(self)
  - test_map_modal_to_modal(self)
  - test_map_e2b_to_e2b(self)
  - test_map_daytona_to_daytona(self)
  - test_map_prime_to_prime(self)
  - test_map_unknown_to_local(self)
- TestConfigurationHandling
  **Methods**:
  - test_config_isolation(self)
  - test_config_immutability(self)
  - test_empty_config_handling(self)
  - test_config_with_special_characters(self)
- TestErrorHandling
  **Methods**:
  - test_get_environment_exception_propagation(self, mock_get_environment)
  - test_get_environment_with_none_environment_id(self, mock_get_environment)
  - test_get_environment_with_empty_environment_id(self, mock_get_environment)
- TestMultipleEnvironments
  **Methods**:
  - test_create_multiple_environments(self, mock_get_environment)
  - test_reuse_environment_config(self, mock_get_environment)
- TestConfigValidation
  **Methods**:
  - test_config_with_missing_required_fields(self)
  - test_config_with_extra_fields(self)
- TestLayer1Configuration
  **Methods**:
  - test_enable_layer1_flag(self, mock_get_environment)
  - test_custom_tools_configuration(self, mock_get_environment)

#### File: tests/routing/test_environment_router.py

**Imports**:
- from pathlib import Path
- from rlm.routing.backend_router import TaskDescriptor
- from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
- import pytest

**Classes**:
- TestEnvironmentRouterInitialization
  **Methods**:
  - test_init_with_default_config(self)
  - test_init_with_config_path(self, temp_dir: Path)
- TestEnvironmentRuleMatching
  **Methods**:
  - test_route_lean_task_to_local(self, environment_router_with_config)
  - test_route_internet_task_to_modal(self, environment_router_with_config)
  - test_route_sensitive_data_to_local(self, environment_router_with_config)
  - test_route_with_no_matching_rule(self, environment_router_with_config)
  - test_route_high_cpu_task_to_modal(self, environment_router_with_config)
- TestSecurityConstraintChecking
  **Methods**:
  - test_confidential_data_always_local(self, environment_router_with_config)
  - test_public_data_can_use_remote(self, environment_router_with_config)
  - test_internal_data_restricted_in_dev(self, environment_router_with_config)
- TestCapabilityBasedRouting
  **Methods**:
  - test_lean_access_requires_local(self, environment_router_with_config)
  - test_haskell_access_requires_local(self, environment_router_with_config)
  - test_filesystem_access_allows_docker(self, environment_router_with_config)
  - test_multiple_capabilities_priority(self, environment_router_with_config)
- TestEdgeCases
  **Methods**:
  - test_route_with_empty_task_descriptor(self, environment_router_with_config)
  - test_route_with_extreme_cpu_requirements(self, environment_router_with_config)
  - test_route_with_unknown_capability(self, environment_router_with_config)
  - test_route_with_none_metrics(self, environment_router_with_config)
- TestEnvironmentRouteDataclass
  **Methods**:
  - test_environment_route_creation(self)
  - test_environment_route_with_empty_fields(self)

**Functions**:
- test_init_with_missing_config_file(self, temp_dir: Path)
- test_init_with_invalid_yaml(self, temp_dir: Path)

#### File: tests/routing/test_task_descriptor.py

**Imports**:
- from rlm.routing.task_descriptor import (
- import pytest

**Classes**:
- TestClassifyIntent
  **Methods**:
  - test_classify_web_research(self)
  - test_classify_proof_synthesis(self)
  - test_classify_code_generation(self)
  - test_classify_refactor(self)
  - test_classify_summarization(self)
  - test_classify_general(self)
  - test_classify_case_insensitive(self)
  - test_classify_with_multiple_keywords(self)
- TestEstimateComplexity
  **Methods**:
  - test_estimate_complexity_simple(self)
  - test_estimate_complexity_complex(self)
  - test_estimate_complexity_with_depth(self)
  - test_estimate_complexity_with_length(self)
  - test_estimate_complexity_with_keywords(self)
  - test_estimate_complexity_upper_bound(self)
  - test_estimate_complexity_lower_bound(self)
- TestCapabilityDetection
  **Methods**:
  - test_needs_internet_detection(self)
  - test_needs_filesystem_detection(self)
  - test_needs_lean_access_detection(self)
  - test_needs_haskell_access_detection(self)
  - test_needs_docker_isolation_detection(self)
  - test_capability_detection_case_insensitive(self)
- TestTokenEstimation
  **Methods**:
  - test_token_estimation_in_descriptor(self)
  - test_token_estimation_scales_with_length(self)
- TestCpuTimeEstimation
  **Methods**:
  - test_estimate_cpu_time_simple(self)
  - test_estimate_cpu_time_complex(self)
  - test_estimate_cpu_time_scales_with_complexity(self)
- TestDefaultTaskDescriptor
  **Methods**:
  - test_descriptor_has_required_fields(self)
  - test_descriptor_subtask_id_format(self)
  - test_descriptor_parent_task_id(self)
  - test_descriptor_capabilities(self)
  - test_descriptor_security(self)
  - test_descriptor_performance(self)
  - test_descriptor_mode(self)
  - test_descriptor_with_different_depths(self)
  - test_descriptor_with_empty_prompt(self)
  - test_descriptor_with_very_long_prompt(self)
- TestEdgeCases
  **Methods**:
  - test_classify_intent_with_none(self)
  - test_estimate_complexity_with_negative_depth(self)
  - test_capability_detection_with_special_characters(self)

#### File: view_log.py

**Imports**:
- from rich.console import Console
- from rich.panel import Panel
- from rich.syntax import Syntax
- import json
- import os
- import sys

**Functions**:
- view_log(log_file)

---

## Key Symbols by Feature

### Agent Framework
**feature/agent-framework**: 179 classes, 534 functions

### Core/Base
**develop**: 179 classes, 534 functions
**main**: 179 classes, 534 functions

### Messaging
**feature/messaging-system**: 179 classes, 534 functions

### Other
**feature/backend-diversity**: 179 classes, 534 functions
**feature/self-improvement**: 179 classes, 534 functions

### Redux/State Management
**feature/redux-state-management**: 179 classes, 534 functions

### Swarm/Orchestration
**feature/swarm-orchestration**: 179 classes, 534 functions

### Testing
**feature/testing-infrastructure**: 179 classes, 534 functions
**test-feature**: 179 classes, 534 functions

### Tools
**feature/dynamic-tools**: 179 classes, 534 functions

### Verification
**feature/verification-system**: 179 classes, 534 functions

### Visualization
**feature/visualization-interface**: 179 classes, 534 functions
