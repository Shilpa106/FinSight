from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.reviews import (
    HumanReviewResponse,
    ReviewDecisionRequest,
    ReviewDecisionResponse,
    ReviewEditApproveRequest,
    ReviewListResponse,
)
from app.services.reviews.reviews_service import ReviewService

router = APIRouter()


@router.get("/pending", response_model=ReviewListResponse)
def list_pending_reviews(
    organization_id: UUID,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> ReviewListResponse:
    service = ReviewService(db)

    reviews = service.list_pending_reviews(
        organization_id=organization_id,
        limit=limit,
    )

    return ReviewListResponse(
        reviews=reviews,
        total=len(reviews),
    )


@router.get("/{review_id}", response_model=HumanReviewResponse)
def get_review(
    review_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> HumanReviewResponse:
    service = ReviewService(db)

    try:
        return service.get_review(
            review_id=review_id,
            organization_id=organization_id,
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/documents/{document_id}/items", response_model=ReviewListResponse)
def list_document_reviews(
    document_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
) -> ReviewListResponse:
    service = ReviewService(db)

    reviews = service.list_reviews_by_document(
        document_id=document_id,
        organization_id=organization_id,
    )

    return ReviewListResponse(
        reviews=reviews,
        total=len(reviews),
    )


@router.post("/{review_id}/approve", response_model=ReviewDecisionResponse)
def approve_review(
    review_id: UUID,
    organization_id: UUID,
    request: ReviewDecisionRequest,
    db: Session = Depends(get_db),
) -> ReviewDecisionResponse:
    service = ReviewService(db)

    try:
        review = service.approve_review(
            review_id=review_id,
            organization_id=organization_id,
            reviewer_id=request.reviewer_id,
            reviewer_notes=request.reviewer_notes,
        )

        db.commit()

        return ReviewDecisionResponse(
            review_id=review.id,
            status=review.status,
            message="Review approved.",
        )

    except PermissionError as error:
        db.rollback()
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{review_id}/reject", response_model=ReviewDecisionResponse)
def reject_review(
    review_id: UUID,
    organization_id: UUID,
    request: ReviewDecisionRequest,
    db: Session = Depends(get_db),
) -> ReviewDecisionResponse:
    service = ReviewService(db)

    try:
        review = service.reject_review(
            review_id=review_id,
            organization_id=organization_id,
            reviewer_id=request.reviewer_id,
            reviewer_notes=request.reviewer_notes,
        )

        db.commit()

        return ReviewDecisionResponse(
            review_id=review.id,
            status=review.status,
            message="Review rejected.",
        )

    except PermissionError as error:
        db.rollback()
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{review_id}/edit-approve", response_model=ReviewDecisionResponse)
def edit_and_approve_review(
    review_id: UUID,
    organization_id: UUID,
    request: ReviewEditApproveRequest,
    db: Session = Depends(get_db),
) -> ReviewDecisionResponse:
    service = ReviewService(db)

    try:
        review = service.edit_and_approve_review(
            review_id=review_id,
            organization_id=organization_id,
            reviewer_id=request.reviewer_id,
            final_answer=request.final_answer,
            reviewer_notes=request.reviewer_notes,
        )

        db.commit()

        return ReviewDecisionResponse(
            review_id=review.id,
            status=review.status,
            message="Review edited and approved.",
        )

    except PermissionError as error:
        db.rollback()
        raise HTTPException(status_code=403, detail=str(error)) from error

    except ValueError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error