# Blog Dmitriy Belkin

## Для запуска:
```bash
uvicorn main:app --reload
```

## Загрузить файл можно так:
```
curl -F "file=@path/to/your/article.md" http://127.0.0.1:8000/upload
```

## Спека по апихе:
http://127.0.0.1:8000/docs

## Инициализация БД:
```bash
python init_db.py
```

## Инициализация Alembic (если еще не выполнена)
```bash
alembic init alembic
```

## Создание миграции:
```bash
alembic revision --autogenerate -m "comment"
```

## Применение миграции:
```bash
alembic upgrade head
```


## Миграционный файл будет выглядеть примерно так:
```
# alembic/versions/<revision_id>_add_disabled_column_to_users.py

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '<revision_id>'
down_revision = '<previous_revision_id>'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('disabled', sa.Boolean(), nullable=True, server_default=sa.false()))

def downgrade():
    op.drop_column('users', 'disabled')
```

## Применение изменений
## Запустите миграции:
```bash
alembic upgrade head
```

## Перезапустите приложение:
```bash
uvicorn main:app --reload
```