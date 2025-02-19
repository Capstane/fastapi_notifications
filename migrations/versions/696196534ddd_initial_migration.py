"""Initial migration

Revision ID: 696196534ddd
Revises: 
Create Date: 2025-02-16 23:14:13.080386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '696196534ddd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification_type',
    sa.Column('id', sa.Integer(), nullable=False, comment='Идентификатор типа уведомления'),
    sa.Column('code', sa.String(), nullable=False, comment='Код типа уведомления'),
    sa.Column('name', sa.String(), nullable=False, comment='Название типа уведомления'),
    sa.Column('default_text', sa.String(), nullable=False, comment='Шаблон текста уведомления по умолчанию'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='Флаг активности уведомления'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('user_notification_settings',
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Пользователь'),
    sa.Column('email_enabled', sa.Boolean(), nullable=True, comment='Флаг отправки уведомлений на email'),
    sa.Column('telegram_enabled', sa.Boolean(), nullable=True, comment='Флаг отправки уведомлений в Telegram'),
    sa.Column('console_enabled', sa.Boolean(), nullable=True, comment='Флаг логирования уведомлений в консоль'),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False, comment='Идентификатор уведомления'),
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Пользователь'),
    sa.Column('notification_type_id', sa.Integer(), nullable=False, comment='Тип уведомления'),
    sa.Column('data', sa.JSON(), nullable=True, comment='Дополнительные данные для рендеринга сообщения'),
    sa.Column('is_read', sa.Boolean(), nullable=True, comment='Флаг прочтения уведомления'),
    sa.Column('read_at', sa.DateTime(timezone=True), nullable=True, comment='Дата и время прочтения уведомления'),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Дата и время создания уведомления'),
    sa.ForeignKeyConstraint(['notification_type_id'], ['notification_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_user_id'), 'notification', ['user_id'], unique=False)
    op.create_table('user_notification_type_settings',
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Пользователь'),
    sa.Column('notification_type_id', sa.Integer(), nullable=False, comment='Тип уведомления'),
    sa.Column('enabled', sa.Boolean(), nullable=True, comment='Флаг включения уведомлений данного типа для пользователя'),
    sa.ForeignKeyConstraint(['notification_type_id'], ['notification_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_notification_settings.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'notification_type_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_notification_type_settings')
    op.drop_index(op.f('ix_notification_user_id'), table_name='notification')
    op.drop_table('notification')
    op.drop_table('user_notification_settings')
    op.drop_table('notification_type')
    # ### end Alembic commands ###
