from main.models import Recipe, Instruction
from main.functions.exceptions import RequiredParameterException
from main.functions import Functions


class CInstruction:
    @staticmethod
    def add_new(text_inst: str, nb: int, recipe: Recipe, level: int = 0, files_replaces: dict = None) -> Instruction:
        """
        Add new instruction to a recipe
        :param text_inst: text of the instruction {str} [REQ]
        :param nb: define order of instructions in the recipe {int} [REQ]
        :param recipe: the recipe to add the instruction {Recipe} [REQ]
        :param level: represent the indentation of the instruction {int} [OPT]
        :param files_replaces: list of files replaces to do in text {dict} [OPT]
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
        if files_replaces is not None:
            text_inst = Functions.replace_files(text_inst, files_replaces)
        inst = Instruction(text_inst=text_inst, nb=nb, recipe=recipe, level=level)
        inst.save()

        return inst

    @staticmethod
    def add_new_list(instructions: list, recipe: Recipe, files_replaces: dict = None):
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
            instr = CInstruction.add_new(text_inst=instruction["text_inst"], nb=instruction["nb"], level=level,
                                         recipe=recipe, files_replaces=files_replaces)
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
        author_url = recipe.author.url
        opened_li = set()
        for instr in instructions:
            level = instr.level
            if level > last_level:
                if last_level > 0:
                    # Remove last li:
                    html = html[:-5]
                    opened_li.add(level)
                for i in range(last_level, level):
                    html += "<ol>"
            elif level < last_level:
                for i in range(last_level, level, -1):
                    html += "</ol>"
                    if i in opened_li:
                        html += "</li>"
                        opened_li.remove(i)
            if level > 0:
                html += "<li>" + Functions.insert_picture(instr.text_inst, author_url) + "</li>"
            else:
                html += "<p>" + Functions.insert_picture(instr.text_inst, author_url) + "</p>"
            last_level = level

        if last_level > 0:
            for i in range(last_level, 0, -1):
                html += "</ol>"
                if i in opened_li:
                    html += "</li>"
                    opened_li.remove(i)

        return html
