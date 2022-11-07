from setuptools import setup

setup(
    name="app_example",
    version="0.0.1",
    author="ZRR",
    author_email="zrr@gmail.com",
    description="Fast API app",
    install_requires=[
        'SQLAlchemy==1.4.42',
        'fastapi==0.85.1',
        'starlette==0.20.4',
        'pydantic==1.10.2',
        'PyJWT==2.6.0',
        'setuptools==60.2.0',
        'alembic==1.8.1',
        'psycopg2-binary==2.9.4',
        'requests==2.28.1',
        'uvicorn==0.18.3',
        'pytest==7.1.3',
    ],
    scripts=['app/main.py', 'app/scripts/create_db.py']
)
