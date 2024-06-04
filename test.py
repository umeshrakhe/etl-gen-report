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
class Action:

    def __init__(self, name: str, execution_function: Callable[[Fact], None]):
        self.name = name
        self.exec_func = execution_function

    def execute(self, fact: Fact) -> None:
        self.exec_func(fact)


class Rule:
    def __init__(self, condition: Condition, action: Action):
        self.conditions = [condition]
        self.actions = [action]

    def add_condition(self, condition: Condition) -> None:
        self.conditions.append(condition)

    def add_action(self, action: Action) -> None:
        self.actions.append(action)

    def evaluate(self, facts: List[Fact]) -> Any:
        def fact_generator(conditions: List[Condition], facts: List[Fact]):
            all_conditions_true = True
            for fact in facts:
                results = map(lambda condition: condition.eval_func(fact), conditions)
                all_conditions_true = reduce(lambda x, y: x and y, results)

                if all_conditions_true:
                    yield fact

        true_facts = list(fact_generator(self.conditions, facts))

        if len(true_facts) > 0:
            for fact in true_facts:
                for action in self.actions:
                    action.exec_func(fact)
if __name__ == "__main__":
  age_cond = Condition(name="Age>=21", evaluation_function=lambda fact: fact.age >= 21)
  occupation_cond = Condition(name="Occupation==Software Developer", evaluation_function=lambda fact: fact.occupation == "Software Developer")
  
  print_action = Action(name="Print Fact", execution_function=lambda fact: print("Name: {} Age: {} Occupation: {}".format(fact.name, fact.age, fact.occupation)))
  
  john = Fact(age=25,name="John Brown", occupation="Software Developer")
  sarah = Fact(age=35,name="Sarah Purple", occupation="Data Engineer")
  barry = Fact(age=27, name="Barry White", occupation="Software Developer")
  
  rule = Rule(condition=age_cond, action=print_action)
  rule.add_condition(occupation_cond)
  
  rule.evaluate([john, sarah, barry])