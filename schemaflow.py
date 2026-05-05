#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SchemaFlow - Lightweight JSON Schema Terminal Visualizer & Validator
A zero-dependency Python CLI tool for JSON Schema visualization, validation, and analysis.

Author: SchemaFlow Team
License: MIT
Python: 3.8+
"""

import json
import sys
import os
import re
import argparse
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
from enum import Enum

__version__ = "1.0.0"
__author__ = "SchemaFlow Team"


class Colors:
    """Terminal color codes"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class SchemaType(Enum):
    """JSON Schema types"""
    OBJECT = "object"
    ARRAY = "array"
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NULL = "null"


class SchemaFlow:
    """Main SchemaFlow engine"""
    
    # Type colors mapping
    TYPE_COLORS = {
        "object": Colors.BRIGHT_BLUE,
        "array": Colors.BRIGHT_MAGENTA,
        "string": Colors.BRIGHT_GREEN,
        "number": Colors.BRIGHT_CYAN,
        "integer": Colors.CYAN,
        "boolean": Colors.BRIGHT_YELLOW,
        "null": Colors.BRIGHT_BLACK,
        "any": Colors.WHITE,
    }
    
    # Constraint keywords
    CONSTRAINT_KEYWORDS = {
        "string": ["minLength", "maxLength", "pattern", "format", "enum"],
        "number": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
        "integer": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
        "array": ["minItems", "maxItems", "uniqueItems"],
        "object": ["minProperties", "maxProperties", "required"],
    }
    
    def __init__(self, use_color: bool = True, compact: bool = False):
        self.use_color = use_color and sys.stdout.isatty()
        self.compact = compact
        self.indent_size = 2
        
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if enabled"""
        if self.use_color:
            return f"{color}{text}{Colors.RESET}"
        return text
    
    def get_type_color(self, schema_type: Union[str, List[str]]) -> str:
        """Get color for schema type"""
        if isinstance(schema_type, list):
            return Colors.WHITE
        return self.TYPE_COLORS.get(schema_type, Colors.WHITE)
    
    def format_type(self, schema_type: Union[str, List[str]]) -> str:
        """Format schema type with color"""
        if isinstance(schema_type, list):
            type_str = " | ".join(schema_type)
        else:
            type_str = schema_type
        color = self.get_type_color(schema_type)
        return self.colorize(type_str, color)
    
    def format_constraints(self, schema: Dict[str, Any], schema_type: str) -> str:
        """Format schema constraints"""
        constraints = []
        keywords = self.CONSTRAINT_KEYWORDS.get(schema_type, [])
        
        for keyword in keywords:
            if keyword in schema:
                value = schema[keyword]
                if keyword == "required" and isinstance(value, list):
                    constraints.append(f"required={len(value)}")
                elif keyword == "enum" and isinstance(value, list):
                    constraints.append(f"enum={len(value)}")
                elif keyword == "pattern":
                    constraints.append(f"pattern")
                else:
                    constraints.append(f"{keyword}={value}")
        
        if constraints:
            constraint_str = "[" + ", ".join(constraints) + "]"
            return self.colorize(constraint_str, Colors.DIM)
        return ""
    
    def format_description(self, description: Optional[str], max_length: int = 50) -> str:
        """Format description with truncation"""
        if not description:
            return ""
        
        if len(description) > max_length:
            description = description[:max_length-3] + "..."
        
        return self.colorize(f" # {description}", Colors.BRIGHT_BLACK)
    
    def visualize(self, schema: Dict[str, Any], name: str = "root", depth: int = 0, 
                  is_last: bool = True, parent_prefix: str = "") -> str:
        """
        Recursively visualize JSON Schema as a tree structure
        
        Args:
            schema: JSON Schema object
            name: Property name
            depth: Current depth in tree
            is_last: Whether this is the last child
            parent_prefix: Prefix for parent indentation
            
        Returns:
            Formatted tree string
        """
        lines = []
        
        # Determine tree characters
        if depth == 0:
            branch = ""
            new_prefix = ""
        else:
            branch = "└── " if is_last else "├── "
            new_prefix = parent_prefix + ("    " if is_last else "│   ")
        
        # Get schema type
        schema_type = schema.get("type", "any")
        if isinstance(schema_type, list):
            schema_type = " | ".join(schema_type)
        
        # Format the node
        type_str = self.format_type(schema.get("type", "any"))
        
        # Build node label
        if depth == 0:
            node_label = f"{self.colorize(name, Colors.BOLD)}: {type_str}"
        else:
            node_label = f"{parent_prefix}{branch}{self.colorize(name, Colors.BOLD)}: {type_str}"
        
        # Add constraints
        constraints = self.format_constraints(schema, schema_type if isinstance(schema_type, str) else "any")
        if constraints:
            node_label += f" {constraints}"
        
        # Add description
        description = schema.get("description")
        if description and not self.compact:
            node_label += self.format_description(description)
        
        lines.append(node_label)
        
        # Handle object properties
        if schema_type == "object" or "properties" in schema:
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            
            items = list(properties.items())
            for i, (prop_name, prop_schema) in enumerate(items):
                is_prop_last = (i == len(items) - 1) and "additionalProperties" not in schema
                
                # Mark required fields
                if prop_name in required and not self.compact:
                    prop_name = f"{prop_name}*"
                
                lines.append(self.visualize(prop_schema, prop_name, depth + 1, is_prop_last, new_prefix))
        
        # Handle array items
        if schema_type == "array" or "items" in schema:
            items_schema = schema.get("items")
            if items_schema:
                is_items_last = "additionalItems" not in schema
                lines.append(self.visualize(items_schema, "[items]", depth + 1, is_items_last, new_prefix))
        
        # Handle additionalProperties
        additional = schema.get("additionalProperties")
        if additional is not None and additional is not True:
            if isinstance(additional, dict):
                lines.append(self.visualize(additional, "[additional]", depth + 1, True, new_prefix))
            elif additional is False:
                lines.append(f"{new_prefix}{'└── ' if is_last else '├── '}{self.colorize('[additional]', Colors.DIM)}: {self.colorize('false', Colors.BRIGHT_RED)}")
        
        # Handle oneOf, anyOf, allOf
        for combiner in ["oneOf", "anyOf", "allOf"]:
            if combiner in schema:
                combiner_schemas = schema[combiner]
                lines.append(f"{new_prefix}{'└── ' if is_last else '├── '}{self.colorize(f'[{combiner}]', Colors.BRIGHT_YELLOW)}")
                combiner_prefix = new_prefix + ("    " if is_last else "│   ")
                for j, sub_schema in enumerate(combiner_schemas):
                    is_sub_last = j == len(combiner_schemas) - 1
                    sub_lines = self.visualize(sub_schema, f"option_{j+1}", depth + 2, is_sub_last, combiner_prefix)
                    lines.append(sub_lines)
        
        # Handle $ref
        if "$ref" in schema:
            ref = schema["$ref"]
            lines.append(f"{new_prefix}{'└── ' if is_last else '├── '}{self.colorize('$ref', Colors.DIM)}: {self.colorize(ref, Colors.BRIGHT_CYAN)}")
        
        return "\n".join(lines)
    
    def validate_json(self, data: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
        """
        Validate JSON data against schema
        
        Returns:
            List of validation errors
        """
        errors = []
        schema_type = schema.get("type")
        
        # Type validation
        if schema_type:
            valid = self._check_type(data, schema_type)
            if not valid:
                expected = schema_type if isinstance(schema_type, str) else " | ".join(schema_type)
                actual = type(data).__name__
                errors.append(f"{path}: expected {expected}, got {actual}")
                return errors
        
        # String validation
        if schema_type == "string" and isinstance(data, str):
            errors.extend(self._validate_string(data, schema, path))
        
        # Number validation
        if schema_type in ["number", "integer"] and isinstance(data, (int, float)):
            errors.extend(self._validate_number(data, schema, path))
        
        # Array validation
        if schema_type == "array" and isinstance(data, list):
            errors.extend(self._validate_array(data, schema, path))
        
        # Object validation
        if schema_type == "object" and isinstance(data, dict):
            errors.extend(self._validate_object(data, schema, path))
        
        # Enum validation
        if "enum" in schema:
            if data not in schema["enum"]:
                errors.append(f"{path}: value must be one of {schema['enum']}")
        
        return errors
    
    def _check_type(self, data: Any, expected_type: Union[str, List[str]]) -> bool:
        """Check if data matches expected type"""
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }
        
        if isinstance(expected_type, list):
            return any(self._check_type(data, t) for t in expected_type)
        
        expected = type_mapping.get(expected_type)
        if expected is None:
            return True
        
        if isinstance(expected, tuple):
            return isinstance(data, expected)
        return isinstance(data, expected)
    
    def _validate_string(self, data: str, schema: Dict[str, Any], path: str) -> List[str]:
        """Validate string constraints"""
        errors = []
        
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: string length {len(data)} < minLength {schema['minLength']}")
        
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path}: string length {len(data)} > maxLength {schema['maxLength']}")
        
        if "pattern" in schema:
            pattern = schema["pattern"]
            if not re.search(pattern, data):
                errors.append(f"{path}: string does not match pattern '{pattern}'")
        
        if "format" in schema:
            format_errors = self._validate_format(data, schema["format"], path)
            errors.extend(format_errors)
        
        return errors
    
    def _validate_number(self, data: Union[int, float], schema: Dict[str, Any], path: str) -> List[str]:
        """Validate number constraints"""
        errors = []
        
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: value {data} < minimum {schema['minimum']}")
        
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: value {data} > maximum {schema['maximum']}")
        
        if "exclusiveMinimum" in schema and data <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: value {data} <= exclusiveMinimum {schema['exclusiveMinimum']}")
        
        if "exclusiveMaximum" in schema and data >= schema["exclusiveMaximum"]:
            errors.append(f"{path}: value {data} >= exclusiveMaximum {schema['exclusiveMaximum']}")
        
        if "multipleOf" in schema:
            if data % schema["multipleOf"] != 0:
                errors.append(f"{path}: value {data} is not multiple of {schema['multipleOf']}")
        
        return errors
    
    def _validate_array(self, data: List[Any], schema: Dict[str, Any], path: str) -> List[str]:
        """Validate array constraints"""
        errors = []
        
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: array length {len(data)} < minItems {schema['minItems']}")
        
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append(f"{path}: array length {len(data)} > maxItems {schema['maxItems']}")
        
        if "uniqueItems" in schema and schema["uniqueItems"]:
            seen = set()
            for item in data:
                item_key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
                if item_key in seen:
                    errors.append(f"{path}: array contains duplicate items")
                    break
                seen.add(item_key)
        
        # Validate items
        if "items" in schema:
            items_schema = schema["items"]
            for i, item in enumerate(data):
                item_errors = self.validate_json(item, items_schema, f"{path}[{i}]")
                errors.extend(item_errors)
        
        return errors
    
    def _validate_object(self, data: Dict[str, Any], schema: Dict[str, Any], path: str) -> List[str]:
        """Validate object constraints"""
        errors = []
        
        if "minProperties" in schema and len(data) < schema["minProperties"]:
            errors.append(f"{path}: object has {len(data)} properties < minProperties {schema['minProperties']}")
        
        if "maxProperties" in schema and len(data) > schema["maxProperties"]:
            errors.append(f"{path}: object has {len(data)} properties > maxProperties {schema['maxProperties']}")
        
        # Check required properties
        required = schema.get("required", [])
        for prop in required:
            if prop not in data:
                errors.append(f"{path}: missing required property '{prop}'")
        
        # Validate properties
        properties = schema.get("properties", {})
        for prop_name, prop_schema in properties.items():
            if prop_name in data:
                prop_errors = self.validate_json(data[prop_name], prop_schema, f"{path}.{prop_name}")
                errors.extend(prop_errors)
        
        # Check additionalProperties
        additional = schema.get("additionalProperties", True)
        if additional is False:
            allowed = set(properties.keys())
            for key in data.keys():
                if key not in allowed:
                    errors.append(f"{path}: additional property '{key}' not allowed")
        elif isinstance(additional, dict):
            allowed = set(properties.keys())
            for key, value in data.items():
                if key not in allowed:
                    prop_errors = self.validate_json(value, additional, f"{path}.{key}")
                    errors.extend(prop_errors)
        
        return errors
    
    def _validate_format(self, data: str, format_type: str, path: str) -> List[str]:
        """Validate string format"""
        errors = []
        
        format_patterns = {
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "uri": r'^https?://[^\s/$.?#].[^\s]*$',
            "date": r'^\d{4}-\d{2}-\d{2}$',
            "date-time": r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$',
            "uuid": r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        }
        
        pattern = format_patterns.get(format_type)
        if pattern and not re.match(pattern, data):
            errors.append(f"{path}: string does not match format '{format_type}'")
        
        return errors
    
    def analyze_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze schema structure and return statistics
        
        Returns:
            Dictionary with schema analysis results
        """
        stats = {
            "total_properties": 0,
            "required_properties": 0,
            "nested_levels": 0,
            "types_used": set(),
            "constraints_used": set(),
            "has_references": False,
        }
        
        self._analyze_recursive(schema, stats, 0)
        
        stats["types_used"] = list(stats["types_used"])
        stats["constraints_used"] = list(stats["constraints_used"])
        
        return stats
    
    def _analyze_recursive(self, schema: Dict[str, Any], stats: Dict[str, Any], depth: int):
        """Recursively analyze schema"""
        stats["nested_levels"] = max(stats["nested_levels"], depth)
        
        schema_type = schema.get("type")
        if schema_type:
            if isinstance(schema_type, list):
                stats["types_used"].update(schema_type)
            else:
                stats["types_used"].add(schema_type)
        
        # Check constraints
        for keyword in ["minLength", "maxLength", "pattern", "format", "minimum", "maximum",
                       "minItems", "maxItems", "uniqueItems", "minProperties", "maxProperties"]:
            if keyword in schema:
                stats["constraints_used"].add(keyword)
        
        if "$ref" in schema:
            stats["has_references"] = True
        
        # Analyze properties
        if "properties" in schema:
            props = schema["properties"]
            stats["total_properties"] += len(props)
            stats["required_properties"] += len(schema.get("required", []))
            
            for prop_schema in props.values():
                self._analyze_recursive(prop_schema, stats, depth + 1)
        
        # Analyze items
        if "items" in schema and isinstance(schema["items"], dict):
            self._analyze_recursive(schema["items"], stats, depth + 1)
        
        # Analyze combiners
        for combiner in ["oneOf", "anyOf", "allOf"]:
            if combiner in schema:
                for sub_schema in schema[combiner]:
                    self._analyze_recursive(sub_schema, stats, depth + 1)
    
    def format_json(self, data: Any, indent: int = 2) -> str:
        """Format JSON with optional colorization"""
        json_str = json.dumps(data, indent=indent, ensure_ascii=False)
        
        if not self.use_color:
            return json_str
        
        # Simple syntax highlighting
        lines = json_str.split("\n")
        formatted_lines = []
        
        for line in lines:
            formatted = line
            # Highlight keys
            formatted = re.sub(
                r'("[^"]+")\s*:',
                lambda m: f'{self.colorize(m.group(1), Colors.BRIGHT_CYAN)}:',
                formatted
            )
            # Highlight strings
            formatted = re.sub(
                r':\s*"([^"]*)"',
                lambda m: ': ' + self.colorize('"' + m.group(1) + '"', Colors.BRIGHT_GREEN),
                formatted
            )
            # Highlight numbers
            formatted = re.sub(
                r':\s*(-?\d+\.?\d*)',
                lambda m: f': {self.colorize(m.group(1), Colors.BRIGHT_YELLOW)}',
                formatted
            )
            # Highlight booleans and null
            formatted = re.sub(
                r':\s*(true|false|null)',
                lambda m: f': {self.colorize(m.group(1), Colors.BRIGHT_MAGENTA)}',
                formatted
            )
            formatted_lines.append(formatted)
        
        return "\n".join(formatted_lines)


def load_json_file(filepath: str) -> Any:
    """Load JSON from file"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    📊 SchemaFlow v1.0.0                      ║
║        JSON Schema Terminal Visualizer & Validator           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog='schemaflow',
        description='SchemaFlow - Lightweight JSON Schema Terminal Visualizer & Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  schemaflow visualize schema.json          # Visualize schema structure
  schemaflow validate data.json schema.json # Validate JSON against schema
  schemaflow analyze schema.json            # Analyze schema statistics
  schemaflow format data.json               # Format JSON file
  schemaflow visualize schema.json --no-color --compact
        """
    )
    
    parser.add_argument('--version', action='version', version=f'SchemaFlow {__version__}')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--compact', action='store_true', help='Compact output (less verbose)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', aliases=['viz', 'v'],
                                       help='Visualize JSON Schema structure')
    viz_parser.add_argument('schema', help='Path to JSON Schema file')
    viz_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    
    # Validate command
    val_parser = subparsers.add_parser('validate', aliases=['val', 'vld'],
                                       help='Validate JSON data against schema')
    val_parser.add_argument('data', help='Path to JSON data file')
    val_parser.add_argument('schema', help='Path to JSON Schema file')
    
    # Analyze command
    ana_parser = subparsers.add_parser('analyze', aliases=['ana', 'a'],
                                       help='Analyze schema structure and statistics')
    ana_parser.add_argument('schema', help='Path to JSON Schema file')
    
    # Format command
    fmt_parser = subparsers.add_parser('format', aliases=['fmt', 'f'],
                                       help='Format JSON file with syntax highlighting')
    fmt_parser.add_argument('file', help='Path to JSON file')
    fmt_parser.add_argument('-i', '--indent', type=int, default=2, help='Indentation size')
    fmt_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)
    
    # Initialize SchemaFlow
    flow = SchemaFlow(use_color=not args.no_color, compact=args.compact)
    
    try:
        if args.command in ['visualize', 'viz', 'v']:
            schema = load_json_file(args.schema)
            output = flow.visualize(schema)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"✓ Visualization saved to {args.output}")
            else:
                print(output)
        
        elif args.command in ['validate', 'val', 'vld']:
            data = load_json_file(args.data)
            schema = load_json_file(args.schema)
            
            errors = flow.validate_json(data, schema)
            
            if errors:
                print(f"❌ Validation failed with {len(errors)} error(s):")
                for error in errors:
                    print(f"  • {error}")
                sys.exit(1)
            else:
                print("✅ Validation successful! JSON data is valid.")
        
        elif args.command in ['analyze', 'ana', 'a']:
            schema = load_json_file(args.schema)
            stats = flow.analyze_schema(schema)
            
            print(f"\n📊 Schema Analysis: {args.schema}\n")
            print(f"  Total Properties:     {stats['total_properties']}")
            print(f"  Required Properties:  {stats['required_properties']}")
            print(f"  Max Nesting Level:    {stats['nested_levels']}")
            print(f"  Types Used:           {', '.join(stats['types_used']) or 'N/A'}")
            print(f"  Constraints Used:     {', '.join(stats['constraints_used']) or 'N/A'}")
            print(f"  Has References:       {'Yes' if stats['has_references'] else 'No'}")
            print()
        
        elif args.command in ['format', 'fmt', 'f']:
            data = load_json_file(args.file)
            formatted = flow.format_json(data, indent=args.indent)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(data, indent=args.indent, ensure_ascii=False))
                print(f"✓ Formatted JSON saved to {args.output}")
            else:
                print(formatted)
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
