import json

with open("local_schema.sql", "r", encoding="utf-8") as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    if "OWNER TO" in line: continue
    if "GRANT" in line: continue
    if "ALTER DEFAULT PRIVILEGES" in line: continue
    clean_lines.append(line)

clean_sql = "".join(clean_lines)

with open("cleaned_schema.sql", "w", encoding="utf-8") as f:
    f.write(clean_sql)
