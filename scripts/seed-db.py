from app.db.models.organization import Organization
from app.db.models.user import User
from app.db.transaction import transactional_session
from app.enums.user_role import UserRole


def seed() -> None:
    with transactional_session() as db:
        existing_org = (
            db.query(Organization)
            .filter(Organization.slug == "demo-capital")
            .first()
        )

        if existing_org is not None:
            print("Seed data already exists.")
            return

        organization = Organization(
            name="Demo Capital",
            slug="demo-capital",
        )

        db.add(organization)
        db.flush()
        db.refresh(organization)

        admin_user = User(
            organization_id=organization.id,
            email="admin@demo-capital.com",
            full_name="Demo Admin",
            role=UserRole.ADMIN.value,
            hashed_password=None,
        )

        analyst_user = User(
            organization_id=organization.id,
            email="analyst@demo-capital.com",
            full_name="Demo Analyst",
            role=UserRole.ANALYST.value,
            hashed_password=None,
        )

        db.add_all([admin_user, analyst_user])

        print("Seed data created successfully.")


if __name__ == "__main__":
    seed()