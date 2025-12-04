"""
One-time database initialization script

Checks if database is already seeded and only runs seed scripts if empty.
Safe to call on every deployment.
"""
from database import SessionLocal, init_db
from models import Dataset

def is_database_seeded():
    """Check if database has any datasets"""
    init_db()
    db = SessionLocal()
    try:
        count = db.query(Dataset).count()
        return count > 0
    finally:
        db.close()

def initialize_database():
    """Initialize database with seed data if empty"""
    print("\n" + "="*60)
    print("🔍 CHECKING DATABASE STATUS")
    print("="*60 + "\n")
    
    if is_database_seeded():
        print("✅ Database already seeded (found existing datasets)")
        print("   Skipping initialization.\n")
        return
    
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
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        raise

if __name__ == "__main__":
    initialize_database()

