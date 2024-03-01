CREATE_IMAGES_TABLE = (
    lambda table_name: f"CREATE TABLE IF NOT EXISTS {table_name}(url VARCHAR);"
)
INSERT_IMAGES = lambda table_name: f"INSERT INTO {table_name}(url) VALUES (?);"
