from services.bigquery_service import *

print("=" * 60)
print("BIGQUERY SERVICE TEST")
print("=" * 60)

print("\nTABLES")
print(get_tables())

table = get_tables()["table_name"][0]

print("\nSELECTED TABLE")
print(table)

print("\nROW COUNT")
print(get_row_count(table))

print("\nCOLUMN METADATA")
print(get_columns(table))

print("\nTABLE PREVIEW")
print(preview_table(table, 5))

print("\nDATASET STATISTICS")
print(get_dataset_statistics())

print("\nSERVICE TEST COMPLETED")