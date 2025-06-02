"""
Model-Based AI Agent Example

This example demonstrates a model-based agent that maintains an internal state
of the world and uses it to make decisions.
"""

class ModelBasedAgent:
    """A model-based agent that maintains internal state of the environment."""
    
    def __init__(self, name="ModelAgent"):
        """Initialize the agent with a name and internal model."""
        self.name = name
        self.actions_taken = 0
        
        # Internal model of the world
        self.model = {
            "room_temperature": "normal",  # cold, normal, hot
            "room_lighting": "normal",     # dark, normal, bright
            "noise_level": "quiet",        # quiet, noisy
            "danger_present": False,       # True if danger detected
            "time_of_day": "day",          # morning, day, evening, night
            "last_meal": 0,                # hours since last meal
            "energy_level": 100            # 0-100 scale
        }
        
        # Action effects on the model (simplified)
        self.action_effects = {
            "turn_on_ac": {"room_temperature": "normal", "energy_level": -5},
            "turn_on_heater": {"room_temperature": "normal", "energy_level": -5},
            "turn_on_light": {"room_lighting": "normal", "energy_level": -1},
            "close_blinds": {"room_lighting": "normal", "energy_level": -1},
            "investigate_noise": {"noise_level": "quiet", "energy_level": -10},
            "eat_food": {"last_meal": 0, "energy_level": +30},
            "rest": {"energy_level": +50},
            "escape": {"danger_present": False, "energy_level": -20}
        }
    
    def update_model(self, percept):
        """Update the internal model based on new percepts."""
        # Parse percept to update model (simplified)
        if "cold" in percept:
            self.model["room_temperature"] = "cold"
        elif "hot" in percept:
            self.model["room_temperature"] = "hot"
            
        if "dark" in percept:
            self.model["room_lighting"] = "dark"
        elif "bright" in percept:
            self.model["room_lighting"] = "bright"
            
        if "noise" in percept:
            self.model["noise_level"] = "noisy"
            
        if "danger" in percept or "smoke" in percept:
            self.model["danger_present"] = True
            
        if "morning" in percept:
            self.model["time_of_day"] = "morning"
        elif "night" in percept:
            self.model["time_of_day"] = "night"
            
        if "hungry" in percept:
            self.model["last_meal"] += 4
            
        # Decrease energy over time
        self.model["energy_level"] -= 2
        if self.model["energy_level"] < 0:
            self.model["energy_level"] = 0
            
        print(f"{self.name} updated model: {self.model}")
    
    def perceive(self, environment_state):
        """Perceive the current state of the environment."""
        print(f"{self.name} perceives: {environment_state}")
        self.update_model(environment_state)
        return self
    
    def think(self):
        """Process the current model and decide on an action."""
        # Priority-based decision making
        
        # First priority: Handle danger
        if self.model["danger_present"]:
            return "escape"
            
        # Second priority: Critical needs
        if self.model["energy_level"] < 20:
            return "rest"
        if self.model["last_meal"] > 6:
            return "eat_food"
            
        # Third priority: Comfort adjustments
        if self.model["room_temperature"] == "cold":
            return "turn_on_heater"
        if self.model["room_temperature"] == "hot":
            return "turn_on_ac"
            
        if self.model["room_lighting"] == "dark" and self.model["time_of_day"] != "night":
            return "turn_on_light"
        if self.model["room_lighting"] == "bright" and self.model["time_of_day"] == "night":
            return "close_blinds"
            
        # Fourth priority: Investigate anomalies
        if self.model["noise_level"] == "noisy":
            return "investigate_noise"
            
        # Default action
        return "do_nothing"
    
    def act(self):
        """Execute the selected action and update the model."""
        action = self.think()
        self.actions_taken += 1
        
        print(f"{self.name} performs action: {action} (Total actions: {self.actions_taken})")
        
        # Update model based on action effects
        if action in self.action_effects:
            for key, value in self.action_effects[action].items():
                self.model[key] = value
        
        return action
    
    def __str__(self):
        """Return a string representation of the agent."""
        return f"Agent '{self.name}' with model: {self.model} and {self.actions_taken} actions taken"


# Example usage
if __name__ == "__main__":
    # Create a model-based agent
    agent = ModelBasedAgent("HomeAssistant")
    
    # Simulate a sequence of environment states
    environment_states = [
        "The room is getting cold as night approaches",
        "It's completely dark now",
        "There is a strange noise coming from outside",
        "The noise stopped but you feel hungry",
        "Morning arrives and the room is bright",
        "There's smoke in the room - danger!"
    ]
    
    # Run the agent through the environment states
    print("=== Model-Based Agent Simulation ===")
    for state in environment_states:
        agent.perceive(state).act()
        print("-" * 50)
    
    print(agent)