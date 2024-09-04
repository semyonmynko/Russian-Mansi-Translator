from sqlalchemy import create_engine
import pandas as pd

# Создание соединения с PostgreSQL через SQLAlchemy
engine = create_engine('postgresql+psycopg2://smynko:cie98vxu@rc1a-5v1hh8zp1edg6u8j.mdb.yandexcloud.net:6432/mansi_russian_translator')

# Чтение данных из CSV
df = pd.read_csv('scraping data/data/dataset_bible.csv', delimiter='|')[['target', 'source']]\
.rename(columns={'target':'mansi_phrase', 'source':'russian_phrase'})
print(df)

# Запись данных в таблицу
df.to_sql(name='phrase_translation', con=engine, if_exists='append', index=False)