from typing import List, Dict, Any, Tuple


class Case:
    """Represents a single CBR case containing problem features and solution actions."""
    def __init__(self, case_id: str, case_name: str, problem: Dict[str, Any], solution: Dict[str, int]):
        self.case_id = case_id
        self.case_name = case_name
        self.problem = problem  # Features: disaster_type, severity_level, affected_population, infrastructure_damage, accessibility_score
        self.solution = solution  # Actions: rescue_teams, ambulances, medical_kits, temporary_shelters

    def __repr__(self):
        return f"<Case {self.case_id} ({self.case_name})>"


class CaseBase:
    """Stores historical disaster cases and provides retrieval/retention mechanisms."""
    def __init__(self):
        self.cases: List[Case] = []

    def add_case(self, case: Case):
        self.cases.append(case)

    def get_all(self) -> List[Case]:
        return self.cases


class CBRSystem:
    """Implements the complete CBR 4R Cycle: Retrieve, Reuse/Adapt, Revise, Retain."""
    
    # Feature weights summing to 1.0
    WEIGHTS = {
        "disaster_type": 0.25,
        "severity_level": 0.25,
        "affected_population": 0.20,
        "infrastructure_damage": 0.15,
        "accessibility_score": 0.15
    }

    # Range normalization for numerical attributes
    MAX_POPULATION = 50000.0  # Upper boundary for population normalization

    def __init__(self, case_base: CaseBase):
        self.case_base = case_base

    # STEP 1: SIMILARITY ASSESSMENT & RETRIEVAL (RETRIEVE)
    def _attribute_similarity(self, key: str, val1: Any, val2: Any) -> float:
        """Calculates normalized local similarity (0.0 to 1.0) for a given attribute."""
        if key == "disaster_type":
            # Exact match for categorical disaster type
            return 1.0 if str(val1).strip().title() == str(val2).strip().title() else 0.0

        elif key in ["severity_level", "infrastructure_damage", "accessibility_score"]:
            # Distance scoring for 1-5 scales: 1.0 - (|val1 - val2| / 4.0)
            diff = abs(int(val1) - int(val2))
            return max(0.0, 1.0 - (diff / 4.0))

        elif key == "affected_population":
            # Normalized difference based on MAX_POPULATION
            diff = abs(float(val1) - float(val2))
            return max(0.0, 1.0 - (diff / self.MAX_POPULATION))

        return 0.0

    def calculate_global_similarity(self, target_problem: Dict[str, Any], historical_problem: Dict[str, Any]) -> float:
        """Computes weighted sum of local attribute similarities."""
        total_score = 0.0
        for key, weight in self.WEIGHTS.items():
            sim = self._attribute_similarity(key, target_problem[key], historical_problem[key])
            total_score += weight * sim
        return round(total_score, 4)

    def retrieve(self, target_problem: Dict[str, Any], k: int = 2) -> List[Tuple[Case, float]]:
        """Retrieves top-k most similar cases from the Case Base."""
        scored_cases = []
        for case in self.case_base.get_all():
            sim = self.calculate_global_similarity(target_problem, case.problem)
            scored_cases.append((case, sim))
        
        # Sort descending by similarity score
        scored_cases.sort(key=lambda x: x[1], reverse=True)
        return scored_cases[:k]

    # STEP 2 & 3: SOLUTION ADAPTATION & REVISION (REUSE & REVISE)
    def adapt_solution(self, target_problem: Dict[str, Any], nearest_case: Case) -> Dict[str, int]:
        """
        Rule-based adaptation scaling solution parameters based on 
        population ratio and severity level difference.
        """
        hist_prob = nearest_case.problem
        hist_sol = nearest_case.solution

        # Population ratio multiplier
        pop_ratio = float(target_problem["affected_population"]) / max(1.0, float(hist_prob["affected_population"]))
        
        # Severity scaling (+20% per severity rank increase)
        sev_diff = int(target_problem["severity_level"]) - int(hist_prob["severity_level"])
        sev_multiplier = 1.0 + (sev_diff * 0.20)

        # Combined adaptation factor
        scale_factor = max(0.5, pop_ratio * sev_multiplier)

        adapted_solution = {}
        for resource, count in hist_sol.items():
            adapted_solution[resource] = max(1, round(count * scale_factor))

        return adapted_solution

    def revise(self, solution: Dict[str, int], max_caps: Dict[str, int]) -> Dict[str, int]:
        """Validates solution against local government inventory capacity constraints."""
        revised_solution = {}
        for resource, qty in solution.items():
            cap = max_caps.get(resource, qty)
            revised_solution[resource] = min(qty, cap)
        return revised_solution

    # STEP 4: LEARNING & RETENTION (RETAIN)
    def retain(self, new_case_id: str, new_case_name: str, problem: Dict[str, Any], solution: Dict[str, int]):
        """Stores a newly resolved disaster scenario into the Case Base."""
        new_case = Case(new_case_id, new_case_name, problem, solution)
        self.case_base.add_case(new_case)
        print(f"[RETAIN] Confirmation: New case '{new_case_id}' ({new_case_name}) successfully stored in Case Base.")


if __name__ == "__main__":
    # Initialize Case Base with Historical Philippines Disaster Data
    cb = CaseBase()
    
    cb.add_case(Case(
        "CASE_001", "Typhoon Ursula (2019)",
        {"disaster_type": "Typhoon", "severity_level": 3, "affected_population": 8000, "infrastructure_damage": 3, "accessibility_score": 4},
        {"rescue_teams": 8, "ambulances": 12, "medical_kits": 300, "temporary_shelters": 5}
    ))
    
    cb.add_case(Case(
        "CASE_002", "Typhoon Odette (2021)",
        {"disaster_type": "Typhoon", "severity_level": 5, "affected_population": 25000, "infrastructure_damage": 5, "accessibility_score": 1},
        {"rescue_teams": 25, "ambulances": 40, "medical_kits": 1200, "temporary_shelters": 20}
    ))
    
    cb.add_case(Case(
        "CASE_003", "Luzon Flash Flood",
        {"disaster_type": "Flood", "severity_level": 3, "affected_population": 6000, "infrastructure_damage": 2, "accessibility_score": 3},
        {"rescue_teams": 6, "ambulances": 10, "medical_kits": 250, "temporary_shelters": 4}
    ))
    
    cb.add_case(Case(
        "CASE_004", "Mindanao Earthquake",
        {"disaster_type": "Earthquake", "severity_level": 4, "affected_population": 18000, "infrastructure_damage": 4, "accessibility_score": 2},
        {"rescue_teams": 18, "ambulances": 30, "medical_kits": 800, "temporary_shelters": 14}
    ))

    cbr = CBRSystem(cb)

    # Maximum operational capacities of the LGU / Emergency Response Unit
    max_capabilities = {
        "rescue_teams": 30,
        "ambulances": 50,
        "medical_kits": 1500,
        "temporary_shelters": 25
    }

    incident_count = len(cb.get_all()) + 1

    while True:
        print("  STEP 0: ENTER NEW DISASTER INCIDENT DETAILS")
        try:
            incident_name = input("Incident Identifier/Name (e.g., Typhoon Egay Urban Flood): ").strip()
            if not incident_name:
                incident_name = f"Incident_{incident_count}"

            d_type = input("Disaster Type (Typhoon / Flood / Earthquake / Fire): ").strip().title()
            severity = int(input("Severity Level (1 = Minor, 5 = Catastrophic): "))
            affected_pop = int(input("Estimated Affected Population (e.g., 15000): "))
            inf_damage = int(input("Infrastructure Damage (1 = Minimal, 5 = Severe): "))
            access_score = int(input("Accessibility Score (1 = Cut off, 5 = Accessible): "))

            target_scenario = {
                "disaster_type": d_type,
                "severity_level": severity,
                "affected_population": affected_pop,
                "infrastructure_damage": inf_damage,
                "accessibility_score": access_score
            }

            print("  STEP 1: SIMILARITY ASSESSMENT & CASE RETRIEVAL (RETRIEVE)")
            retrieved = cbr.retrieve(target_scenario, k=2)
            
            for rank, (case, sim) in enumerate(retrieved, start=1):
                print(f"  Rank {rank}: {case.case_id} ({case.case_name}) | Similarity Score: {sim * 100:.2f}%")

            top_case, top_sim = retrieved[0]
            print(f"\n[SELECTED BASE CASE]: {top_case.case_id} ({top_case.case_name}) with {top_sim * 100:.2f}% Match")
            print(f"Historical Problem Features: {top_case.problem}")
            print(f"Historical Recommended Solution: {top_case.solution}")

            print("  STEP 2 & 3: REUSE, SOLUTION ADAPTATION & REVISION (REVISE)")
            adapted_sol = cbr.adapt_solution(target_scenario, top_case)
            print("Unconstrained Adapted Solution (Raw Scaling):", adapted_sol)

            revised_sol = cbr.revise(adapted_sol, max_capabilities)
            print("Final Approved Response Plan (Capped to Max Inventory):", revised_sol)

            print("  STEP 4: LEARNING & CASE RETENTION (RETAIN)")
            new_id = f"CASE_00{incident_count}"
            cbr.retain(new_id, incident_name, target_scenario, revised_sol)
            incident_count += 1

            print("  UPDATED SYSTEM CASE BASE")
            for c in cb.get_all():
                print(f"  - {c.case_id}: {c.case_name} | Type: {c.problem['disaster_type']} | Severity: {c.problem['severity_level']}")

        except ValueError:
            print("\n[ERROR] Invalid numerical input format. Please enter valid integers for ratings and population.")

        cont = input("\nWould you like to process another disaster incident? (y/n): ").strip().lower()
        if cont != 'y':
            print("\nExiting Case-Based Reasoning DSS System. Program finished.")
            break