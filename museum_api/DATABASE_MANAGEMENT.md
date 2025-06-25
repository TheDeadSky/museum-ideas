# Database Management Guide

This guide explains how to update your SQLAlchemy tables safely and efficiently.

## Overview

There are several approaches to update database tables, each suitable for different scenarios:

1. **Alembic Migrations** (Recommended for production)
2. **Direct SQLAlchemy Operations** (Development/Simple changes)
3. **Manual SQL** (Advanced cases)

## 1. Alembic Migrations (Production Approach)

Alembic is the official migration tool for SQLAlchemy and is already configured in this project.

### Setup (Already Done)
- ✅ Alembic is installed (`alembic==1.16.2`)
- ✅ Migration directory created (`migrations/`)
- ✅ Configuration files set up (`alembic.ini`, `migrations/env.py`)

### How to Use Alembic

#### Create a New Migration
```bash
# Generate migration automatically by detecting model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration for manual editing
alembic revision -m "Description of changes"
```

#### Apply Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Apply one migration forward
alembic upgrade +1
```

#### Rollback Migrations
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

#### Check Migration Status
```bash
# Show current migration status
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic show <revision_id>
```

### Example: Adding a New Field

1. **Update your model** in `db/models.py`:
```python
class User(Base):
    # ... existing fields ...
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
```

2. **Generate migration**:
```bash
alembic revision --autogenerate -m "Add phone_number to User"
```

3. **Review the generated migration** in `migrations/versions/`

4. **Apply the migration**:
```bash
alembic upgrade head
```

## 2. Direct SQLAlchemy Operations (Development)

For simple changes during development, you can use the utility functions in `db/database.py`.

### Available Functions

- `create_tables()` - Create all tables
- `drop_tables()` - Drop all tables
- `update_tables()` - Drop and recreate all tables (⚠️ loses data)
- `add_column(table_name, column_name, column_type, **kwargs)` - Add a column
- `drop_column(table_name, column_name)` - Drop a column

### Interactive Database Manager

Run the interactive database manager:
```bash
python db_manager.py
```

This provides a menu-driven interface for common database operations.

### Example Usage

```python
from db.database import add_column, drop_column

# Add a new column
add_column('user', 'phone_number', 'VARCHAR(20)', nullable=True)

# Drop a column
drop_column('user', 'old_field')
```

## 3. Manual SQL (Advanced)

For complex changes or when you need full control:

```python
from db.database import engine
import sqlalchemy as sa

with engine.connect() as connection:
    # Add column
    connection.execute(sa.text("ALTER TABLE user ADD COLUMN phone_number VARCHAR(20)"))
    
    # Modify column
    connection.execute(sa.text("ALTER TABLE user MODIFY COLUMN phone_number VARCHAR(50)"))
    
    # Drop column
    connection.execute(sa.text("ALTER TABLE user DROP COLUMN phone_number"))
    
    connection.commit()
```

## Best Practices

### 1. Always Backup Your Data
Before making schema changes, especially in production:
```bash
# MySQL backup
mysqldump -u username -p database_name > backup.sql
```

### 2. Test Migrations in Development First
- Always test migrations in a development environment
- Use sample data that mirrors production

### 3. Use Descriptive Migration Names
```bash
alembic revision --autogenerate -m "Add user phone number field"
alembic revision --autogenerate -m "Increase story text length to 10000 chars"
alembic revision --autogenerate -m "Add index on user telegram_id"
```

### 4. Review Generated Migrations
Always review auto-generated migrations before applying them:
- Check that the changes match your expectations
- Verify foreign key constraints
- Ensure data types are correct

### 5. Handle Data Migration
For non-nullable columns, provide default values:
```python
# In your migration
def upgrade() -> None:
    # Add column with default value
    op.add_column('user', sa.Column('phone_number', sa.String(20), nullable=False, server_default=''))
    
    # Or update existing data first
    op.execute("UPDATE user SET phone_number = '' WHERE phone_number IS NULL")
    op.alter_column('user', 'phone_number', nullable=False)
```

## Common Operations

### Adding a Column
```python
# In your model
new_field: Mapped[Optional[str]] = mapped_column(String(255))

# Migration
def upgrade() -> None:
    op.add_column('table_name', sa.Column('new_field', sa.String(255), nullable=True))
```

### Removing a Column
```python
# Migration
def upgrade() -> None:
    op.drop_column('table_name', 'old_field')
```

### Changing Column Type
```python
# Migration
def upgrade() -> None:
    op.alter_column('table_name', 'column_name', type_=sa.String(500))
```

### Adding Index
```python
# Migration
def upgrade() -> None:
    op.create_index('idx_user_telegram_id', 'user', ['telegram_id'])
```

### Adding Foreign Key
```python
# Migration
def upgrade() -> None:
    op.create_foreign_key('fk_user_course', 'user', 'courses', ['course_id'], ['id'])
```

## Troubleshooting

### Migration Conflicts
If you have migration conflicts:
1. Check the migration history: `alembic history`
2. Identify the conflicting revisions
3. Resolve conflicts manually or reset migrations

### Database Connection Issues
- Verify your database is running
- Check connection settings in `config.py`
- Ensure database credentials are correct

### Rollback Issues
If a migration fails:
1. Check the error message
2. Fix the issue in your models or migration
3. Rollback: `alembic downgrade -1`
4. Re-apply: `alembic upgrade head`

## Environment-Specific Notes

### Development
- Use `update_tables()` for quick schema changes
- Use Alembic for tracking changes
- Test with sample data

### Production
- Always use Alembic migrations
- Test migrations in staging first
- Backup data before applying changes
- Apply migrations during maintenance windows

## Files Overview

- `alembic.ini` - Alembic configuration
- `migrations/env.py` - Alembic environment setup
- `migrations/versions/` - Migration files
- `db/database.py` - Database utilities
- `db_manager.py` - Interactive database manager
- `db/models.py` - SQLAlchemy models 