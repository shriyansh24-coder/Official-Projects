import os

from services.file_service import scan_project, read_file


SUPPORTED_EXTENSIONS = {
    ".py",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".sql",
    ".json",
    ".xml",
    ".md",
}


class ProjectMemory:

    def __init__(self):
        self.project_path = None
        self.chunks = []

    def load_project(self, project_path):
        """
        Scan the project and build searchable memory.
        """

        self.project_path = project_path
        self.chunks = []

        if not project_path or not os.path.isdir(project_path):
            return

        files = scan_project(project_path)

        for relative_path in files:

            extension = os.path.splitext(
                relative_path
            )[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(
                project_path,
                relative_path
            )

            try:

                content = read_file(full_path)

                if not content:
                    continue

                self._create_chunks(
                    relative_path,
                    content
                )

            except Exception:
                continue

    def _create_chunks(self, file_path, content):
        """
        Break a file into smaller searchable chunks.
        """

        lines = content.splitlines()

        chunk_size = 80

        for start in range(
            0,
            len(lines),
            chunk_size
        ):

            chunk_lines = lines[
                start:start + chunk_size
            ]

            chunk_text = "\n".join(chunk_lines)

            if not chunk_text.strip():
                continue

            self.chunks.append({
                "file": file_path,
                "start_line": start + 1,
                "end_line": min(
                    start + chunk_size,
                    len(lines)
                ),
                "content": chunk_text
            })

    def search(self, query, max_results=5):
        """
        Search project memory using simple keyword matching.
        """

        if not query or not self.chunks:
            return []

        query_words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        results = []

        for chunk in self.chunks:

            text = chunk["content"].lower()
            file_name = chunk["file"].lower()

            score = 0

            for word in query_words:

                if word in text:
                    score += 1

                if word in file_name:
                    score += 2

            if score > 0:

                results.append({
                    "score": score,
                    "file": chunk["file"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "content": chunk["content"]
                })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:max_results]

    def get_context(self, query, max_results=5):
        """
        Return relevant project code as AI-ready context.
        """

        results = self.search(
            query,
            max_results
        )

        if not results:
            return "No relevant project code was found."

        context_parts = []

        for result in results:

            context_parts.append(
                f"""
--- FILE: {result["file"]} ---
LINES: {result["start_line"]}-{result["end_line"]}

{result["content"]}
"""
            )

        return "\n".join(context_parts)

    def clear(self):
        """
        Clear project memory.
        """

        self.project_path = None
        self.chunks = []

    def get_stats(self):
        """
        Return basic memory statistics.
        """

        files = {
            chunk["file"]
            for chunk in self.chunks
        }

        return {
            "files": len(files),
            "chunks": len(self.chunks)
        }