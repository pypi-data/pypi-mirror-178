"""
Dice command processor
"""
import random
import re
from chatbots.robot import CompletionReaction, CompletionReactionInterface
from .utils import split_completion, COMMAND_DICE


class DiceCompletionReaction(CompletionReactionInterface):
    """
    Dice command processor
    """
    def check(self, completion: str, variables: dict) -> CompletionReaction:
        for command in split_completion(completion):
            if command.type == COMMAND_DICE:
                items = re.split(r"\n\s*-", command.args)
                items = [item.strip() for item in items]
                items = [item for item in items if item]
                chosen = random.choice(items)
                return CompletionReaction(chosen, True)
        return CompletionReaction(None, False)
