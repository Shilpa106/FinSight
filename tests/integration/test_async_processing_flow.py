"""
Integration test plan:

1. Start Redis-compatible server
2. Start Celery worker
3. Start FastAPI
4. Upload PDF
5. Call process-text/async
6. Poll /tasks/{task_id}
7. Assert task status becomes SUCCESS
8. Assert document status becomes text_extracted
9. Call index/async
10. Poll task
11. Assert document status becomes indexed
12. Assert chunks exist
13. Assert Qdrant collection has points
"""