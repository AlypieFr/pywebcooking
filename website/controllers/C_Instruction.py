from website.models import Recipe, Instruction
from website.functions.exceptions import RequiredParameterException


class CInstruction:
    @staticmethod
    def add_new(text_inst: str, nb: int, recipe: Recipe, level: int = 0) -> Instruction:
        """
        Add new instruction to a recipe
        :param text_inst: text of the instruction {str} [REQ]
        :param nb: define order of instructions in the recipe {int} [REQ]
        :param recipe: the recipe to add the instruction {Recipe} [REQ]
        :param level: represent the indentation of the instruction {int} [OPT]
        :return:
        """
        # Check parameters:
        if text_inst is not None and (not isinstance(text_inst, str)):
            raise TypeError("text_inst must be a string")
        if text_inst is None or len(text_inst) == 0:
            raise RequiredParameterException("text_inst is required and must be not empty")
        if nb is not None and (not isinstance(nb, int)):
            raise TypeError("nb must be an integer")
        if nb is None:
            raise RequiredParameterException("nb is required")
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of Recipe model")
        if recipe is None:
            raise RequiredParameterException("recipe is required")
        if not isinstance(level, int):
            raise TypeError("level must be an integer")

        # Add instruction:
        inst = Instruction(text_inst=text_inst, nb=nb, recipe=recipe, level=level)
        inst.save()

        return inst

    @staticmethod
    def add_new_list(instructions: list, recipe: Recipe):
        # Check parameters and order instructions to add:
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of Recipe model")
        if recipe is None:
            raise RequiredParameterException("recipe is required")
        if instructions is None:
            raise RequiredParameterException("instructions is required")
        else:
            if not isinstance(instructions, list):
                raise TypeError("instructions must be a list")
            for instruction in instructions:
                if not isinstance(instruction, dict):
                    raise TypeError("instructions: each instruction must be a dict")
                for key, value in instruction.items():
                    if not isinstance(key, str):
                        raise TypeError("instructions: keys of each instruction must be string")
                    if key == "nb":
                        if not isinstance(value, int):
                            raise TypeError("instruction: nb must be an integer")
                    if key == "level":
                        if not isinstance(value, int):
                            raise TypeError("instruction: level must be an integer")
                    elif key == "text_inst":
                        if not isinstance(value, str):
                            raise TypeError("instruction: text_inst must be a string")

        # Do the adds:
        instrs = []
        for instruction in instructions:
            level = instruction["level"] if "level" in instruction else 0
            instr = CInstruction.add_new(text_inst=instruction["text_inst"], nb=instruction["nb"], level=level, recipe=recipe)
            instrs.append(instr)

        return instrs

    @staticmethod
    def build_html_for_instructions(recipe: Recipe) -> str:
        # Check parameters:
        if recipe is not None and (not isinstance(recipe, Recipe)):
            raise TypeError("recipe must be an instance of the Recipe class")
        if recipe is None:
            raise RequiredParameterException("recipe is required")

        instructions_query = recipe.instruction_set.iterator()
        instructions = []
        for instr in instructions_query:
            instructions.append(instr)

        instructions.sort(key=lambda k: k.nb)
        html = ""
        last_level = 0
        for instr in instructions:
            level = instr.level
            if level > last_level:
                for i in range(last_level, level):
                    html += "<ol>"
            elif level < last_level:
                for i in range(level, last_level):
                    html += "</ol>"
            if level > 0:
                html += "<li>" + instr.text_inst + "</li>"
            else:
                html += instr.text_inst
            last_level = level

        if last_level > 0:
            for i in range(0, last_level):
                html += "</ol>"

        return html
