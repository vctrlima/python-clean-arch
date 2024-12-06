import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.persistence.models.refresh_token_model import RefreshTokenModel
from infra.persistence.models.user_model import UserModel
from sqlalchemy.orm import scoped_session


@pytest.fixture(scope="module")
def setup_db():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Session = scoped_session(sessionmaker(bind=engine))
    RefreshTokenModel.metadata.create_all(engine)
    UserModel.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def create_user(setup_db):
    user = UserModel(
        user=type(
            "User", (object,), {"name": "Test User", "email": "test@example.com"}
        ),
        hashed_password="hashed_password",
    )
    setup_db.add(user)
    setup_db.commit()
    return user


@pytest.fixture
def update_user(setup_db):
    user = UserModel(
        user=type(
            "User",
            (object,),
            {"name": "Test User", "email": "another.test@example.com"},
        ),
        hashed_password="hashed_password",
    )
    setup_db.add(user)
    setup_db.commit()
    return user


def test_refresh_token_model_creation(setup_db, create_user):
    user = create_user
    hashed_token = "hashed_token_123"
    refresh_token = RefreshTokenModel(hashed_token=hashed_token, user_id=user.id)

    assert isinstance(refresh_token.id, uuid.UUID)
    assert refresh_token.hashed_token == hashed_token
    assert refresh_token.user_id == user.id

    setup_db.add(refresh_token)
    setup_db.commit()

    retrieved_token = (
        setup_db.query(RefreshTokenModel).filter_by(id=refresh_token.id).first()
    )
    assert retrieved_token is not None
    assert retrieved_token.id == refresh_token.id
    assert retrieved_token.hashed_token == hashed_token
    assert retrieved_token.user_id == user.id


def test_refresh_token_model_defaults(setup_db, update_user):
    user = update_user
    hashed_token = "hashed_token_456"
    refresh_token = RefreshTokenModel(hashed_token=hashed_token, user_id=user.id)

    setup_db.add(refresh_token)
    setup_db.commit()

    retrieved_token = (
        setup_db.query(RefreshTokenModel).filter_by(id=refresh_token.id).first()
    )
    assert retrieved_token.created_at == retrieved_token.updated_at
