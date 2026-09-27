from ai.client import ask_ai
from services.project_memory import ProjectMemory


class ProjectAI:

    def __init__(self):
        self.memory = ProjectMemory()

    def load_project(self, project_path):
        """
        Load a project into AI memory.
        """

        self.memory.load_project(project_path)

    def ask(self, question):
        """
        Ask Gemini a question using relevant project context.
        """

        context = self.memory.get_context(
            question,
            max_results=5
        )

        prompt = f"""
You are DevPilot, an AI development assistant.

Answer the user's question using the provided
project context.

PROJECT CONTEXT
==================================================

{context}

==================================================

USER QUESTION
==================================================

{question}

==================================================

RULES:

- Use the project context as your primary source.
- Do not invent files, functions, classes, or behavior.
- If the answer cannot be determined from the provided
  context, clearly say that more project context is needed.
- Mention relevant file names when useful.
- Keep the answer practical and concise.
- If code is requested, provide clean code.
"""

        return ask_ai(prompt)