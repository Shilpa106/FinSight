import re


class TextCleaner:
    def clean(self, text: str) -> str:
        text = self._normalize_line_endings(text)
        text = self._remove_excessive_whitespace(text)
        text = self._normalize_repeated_newlines(text)
        return text.strip()

    def _normalize_line_endings(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _remove_excessive_whitespace(self, text: str) -> str:
        return re.sub(r"[ \t]+", " ", text)

    def _normalize_repeated_newlines(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text)