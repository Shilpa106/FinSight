from app.document_processing.preprocessors.text_cleaner import TextCleaner


def test_text_cleaner_normalizes_whitespace() -> None:
    cleaner = TextCleaner()

    dirty_text = "Revenue     increased\r\n\r\n\r\nNet income\t improved"
    cleaned_text = cleaner.clean(dirty_text)

    assert cleaned_text == "Revenue increased\n\nNet income improved"