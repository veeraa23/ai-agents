"""
LLM-Based AI Agent Example

This example demonstrates a simple LLM-based agent that uses a language model
to make decisions. This is a simplified implementation and would require an
actual LLM API integration to work.
"""

import json
import time
from typing import Dict, List, Any, Optional


class Tool:
    """A tool that the agent can use to interact with the environment."""
    
    def __init__(self, name: str, description: str, func: callable):
        """Initialize a tool with a name, description, and function."""
        self.name = name
        self.description = description
        self.func = func
    
    def __call__(self, *args, **kwargs):
        """Execute the tool function."""
        return self.func(*args, **kwargs)
    
    def to_dict(self) -> Dict[str, str]:
        """Return a dictionary representation of the tool."""
        return {
            "name": self.name,
            "description": self.description
        }


class LLMAgent:
    """An agent that uses a language model to make decisions."""
    
    def __init__(self, name: str = "LLMAgent"):
        """Initialize the agent with a name and tools."""
        self.name = name
        self.memory: List[Dict[str, str]] = []
        self.tools: Dict[str, Tool] = {}
        self.register_default_tools()
    
    def register_tool(self, tool: Tool) -> None:
        """Register a tool that the agent can use."""
        self.tools[tool.name] = tool
        print(f"Registered tool: {tool.name}")
    
    def register_default_tools(self) -> None:
        """Register default tools for the agent."""
        # Weather tool example
        def get_weather(location: str) -> str:
            """Simulate getting weather data."""
            # In a real implementation, this would call a weather API
            weather_data = {
                "New York": "Sunny, 75°F",
                "London": "Rainy, 60°F",
                "Tokyo": "Cloudy, 70°F",
                "Sydney": "Clear, 80°F"
            }
            return weather_data.get(location, "Weather data not available")
        
        # Search tool example
        def search(query: str) -> str:
            """Simulate a search engine."""
            # In a real implementation, this would call a search API
            return f"Simulated search results for: {query}"
        
        # Calculator tool
        def calculate(expression: str) -> str:
            """Evaluate a mathematical expression."""
            try:
                # Warning: eval can be dangerous in production code
                # This is just for demonstration
                result = eval(expression, {"__builtins__": {}})
                return f"Result: {result}"
            except Exception as e:
                return f"Error calculating: {e}"
        
        # Register the tools
        self.register_tool(Tool("get_weather", "Get the current weather for a location", get_weather))
        self.register_tool(Tool("search", "Search for information on the web", search))
        self.register_tool(Tool("calculate", "Evaluate a mathematical expression", calculate))
    
    def add_to_memory(self, role: str, content: str) -> None:
        """Add a message to the agent's memory."""
        self.memory.append({"role": role, "content": content})
    
    def get_available_tools_prompt(self) -> str:
        """Get a prompt describing the available tools."""
        tools_json = json.dumps([tool.to_dict() for tool in self.tools.values()], indent=2)
        return f"You have access to the following tools:\n{tools_json}"
    
    def simulate_llm_response(self, prompt: str) -> Dict[str, Any]:
        """
        Simulate an LLM response.
        
        In a real implementation, this would call an actual LLM API like OpenAI.
        This is just a simplified simulation for demonstration purposes.
        """
        # Simple keyword-based simulation
        response = {
            "action": None,
            "action_input": None,
            "thoughts": "I need to determine the best course of action."
        }
        
        if "weather" in prompt.lower():
            response["action"] = "get_weather"
            # Extract location (very simplified)
            if "new york" in prompt.lower():
                response["action_input"] = "New York"
            elif "london" in prompt.lower():
                response["action_input"] = "London"
            elif "tokyo" in prompt.lower():
                response["action_input"] = "Tokyo"
            elif "sydney" in prompt.lower():
                response["action_input"] = "Sydney"
            else:
                response["action_input"] = "New York"  # Default
            
            response["thoughts"] = f"The user is asking about weather. I should check the weather in {response['action_input']}."
        
        elif "calculate" in prompt.lower() or any(op in prompt for op in ["+", "-", "*", "/"]):
            response["action"] = "calculate"
            # Very simplified extraction of a math expression
            import re
            match = re.search(r'\d+\s*[\+\-\*\/]\s*\d+', prompt)
            if match:
                response["action_input"] = match.group(0).replace(" ", "")
                response["thoughts"] = f"This looks like a calculation request. I'll compute {response['action_input']}."
            else:
                response["action_input"] = "2+2"  # Default
                response["thoughts"] = "I'm not sure what to calculate, but I'll do a simple calculation."
        
        elif "search" in prompt.lower() or "find" in prompt.lower() or "look up" in prompt.lower():
            response["action"] = "search"
            # Simplistic query extraction
            response["action_input"] = prompt.replace("search", "").replace("find", "").replace("look up", "").strip()
            response["thoughts"] = f"The user wants information. I'll search for '{response['action_input']}'."
        
        else:
            # Default response if no tool seems appropriate
            response["thoughts"] = "I don't have a specific tool for this request. I'll just respond conversationally."
            response["response"] = "I'm not sure how to help with that specific request. Could you try asking something about the weather, a calculation, or a search query?"
        
        # Simulate thinking time
        time.sleep(0.5)
        return response
    
    def process_tool_use(self, action: str, action_input: Any) -> str:
        """Process a tool use action and return the result."""
        if action in self.tools:
            try:
                result = self.tools[action](action_input)
                return f"Tool '{action}' returned: {result}"
            except Exception as e:
                return f"Error using tool '{action}': {e}"
        else:
            return f"Tool '{action}' not found."
    
    def process(self, user_input: str) -> str:
        """Process a user input and return a response."""
        # Add user input to memory
        self.add_to_memory("user", user_input)
        
        # Create prompt for LLM
        tools_prompt = self.get_available_tools_prompt()
        memory_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in self.memory[-5:]])
        prompt = f"{tools_prompt}\n\nConversation history:\n{memory_prompt}\n\nHow would you respond to this?"
        
        # Get LLM response (simulated)
        llm_response = self.simulate_llm_response(user_input)
        
        # Process the response
        if llm_response.get("action") and llm_response.get("action_input") is not None:
            # The LLM wants to use a tool
            action = llm_response["action"]
            action_input = llm_response["action_input"]
            
            print(f"🤔 {self.name} is thinking: {llm_response['thoughts']}")
            print(f"🛠️ {self.name} is using tool: {action}({action_input})")
            
            # Use the tool
            tool_result = self.process_tool_use(action, action_input)
            
            # Create final response
            final_response = f"I used {action} to help answer your question. {tool_result}"
            self.add_to_memory("assistant", final_response)
            return final_response
        
        elif llm_response.get("response"):
            # The LLM provided a direct response
            print(f"🤔 {self.name} is thinking: {llm_response['thoughts']}")
            self.add_to_memory("assistant", llm_response["response"])
            return llm_response["response"]
        
        else:
            # Fallback response
            fallback = "I'm not sure how to respond to that."
            self.add_to_memory("assistant", fallback)
            return fallback


# Example usage
if __name__ == "__main__":
    # Create an LLM-based agent
    agent = LLMAgent("Jarvis")
    
    # Simulate a conversation
    queries = [
        "What's the weather like in London?",
        "Calculate 125 * 37",
        "Search for information about AI agents",
        "Tell me a joke",
        "What's the weather in Tokyo?"
    ]
    
    print("=== LLM-Based Agent Simulation ===")
    for query in queries:
        print(f"\n👤 User: {query}")
        response = agent.process(query)
        print(f"🤖 {agent.name}: {response}")
        print("-" * 50)