"""
Database migration script to add admin_role column
Run this once to update your existing database
"""
import sqlite3
import os

# Path to your database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'edutrade.db')

print(f"Connecting to database: {db_path}")

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if column already exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'admin_role' in columns:
        print("[OK] Column 'admin_role' already exists!")
    else:
        print("Adding 'admin_role' column to user table...")

        # Add the admin_role column
        cursor.execute("ALTER TABLE user ADD COLUMN admin_role VARCHAR(20) DEFAULT NULL")

        # Update existing admin users to have super_admin role
        cursor.execute("UPDATE user SET admin_role = 'super_admin' WHERE is_admin = 1")

        conn.commit()
        print("[OK] Successfully added 'admin_role' column!")
        print("[OK] Updated existing admins to 'super_admin' role!")

    # Verify the change
    cursor.execute("SELECT COUNT(*) FROM user WHERE admin_role = 'super_admin'")
    admin_count = cursor.fetchone()[0]
    print(f"[OK] Found {admin_count} super admin(s) in database")

    conn.close()
    print("\n[SUCCESS] Database migration completed successfully!")
    print("You can now restart your Flask application.")

except sqlite3.Error as e:
    print(f"[ERROR] Database error: {e}")
except Exception as e:
    print(f"[ERROR] Error: {e}")
