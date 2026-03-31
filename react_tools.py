#!/usr/bin/env python3
"""
ReAct (Reason + Act) Framework for TinyLlama Tool Usage
Uses Pydantic to enforce structured JSON outputs for reliable tool calling
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
import json
import subprocess
from pathlib import Path

class ToolName(str, Enum):
    """Available tools the AI can use"""
    SEARCH_KNOWLEDGE = "search_knowledge"
    ADD_KNOWLEDGE = "add_knowledge"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EXECUTE_CODE = "execute_code"
    ANALYZE_PERFORMANCE = "analyze_performance"
    IMPROVE_SYSTEM = "improve_system"

class ReActStep(BaseModel):
    """Single ReAct reasoning step"""
    thought: str = Field(description="The AI's reasoning about what to do next")
    action: Optional[ToolName] = Field(description="Which tool to use (or None if finished)")
    action_input: Optional[Dict[str, Any]] = Field(description="Parameters for the tool")
    observation: Optional[str] = Field(description="Result from the tool execution")
    
    def is_finished(self) -> bool:
        """Check if this step represents a final answer"""
        return self.action is None

class ReActResponse(BaseModel):
    """Complete ReAct response with multiple steps"""
    steps: List[ReActStep]
    final_answer: Optional[str] = Field(description="The final answer after all tool usage")

class ToolExecutor:
    """Executes tools on behalf of the AI"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.knowledge_base = {}  # Simple in-memory knowledge base for now
        
    def search_knowledge(self, query: str, limit: int = 3) -> str:
        """Search the knowledge base for relevant information"""
        # Simple keyword matching for now
        results = []
        for key, value in self.knowledge_base.items():
            if query.lower() in key.lower() or query.lower() in value.lower():
                results.append(f"{key}: {value}")
        
        if results:
            return f"Found {len(results)} relevant items:\n" + "\n".join(results[:limit])
        else:
            return f"No relevant knowledge found for query: {query}"
    
    def add_knowledge(self, key: str, value: str, category: str = "general") -> str:
        """Add knowledge to the knowledge base"""
        self.knowledge_base[key] = {
            "value": value,
            "category": category,
            "timestamp": "2024-01-01"  # Simplified for now
        }
        return f"Added knowledge: {key} = {value} (category: {category})"
    
    def read_file(self, filepath: str) -> str:
        """Read a file and return its contents"""
        try:
            full_path = self.base_path / filepath
            with open(full_path, 'r') as f:
                content = f.read()
            return f"File contents of {filepath}:\n{content}"
        except FileNotFoundError:
            return f"Error: File {filepath} not found"
        except Exception as e:
            return f"Error reading file {filepath}: {str(e)}"
    
    def write_file(self, filepath: str, content: str, overwrite: bool = False) -> str:
        """Write content to a file"""
        try:
            full_path = self.base_path / filepath
            if full_path.exists() and not overwrite:
                return f"Error: File {filepath} already exists. Use overwrite=True to replace."
            
            with open(full_path, 'w') as f:
                f.write(content)
            return f"Successfully wrote {len(content)} characters to {filepath}"
        except Exception as e:
            return f"Error writing file {filepath}: {str(e)}"
    
    def execute_code(self, code: str, language: str = "python") -> str:
        """Execute code and return results"""
        if language != "python":
            return f"Error: Only Python execution is currently supported"
        
        try:
            # For safety, we'll use a restricted execution environment
            # This is a simplified version - in production, use proper sandboxing
            result = subprocess.run(
                ['python3', '-c', code],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.base_path)
            )
            
            if result.returncode == 0:
                return f"Code executed successfully:\n{result.stdout}"
            else:
                return f"Code execution failed:\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out"
        except Exception as e:
            return f"Error executing code: {str(e)}"
    
    def analyze_performance(self, metric: str = "all") -> str:
        """Analyze system performance"""
        # Simplified performance analysis
        analysis = {
            "knowledge_size": len(self.knowledge_base),
            "base_path": str(self.base_path),
            "available_tools": [tool.value for tool in ToolName]
        }
        return f"Performance Analysis:\n{json.dumps(analysis, indent=2)}"
    
    def improve_system(self, improvement_type: str, target: str) -> str:
        """Generate system improvements"""
        return f"Generated improvement suggestion for {target} in category {improvement_type}"
    
    def execute_tool(self, tool_name: ToolName, action_input: Dict[str, Any]) -> str:
        """Execute a specific tool with given parameters"""
        tool_map = {
            ToolName.SEARCH_KNOWLEDGE: self.search_knowledge,
            ToolName.ADD_KNOWLEDGE: self.add_knowledge,
            ToolName.READ_FILE: self.read_file,
            ToolName.WRITE_FILE: self.write_file,
            ToolName.EXECUTE_CODE: self.execute_code,
            ToolName.ANALYZE_PERFORMANCE: self.analyze_performance,
            ToolName.IMPROVE_SYSTEM: self.improve_system,
        }
        
        if tool_name in tool_map:
            try:
                return tool_map[tool_name](**action_input)
            except Exception as e:
                return f"Error executing {tool_name}: {str(e)}"
        else:
            return f"Error: Unknown tool {tool_name}"

class ReActAI:
    """Main ReAct AI system"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.executor = ToolExecutor(base_path)
        
    def create_react_prompt(self, user_query: str, available_tools: List[ToolName]) -> str:
        """Create a structured prompt for ReAct reasoning"""
        tool_descriptions = {
            ToolName.SEARCH_KNOWLEDGE: "Search the knowledge base for information",
            ToolName.ADD_KNOWLEDGE: "Add new information to the knowledge base",
            ToolName.READ_FILE: "Read contents of a file",
            ToolName.WRITE_FILE: "Write content to a file",
            ToolName.EXECUTE_CODE: "Execute Python code",
            ToolName.ANALYZE_PERFORMANCE: "Analyze system performance metrics",
            ToolName.IMPROVE_SYSTEM: "Generate system improvement suggestions"
        }
        
        prompt = f"""You are an AI assistant that can use tools to help answer questions and solve problems.

Available tools:
{chr(10).join([f"- {tool.value}: {tool_descriptions.get(tool, 'No description')}" for tool in available_tools])}

You must respond in JSON format with the following structure:
{{
    "thought": "Your reasoning about what to do next",
    "action": "tool_name or null if finished",
    "action_input": {{"param1": "value1", "param2": "value2"}} or null
}}

User Query: {user_query}

Think step by step and use the appropriate tools to solve this problem.
If you have enough information to answer the question, set action to null and provide your final answer in the thought field.

Response:"""
        
        return prompt
    
    def query_llm(self, prompt: str) -> str:
        """Query TinyLlama through Ollama"""
        try:
            result = subprocess.run(
                ['ollama', 'run', 'tinyllama'],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Error: Query timeout"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def parse_react_response(self, response: str) -> ReActStep:
        """Parse the JSON response from the model"""
        try:
            # Extract JSON from response (model might add extra text)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                # Convert action string to ToolName enum if present
                if data.get('action') and isinstance(data['action'], str):
                    try:
                        data['action'] = ToolName(data['action'])
                    except ValueError:
                        data['action'] = None
                
                return ReActStep(**data)
            else:
                # Fallback: treat as finished with the response as thought
                return ReActStep(
                    thought=response,
                    action=None,
                    action_input=None
                )
                
        except Exception as e:
            print(f"Error parsing response: {e}")
            # Fallback: treat as finished
            return ReActStep(
                thought=f"Error parsing response: {response}",
                action=None,
                action_input=None
            )
    
    def run_react_loop(self, user_query: str, max_steps: int = 5) -> str:
        """Run the complete ReAct loop"""
        available_tools = list(ToolName)
        steps = []
        
        for step_num in range(max_steps):
            print(f"Step {step_num + 1}: Creating prompt...")
            prompt = self.create_react_prompt(user_query, available_tools)
            
            print(f"Step {step_num + 1}: Querying model...")
            response = self.query_llm(prompt)
            print(f"Model response: {response}")
            
            react_step = self.parse_react_response(response)
            print(f"Parsed step: {react_step}")
            
            if react_step.is_finished():
                steps.append(react_step)
                break
            
            if react_step.action and react_step.action_input:
                print(f"Step {step_num + 1}: Executing tool {react_step.action}...")
                observation = self.executor.execute_tool(
                    react_step.action,
                    react_step.action_input
                )
                print(f"Tool result: {observation}")
                
                # Add observation to the step
                react_step.observation = observation
                steps.append(react_step)
                
                # Update user query for next iteration with observation
                user_query = f"Previous step result: {observation}. Continue solving the original query."
            else:
                print(f"Step {step_num + 1}: No valid action, finishing.")
                steps.append(react_step)
                break
        
        # Create final response
        final_response = ReActResponse(steps=steps)
        
        # Get final answer from last step
        if steps and steps[-1].is_finished():
            final_response.final_answer = steps[-1].thought
        else:
            final_response.final_answer = "Loop completed without final answer."
        
        return final_response

if __name__ == "__main__":
    # Test the ReAct system
    base_path = Path("/mnt/c/Users/drave/Documents/trae_projects/Self_AI")
    ai = ReActAI(base_path)
    
    # Test query
    test_query = "Search the knowledge base for information about sorting algorithms, then add a new entry about quicksort if it's not already there."
    
    print("Starting ReAct loop...")
    result = ai.run_react_loop(test_query)
    
    print(f"\nFinal result: {result}")
    print(f"\nFinal answer: {result.final_answer}")