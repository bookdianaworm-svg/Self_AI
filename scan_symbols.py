#!/usr/bin/env python3
"""
Scan all git branches and extract Python code signatures.
This script uses git worktrees to scan each branch without disturbing the current branch.
"""

import subprocess
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set
import ast
import shutil
from datetime import datetime

class SymbolScanner:
    """Scan Python files for code signatures."""

    def __init__(self):
        self.worktrees_dir = Path("temp_worktrees")
        self.branch_symbols = {}

    def get_all_branches(self) -> List[str]:
        """Get list of all local branches."""
        result = subprocess.run(
            ["git", "branch", "--format=%(refname:short)"],
            capture_output=True,
            text=True,
            check=True
        )
        branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
        return branches

    def create_worktree(self, branch_name: str) -> Path:
        """Create a git worktree for the branch."""
        worktree_path = self.worktrees_dir / branch_name.replace("/", "_")
        worktree_path.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.run(
                ["git", "worktree", "add", str(worktree_path), branch_name],
                capture_output=True,
                text=True,
                check=True
            )
            return worktree_path
        except subprocess.CalledProcessError as e:
            # Worktree might already exist
            if "already exists" in e.stderr.lower():
                return worktree_path
            raise

    def remove_worktree(self, branch_name: str):
        """Remove a git worktree."""
        worktree_path = self.worktrees_dir / branch_name.replace("/", "_")
        try:
            subprocess.run(
                ["git", "worktree", "remove", str(worktree_path)],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError:
            pass  # Worktree might not exist or be already removed

    def get_python_files(self, worktree_path: Path) -> List[Path]:
        """Get all Python files in the worktree."""
        python_files = []
        for root, dirs, files in os.walk(worktree_path):
            # Skip common directories to ignore
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv']]
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        return python_files

    def extract_symbols(self, file_path: Path) -> Dict:
        """Extract symbols (classes, functions) from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            symbols = {
                'path': str(file_path.relative_to(file_path.parents[2]) if len(file_path.parts) > 2 else file_path.name),
                'imports': [],
                'classes': [],
                'functions': [],
                'errors': None
            }

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        symbols['imports'].append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module if node.module else ''
                    for alias in node.names:
                        symbols['imports'].append(f"from {module} import {alias.name}")

            # Extract top-level classes and functions
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'bases': [self._get_name(base) for base in node.bases],
                        'methods': []
                    }
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = self._extract_function_info(item)
                            class_info['methods'].append(method_info)
                        elif isinstance(item, ast.AsyncFunctionDef):
                            method_info = self._extract_function_info(item, is_async=True)
                            class_info['methods'].append(method_info)
                    symbols['classes'].append(class_info)
                elif isinstance(node, ast.FunctionDef):
                    func_info = self._extract_function_info(node)
                    symbols['functions'].append(func_info)
                elif isinstance(node, ast.AsyncFunctionDef):
                    func_info = self._extract_function_info(node, is_async=True)
                    symbols['functions'].append(func_info)

            return symbols

        except Exception as e:
            return {
                'path': str(file_path),
                'imports': [],
                'classes': [],
                'functions': [],
                'errors': str(e)
            }

    def _extract_function_info(self, node, is_async=False) -> Dict:
        """Extract information about a function."""
        args = [arg.arg for arg in node.args.args]
        returns = ast.unparse(node.returns) if node.returns else None

        return {
            'name': node.name,
            'args': args,
            'returns': returns,
            'is_async': is_async,
            'lineno': node.lineno
        }

    def _get_name(self, node):
        """Get name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        else:
            return ast.unparse(node)

    def scan_branch(self, branch_name: str) -> Dict:
        """Scan a single branch for Python symbols."""
        print(f"Scanning branch: {branch_name}")

        try:
            # Create worktree
            worktree_path = self.create_worktree(branch_name)

            # Get Python files
            python_files = self.get_python_files(worktree_path)

            # Extract symbols from each file
            symbols = {
                'branch': branch_name,
                'files': [],
                'total_classes': 0,
                'total_functions': 0,
                'total_files': len(python_files),
                'purpose': self._get_branch_purpose(branch_name)
            }

            for file_path in python_files:
                file_symbols = self.extract_symbols(file_path)
                if file_symbols and not file_symbols.get('errors'):
                    symbols['files'].append(file_symbols)
                    symbols['total_classes'] += len(file_symbols['classes'])
                    symbols['total_functions'] += len(file_symbols['functions'])

            # Clean up worktree
            # self.remove_worktree(branch_name)  # Keep worktrees for now

            return symbols

        except Exception as e:
            print(f"Error scanning branch {branch_name}: {e}")
            return {
                'branch': branch_name,
                'error': str(e),
                'files': [],
                'total_classes': 0,
                'total_functions': 0,
                'total_files': 0,
                'purpose': self._get_branch_purpose(branch_name)
            }

    def _get_branch_purpose(self, branch_name: str) -> str:
        """Get the purpose of a branch based on its name."""
        purposes = {
            'main': 'Production-ready code',
            'develop': 'Integration branch for features',
            'feature/redux-state-management': 'Redux store implementation with slices',
            'feature/agent-framework': 'Base agent classes and implementations',
            'feature/swarm-orchestration': 'Swarm orchestration and coordination',
            'feature/messaging-system': 'Messaging and communication infrastructure',
            'feature/dynamic-tools': 'Dynamic tool discovery and execution',
            'feature/verification-system': 'Lean 4 verification and validation',
            'feature/backend-diversity': 'Multi-backend routing and environment selection',
            'feature/visualization-interface': 'Real-time monitoring and UI',
            'feature/self-improvement': 'Self-improvement and learning capabilities',
            'feature/testing-infrastructure': 'Testing frameworks and CI/CD',
            'test-feature': 'Test feature branch',
            'general-caravel': 'Legacy branch'
        }
        return purposes.get(branch_name, 'Unknown purpose')

    def scan_all_branches(self) -> Dict:
        """Scan all branches."""
        branches = self.get_all_branches()
        all_symbols = {
            'scan_date': datetime.now().isoformat(),
            'branches': {},
            'summary': {
                'total_branches': len(branches),
                'total_files': 0,
                'total_classes': 0,
                'total_functions': 0
            }
        }

        # Create worktrees directory
        self.worktrees_dir.mkdir(parents=True, exist_ok=True)

        for branch in branches:
            branch_symbols = self.scan_branch(branch)
            all_symbols['branches'][branch] = branch_symbols
            all_symbols['summary']['total_files'] += branch_symbols.get('total_files', 0)
            all_symbols['summary']['total_classes'] += branch_symbols.get('total_classes', 0)
            all_symbols['summary']['total_functions'] += branch_symbols.get('total_functions', 0)

        return all_symbols

    def generate_markdown(self, symbols: Dict) -> str:
        """Generate markdown output from symbols."""
        lines = []

        lines.append("# Project Symbols Map")
        lines.append("")
        lines.append(f"**Generated**: {symbols['scan_date']}")
        lines.append("")

        # Summary
        summary = symbols['summary']
        lines.append("## Overview")
        lines.append("")
        lines.append(f"- **Total branches scanned**: {summary['total_branches']}")
        lines.append(f"- **Total Python files**: {summary['total_files']}")
        lines.append(f"- **Total classes**: {summary['total_classes']}")
        lines.append(f"- **Total functions**: {summary['total_functions']}")
        lines.append("")

        # Branch Summary
        lines.append("## Branch Summary")
        lines.append("")
        lines.append("| Branch | Purpose | Files | Classes | Functions |")
        lines.append("|--------|---------|-------|---------|-----------|")

        for branch_name, branch_data in sorted(symbols['branches'].items()):
            purpose = branch_data.get('purpose', 'Unknown')
            files = branch_data.get('total_files', 0)
            classes = branch_data.get('total_classes', 0)
            functions = branch_data.get('total_functions', 0)
            lines.append(f"| {branch_name} | {purpose} | {files} | {classes} | {functions} |")

        lines.append("")

        # Detailed symbols by branch
        lines.append("## Detailed Symbols by Branch")
        lines.append("")

        for branch_name, branch_data in sorted(symbols['branches'].items()):
            lines.append(f"### {branch_name}")
            lines.append("")
            lines.append(f"**Purpose**: {branch_data.get('purpose', 'Unknown')}")
            lines.append(f"**Files**: {branch_data.get('total_files', 0)}")
            lines.append(f"**Classes**: {branch_data.get('total_classes', 0)}")
            lines.append(f"**Functions**: {branch_data.get('total_functions', 0)}")
            lines.append("")

            if 'files' in branch_data:
                for file_data in branch_data['files']:
                    lines.append(f"#### File: `{file_data['path']}`")
                    lines.append("")

                    # Imports
                    if file_data['imports']:
                        lines.append("**Imports**:")
                        for imp in file_data['imports']:
                            lines.append(f"- {imp}")
                        lines.append("")

                    # Classes
                    if file_data['classes']:
                        lines.append("**Classes**:")
                        for class_data in file_data['classes']:
                            bases_str = ", ".join(class_data['bases']) if class_data['bases'] else ''
                            if bases_str:
                                lines.append(f"- **{class_data['name']}**({bases_str}):")
                            else:
                                lines.append(f"- **{class_data['name']}**:")
                            if class_data['methods']:
                                for method in class_data['methods']:
                                    async_prefix = "async " if method['is_async'] else ""
                                    args_str = ", ".join(method['args'])
                                    returns_str = f" -> {method['returns']}" if method['returns'] else ""
                                    lines.append(f"  - {async_prefix}def {method['name']}({args_str}){returns_str}")
                        lines.append("")

                    # Functions
                    if file_data['functions']:
                        lines.append("**Functions**:")
                        for func_data in file_data['functions']:
                            async_prefix = "async " if func_data['is_async'] else ""
                            args_str = ", ".join(func_data['args'])
                            returns_str = f" -> {func_data['returns']}" if func_data['returns'] else ""
                            lines.append(f"- {async_prefix}def {func_data['name']}({args_str}){returns_str}")
                        lines.append("")

        # Cross-branch dependencies (placeholder for manual analysis)
        lines.append("## Cross-Branch Dependencies")
        lines.append("")
        lines.append("> *This section should be updated manually based on analysis of the symbols above.*")
        lines.append("")
        lines.append("Based on the symbols extracted, here are potential cross-branch dependencies:")
        lines.append("")
        lines.append("### Known Dependencies (from BRANCHING.md)")
        lines.append("")
        lines.append("- **feature/swarm-orchestration** depends on:")
        lines.append("  - feature/redux-state-management")
        lines.append("  - feature/agent-framework")
        lines.append("  - feature/messaging-system")
        lines.append("")
        lines.append("- **feature/visualization-interface** depends on:")
        lines.append("  - feature/redux-state-management")
        lines.append("  - feature/messaging-system")
        lines.append("")
        lines.append("- **feature/self-improvement** depends on:")
        lines.append("  - feature/dynamic-tools")
        lines.append("  - feature/messaging-system")
        lines.append("")
        lines.append("- **feature/verification-system** depends on:")
        lines.append("  - feature/agent-framework")
        lines.append("")

        # Key symbols by feature area
        lines.append("## Key Symbols by Feature Area")
        lines.append("")
        lines.append("> *This section should be populated manually based on the symbols above.*")
        lines.append("")
        lines.append("### Agent Framework")
        lines.append("- [List key agent-related classes and functions]")
        lines.append("")
        lines.append("### Redux/State Management")
        lines.append("- [List key Redux-related classes and functions]")
        lines.append("")
        lines.append("### Messaging/Communication")
        lines.append("- [List key messaging-related classes and functions]")
        lines.append("")
        lines.append("### Tools/Utilities")
        lines.append("- [List key tool-related classes and functions]")
        lines.append("")
        lines.append("### Verification/Validation")
        lines.append("- [List key verification-related classes and functions]")
        lines.append("")
        lines.append("### Testing")
        lines.append("- [List key testing-related classes and functions]")
        lines.append("")

        return "\n".join(lines)

    def cleanup(self):
        """Clean up all worktrees."""
        if self.worktrees_dir.exists():
            print(f"Cleaning up worktrees directory: {self.worktrees_dir}")
            shutil.rmtree(self.worktrees_dir)


def main():
    """Main function to scan all branches."""
    scanner = SymbolScanner()

    try:
        # Scan all branches
        print("Starting branch scan...")
        symbols = scanner.scan_all_branches()

        # Generate markdown
        print("Generating markdown...")
        markdown = scanner.generate_markdown(symbols)

        # Write to file
        output_file = Path("symbols.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"\n✅ Symbols map generated: {output_file}")
        print(f"   Total branches: {symbols['summary']['total_branches']}")
        print(f"   Total files: {symbols['summary']['total_files']}")
        print(f"   Total classes: {symbols['summary']['total_classes']}")
        print(f"   Total functions: {symbols['summary']['total_functions']}")

    finally:
        # Cleanup
        scanner.cleanup()
        print("\n✅ Worktrees cleaned up")


if __name__ == "__main__":
    main()
