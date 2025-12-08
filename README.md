# streaming recommendations

app for netflix content using postgres and python

## project info

- **course:** cs 457 (database systems) and cs 330 (mvc design)
- **database:** postgresql with 10 tables (~8,800 netflix titles)
- **pattern:** mvc architecture with sqlalchemy orm

## requirements

- python 3.10+
- postgresql 12+
- packages in requirements.txt

## setup

1. install dependencies:
```bash
pip install -r requirements.txt
```

2. configure database in `.env`:
```bash
cp .env.example .env
# edit .env with your postgres credentials
```

3. initialize database:
```bash
python scripts/init_db.py
```

4. load netflix data:
```bash
python scripts/seed_data.py
```

## usage

run the app:
```bash
python main.py
```

features:
- swipe on titles (y/n/x)
- get personalized recommendations
- set genre preferences
- data persists between sessions

## database dumps

- `schema_dump.sql` - database schema only
- `data_dump.sql` - full data (8,807 titles)

to restore:
```bash
psql -U myuser -d streaming_recommendations -f schema_dump.sql
psql -U myuser -d streaming_recommendations -f data_dump.sql
```

## data source

## Data Source
Download netflix_titles.csv from Kaggle:
https://www.kaggle.com/datasets/shivamb/netflix-shows

Place in: data/netflix_titles.csv