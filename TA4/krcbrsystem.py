# PART 1 — Knowledge Representation (KR) Setup
# Task 1A: Knowledge Base storing facts and categories regarding smart home/weather
knowledge_base = {
    "temperature": 32,      # Category: Temperature (in Celsius)
    "is_raining": True,     # Category: Presence/Weather Status (Boolean)
    "humidity": 85,         # Category: Status/Atmospheric (Percentage)
    "power_status": True,   # Category: Status (Boolean)
    "light_level": "dark"   # Category: Status/Environment ("dark" or "bright")
}


# PART 2 — Implement Rule-Based Reasoning (RBR)
# Task 2A: Define IF-THEN Rules as functions

def rule_hot(facts):
    """Rule 1: If temperature is above 30°C, suggest turning on the aircon."""
    if facts.get("temperature", 0) > 30:
        return "Turn on the aircon"
    return None

def rule_rain(facts):
    """Rule 2: If it is raining, suggest bringing an umbrella."""
    if facts.get("is_raining", False):
        return "Bring umbrella"
    return None

def rule_lighting(facts):
    """Rule 3: If environment is dark and power is on, suggest turning on lights."""
    if facts.get("light_level") == "dark" and facts.get("power_status", False):
        return "Turn on indoor lights"
    return None

# List of all active rules for the inference engine
rules = [rule_hot, rule_rain, rule_lighting]

# Task 2B: Inference Engine
def rbr_inference_engine(facts, rule_set):
    """
    Inference Engine that evaluates all rules against current facts
    and returns a list of inferred actions.
    """
    inferred_actions = []
    for rule in rule_set:
        action = rule(facts)
        if action:
            inferred_actions.append(action)
    return inferred_actions


# PART 3 — Implement Case-Based Reasoning (CBR)
# Task 3A: Build a Case Base with past problems and solutions
case_base = [
    {
        "id": 1,
        "problem": {"won_t_turn_on": True, "noise": False, "overheating": False},
        "solution": "Check power cable and outlet connection."
    },
    {
        "id": 2,
        "problem": {"won_t_turn_on": True, "noise": True, "overheating": True},
        "solution": "Clean internal cooling fan and replace thermal paste."
    },
    {
        "id": 3,
        "problem": {"won_t_turn_on": False, "noise": True, "overheating": True},
        "solution": "Inspect fan blades for physical obstructions."
    }
]

def calculate_similarity(problem1, problem2):
    """Helper method to calculate similarity score based on matching feature values."""
    matching_features = 0
    total_features = len(problem1)
    
    for key in problem1:
        if key in problem2 and problem1[key] == problem2[key]:
            matching_features += 1
            
    return matching_features / total_features if total_features > 0 else 0

# Task 3B & 3C: Retrieve and Reuse Steps
def cbr_retrieve_and_reuse(new_problem, cases):
    """Finds the most similar past case and returns its solution."""
    best_match = None
    highest_similarity = -1.0
    
    for case in cases:
        sim_score = calculate_similarity(new_problem, case["problem"])
        if sim_score > highest_similarity:
            highest_similarity = sim_score
            best_match = case
            
    return best_match, highest_similarity

# Task 3D: Revise Step
def cbr_revise(solution):
    """Allows user/student to manually adjust the solution or keep it unchanged."""
    print(f"\n[CBR - Revise Step] Suggested Solution: '{solution}'")
    user_input = input("Would you like to revise this solution? (yes/no): ").strip().lower()
    
    if user_input == 'yes':
        new_solution = input("Enter the revised solution: ").strip()
        return new_solution
    return solution

# Task 3E: Retain Step
def cbr_retain(cases, new_problem, final_solution):
    """Stores the newly solved case into the case base for future reference."""
    new_case_id = len(cases) + 1
    new_case = {
        "id": new_case_id,
        "problem": new_problem,
        "solution": final_solution
    }
    cases.append(new_case)
    print(f"[CBR - Retain Step] New Case #{new_case_id} retained in Case Base successfully.")


# MAIN EXECUTION / OUTPUT DEMONSTRATION
if __name__ == "__main__":
    # --- RBR DEMO ---
    actions = rbr_inference_engine(knowledge_base, rules)
    print("Rule-Based Reasoning Actions:")
    for action in actions:
        print(f" - {action}")

    # --- CBR DEMO ---
    # Define a new problem query
    new_problem_query = {"won_t_turn_on": True, "noise": True, "overheating": False}
    print(f"New Problem Input: {new_problem_query}")
    
    # 1. Retrieve & Reuse
    matched_case, similarity = cbr_retrieve_and_reuse(new_problem_query, case_base)
    print(f"Most Similar Case Found: Case #{matched_case['id']} (Similarity Score: {similarity * 100:.1f}%)")
    reused_solution = matched_case["solution"]
    
    # 2. Revise
    revised_solution = cbr_revise(reused_solution)
    print(f"Final Solution to Apply: {revised_solution}")
    
    # 3. Retain
    cbr_retain(case_base, new_problem_query, revised_solution)
