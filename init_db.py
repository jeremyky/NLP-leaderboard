"""
One-time database initialization script

Checks if database is already seeded and only runs seed scripts if empty.
Safe to call on every deployment.

Set FORCE_RESEED=true environment variable to **clear all datasets and
submissions** and then re-run all seed scripts from scratch.
"""
import os
from database import SessionLocal, init_db
from models import Dataset, Submission


def is_database_seeded():
    """Check if database has any datasets"""
    init_db()
    db = SessionLocal()
    try:
        count = db.query(Dataset).count()
        return count > 0
    finally:
        db.close()


def clear_all_data():
    """
    Clear all benchmark data (datasets + submissions).

    This is used when FORCE_RESEED=true so that updated seed scripts
    can fully repopulate the leaderboard with the latest baselines.
    """
    init_db()
    db = SessionLocal()
    try:
        print("⚠️  Clearing existing datasets and submissions...\n")
        # Delete submissions first due to FK constraint
        deleted_subs = db.query(Submission).delete()
        deleted_datasets = db.query(Dataset).delete()
        db.commit()
        print(f"   - Deleted {deleted_datasets} datasets")
        print(f"   - Deleted {deleted_subs} submissions\n")
    finally:
        db.close()


def initialize_database():
    """Initialize database with seed data if empty or FORCE_RESEED=true"""
    print("\n" + "="*60)
    print("🔍 CHECKING DATABASE STATUS")
    print("="*60 + "\n")

    force_reseed = os.getenv("FORCE_RESEED", "false").lower() == "true"

    if is_database_seeded() and not force_reseed:
        print("✅ Database already seeded (found existing datasets)")
        print("   Skipping initialization.")
        print("   Set FORCE_RESEED=true to clear and re-seed.\n")
        return

    if force_reseed:
        print("⚠️  FORCE_RESEED=true - Clearing and re-seeding database...\n")
        clear_all_data()
    else:
        print("📦 Database is empty. Running seed scripts...\n")

    # Run all seed scripts
    try:
        print("1️⃣  Seeding general datasets...")
        from seed_data import seed_database

        seed_database()

        print("\n2️⃣  Seeding finance datasets...")
        from finance_datasets import seed_finance_datasets

        seed_finance_datasets()

        print("\n3️⃣  Seeding multilingual datasets...")
        from multilingual_datasets import seed_multilingual_datasets

        seed_multilingual_datasets()

        print("\n4️⃣  Seeding science datasets...")
        from science_datasets import seed_science_datasets

        seed_science_datasets()

        print("\n5️⃣  Adding baseline models to empty datasets...")
        from seed_missing_baselines import seed_missing_baselines

        seed_missing_baselines()

        print("\n" + "="*60)
        print("🎉 DATABASE INITIALIZATION COMPLETE")
        print("="*60 + "\n")

        # Print summary
        db = SessionLocal()
        try:
            dataset_count = db.query(Dataset).count()
            submission_count = db.query(Submission).count()
            print("📊 Summary:")
            print(f"   - {dataset_count} datasets loaded")
            print(f"   - {submission_count} baseline submissions created\n")
        finally:
            db.close()

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    initialize_database()

