"""
Integration test plan:

1. Upload PDF
2. Process text
3. Index document
4. Submit prompt injection query
5. Assert review_required = true
6. Assert review_id is returned
7. List pending reviews
8. Assert review appears
9. Approve review
10. Assert review status = approved
11. Assert human_review.approved audit log exists
12. Create another review
13. Reject review
14. Create another review
15. Edit and approve review
"""