from services.postgres_service import *

print("=" * 60)
print("POSTGRESQL CONNECTION TEST")
print("=" * 60)

print("\nVERSION")
print(get_version())

print("\nDATABASE SIZE")
print(get_database_size())

print("\nACTIVE CONNECTIONS")
print(get_active_connections())

print("\nSCHEMA COUNT")
print(get_schema_count())

print("\nVIEW COUNT")
print(get_view_count())

print("\nDATABASE STATISTICS")
print(get_database_statistics())

print("\nSCHEMAS")
print(get_schemas())

print("\nTABLES")
print(get_tables())

print("\nDATABASE OBJECTS")
print(get_database_objects())

print("=" * 60)
print("TEST COMPLETED")
print("=" * 60)