from typing import Any, Callable, Dict, List

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
    """Example custom action to modify a fact's data."""
    fact.age += 1  # Modify age for demonstration purposes
    print(f"Custom action modified age for {fact.name} to {fact.age}")

class Rule:
    def __init__(self, name: str):
        self.name = name
        self.conditions = []
        self.actions = []
        self.subrules = []

    def add_condition(self, condition: Condition) -> None:
        self.conditions.append(condition)

    def add_action(self, action: Action) -> None:
        self.actions.append(action)
    
    def add_subrule(self, rule: 'Rule') -> None:
        self.subrules.append(rule)

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
            for subrule in self.subrules:
                outcomes.extend(subrule.evaluate(fact))

        return outcomes

def validate_and_append_outcome(facts: List[Fact], rules: List[Rule]) -> List[Fact]:
    validated_facts = []

    for fact in facts:
        validated_fact = fact.__dict__.copy()
        for rule in rules:
            outcomes = rule.evaluate(fact)
            for outcome in outcomes:
                if not outcome.passed:
                    validated_fact[outcome.rule_name] = False
                else:
                    validated_fact[outcome.rule_name] = True

        validated_facts.append(Fact(**validated_fact))

    return validated_facts

if __name__ == "__main__":
    # Define complex condition
    def complex_condition(fact: Fact) -> bool:
        return fact.age >= 21 and fact.occupation == "Software Developer" and fact.salary >= 50000

    # Create complex condition object
    complex_cond = Condition(
        name="Complex Condition: Age>=21, Occupation==Software Developer, Salary>=50000",
        evaluation_function=complex_condition
    )

    # Actions
    print_action = Action(name="Print Fact", execution_function=lambda fact: print("Name: {} Age: {} Occupation: {}".format(fact.name, fact.age, fact.occupation)))
    custom_action = Action(name="Custom Action", execution_function=custom_action)

    # Sample facts
    john = Fact(age=25, name="John Brown", occupation="Software Developer", salary=60000)
    sarah = Fact(age=35, name="Sarah Purple", occupation="Data Engineer", salary=70000)
    barry = Fact(age=27, name="Barry White", occupation="Software Developer", salary=45000)

    # Rule
    rule1 = Rule(name="Complex Rule")
    rule1.add_condition(complex_cond)
    rule1.add_action(print_action)
    rule1.add_action(custom_action)

    rules = [rule1]

    validated_facts = validate_and_append_outcome([john, sarah, barry], rules)

    for fact in validated_facts:
        print(fact.__dict__)
