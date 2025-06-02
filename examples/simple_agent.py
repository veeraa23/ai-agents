"""
Simple AI Agent Example

This is a basic example of a reflex agent that responds to environment states
with predefined actions.
"""

class SimpleAgent:
    """A simple reflex agent that responds to environment states."""
    
    def __init__(self, name="Agent"):
        """Initialize the agent with a name."""
        self.name = name
        self.percepts = []
        self.actions_taken = 0
        
        # Define simple condition-action rules
        self.rules = {
            "hot": "turn_on_ac",
            "cold": "turn_on_heater",
            "dark": "turn_on_light",
            "bright": "close_blinds",
            "hungry": "find_food",
            "tired": "rest",
            "noise": "investigate",
            "danger": "escape"
        }
    
    def perceive(self, environment_state):
        """Perceive the current state of the environment."""
        self.percepts.append(environment_state)
        print(f"{self.name} perceives: {environment_state}")
        return self
    
    def think(self):
        """Process the current percepts and decide on an action."""
        if not self.percepts:
            return "do_nothing"
        
        current_percept = self.percepts[-1]
        
        # Check if the percept matches any rule condition
        for condition, action in self.rules.items():
            if condition in current_percept:
                print(f"{self.name} decides to: {action}")
                return action
        
        # Default action if no rule matches
        print(f"{self.name} decides to: do_nothing")
        return "do_nothing"
    
    def act(self):
        """Execute the selected action."""
        action = self.think()
        self.actions_taken += 1
        print(f"{self.name} performs action: {action} (Total actions: {self.actions_taken})")
        return action
    
    def __str__(self):
        """Return a string representation of the agent."""
        return f"Agent '{self.name}' with {len(self.rules)} rules and {self.actions_taken} actions taken"


# Example usage
if __name__ == "__main__":
    # Create a simple agent
    agent = SimpleAgent("HomeCare")
    
    # Simulate a sequence of environment states
    environment_states = [
        "The room is dark and cold",
        "There is a strange noise coming from outside",
        "The room is now bright but getting hot",
        "Everything seems normal",
        "There's smoke in the room - danger!"
    ]
    
    # Run the agent through the environment states
    print("=== Simple Agent Simulation ===")
    for state in environment_states:
        agent.perceive(state).act()
        print("-" * 40)
    
    print(agent)