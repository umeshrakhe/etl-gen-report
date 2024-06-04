from typing import Any
from typing import Callable, Any, Dict, List
from functools import reduce

class Fact:
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)


class Condition:
    def __init__(self, name: str, evaluation_function: Callable[[Fact], bool]):
        self.name = name
        self.eval_func = evaluation_function

    def evaluate(self, fact: Fact) -> bool:
        return self.eval_func(fact)


class RuleOutcome:
    def __init__(self, rule_name: str, passed: bool, message: str = ""):
        self.rule_name = rule_name
        self.passed = passed
        self.message = message


class Action:
    def __init__(self, name: str, execution_function: Callable[[Fact], None]):
        self.name = name
        self.exec_func = execution_function

    def execute(self, fact: Fact) -> None:
        self.exec_func(fact)


def custom_action(fact: Fact) -> None:
    """
    Example custom action to modify a fact's data.
    """
    fact.age += 1  # Modify age for demonstration purposes
    print(f"Custom action modified age for {fact.name} to {fact.age}")


class Rule:
    def __init__(self, name: str):
        self.name = name
        self.conditions = []
        self.actions = []

    def add_condition(self, condition: Condition) -> None:
        self.conditions.append(condition)

    def add_action(self, action: Action) -> None:
        self.actions.append(action)

    def evaluate(self, fact: Fact) -> List[RuleOutcome]:
        outcomes = []
        passed_all = True

        for condition in self.conditions:
            result = condition.evaluate(fact)
            passed_all &= result
            outcomes.append(RuleOutcome(condition.name, result))

        if passed_all:
            for action in self.actions:
                action.execute(fact)

        return outcomes


def validate_and_append_outcome(facts: List[Fact], rules: List[Rule]) -> List[Fact]:
    """
    Processes facts through a list of rules, appending validation outcomes as new columns.

    Args:
        facts (List[Fact]): List of facts to be validated.
        rules (List[Rule]): List of rules to apply to the facts.

    Returns:
        List[Fact]: Updated list of facts with validation outcomes as columns.
    """

    validated_facts = []
    for fact in facts:
        outcomes = []
        for rule in rules:
            outcomes.extend(rule.evaluate(fact))

        # Create a new dictionary with the original fact data and rule outcomes
        validated_fact = dict(fact.__dict__)
        for outcome in outcomes:
            validated_fact[outcome.rule_name] = outcome.passed

        validated_facts.append(Fact(**validated_fact))

    return validated_facts

def load_facts_from_file(file_path: str) -> List[Fact]:
    """
    Loads facts from a CSV file.

    Args:
        file_path (str): Path to the CSV file containing facts.

    Returns:
        List[Fact]: List of facts loaded from the file.
    """

    facts = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            facts.append(Fact(**row))

    return facts
if __name__ == "__main__":
    age_cond = Condition(name="Age>=21", evaluation_function=lambda fact: fact.age >= 21)
    occupation_cond = Condition(name="Occupation==Software Developer", evaluation_function=lambda fact: fact.occupation == "Software Developer")

    print_action = Action(name="Print Fact", execution_function=lambda fact: print("Name: {} Age: {} Occupation: {}".format(fact.name, fact.age, fact.occupation)))
    custom_action = Action(name="Custom Action", execution_function=custom_action)

    john = Fact(age=25, name="John Brown", occupation="Software Developer")
    sarah = Fact(age=35, name="Sarah Purple", occupation="Data Engineer")
    barry = Fact(age=27, name="Barry White", occupation="Software Developer")

   
    
    rule1 = Rule(name="Age and Occupation Rule")
    rule1.add_condition(age_cond)
    rule1.add_condition(occupation_cond)
    rule1.add_action(print_action)
    rule1.add_action(custom_action)  # Add custom action to rule1

    rule2 = Rule(name="Age Rule")
    
    # Load facts from a CSV file
    facts = load_facts_from_file("path/to/facts.csv")

    # Create and evaluate rules on loaded facts
    for fact in facts:
        outcomes = rule1.evaluate(fact)
        # Process outcomes (print, store in database, etc.)
    
    rules = [rule1, rule2]

    validated_facts = validate_and_append_outcome([john, sarah, barry], rules)

    for fact in validated_facts:
        print(fact.__dict__)
