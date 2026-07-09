from app.utils.file_utils import build_storage_key, get_file_extension, sanitize_filename


def test_get_file_extension() -> None:
    assert get_file_extension("report.pdf") == "pdf"
    assert get_file_extension("loan.agreement.docx") == "docx"


def test_sanitize_filename() -> None:
    assert sanitize_filename("annual report.pdf") == "annual report.pdf"
    assert sanitize_filename("bad/file?.pdf") == "bad_file_.pdf"


def test_build_storage_key() -> None:
    key = build_storage_key(
        organization_id="org-1",
        document_id="doc-1",
        filename="report.pdf",
    )

    assert key == "organizations/org-1/documents/doc-1/report.pdf"