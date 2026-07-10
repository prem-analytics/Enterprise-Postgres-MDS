import re


def analyze_sql(sql):

    if not sql:
        return {}

    sql_upper = sql.upper()

    stats = {
        "Lines": len(sql.splitlines()),
        "SELECT": len(re.findall(r"\bSELECT\b", sql_upper)),
        "JOIN": len(re.findall(r"\bJOIN\b", sql_upper)),
        "LEFT JOIN": len(re.findall(r"\bLEFT JOIN\b", sql_upper)),
        "RIGHT JOIN": len(re.findall(r"\bRIGHT JOIN\b", sql_upper)),
        "INNER JOIN": len(re.findall(r"\bINNER JOIN\b", sql_upper)),
        "CASE": len(re.findall(r"\bCASE\b", sql_upper)),
        "GROUP BY": len(re.findall(r"\bGROUP BY\b", sql_upper)),
        "ORDER BY": len(re.findall(r"\bORDER BY\b", sql_upper)),
        "UNION": len(re.findall(r"\bUNION\b", sql_upper)),
        "WITH": len(re.findall(r"\bWITH\b", sql_upper)),
        "REF": len(re.findall(r"REF\(", sql_upper)),
        "SOURCE": len(re.findall(r"SOURCE\(", sql_upper)),
    }

    return stats
# ==========================================================
# SQL Complexity Score
# ==========================================================

def complexity_score(stats):

    score = (
        stats["JOIN"] * 5
        + stats["CASE"] * 4
        + stats["WITH"] * 3
        + stats["UNION"] * 5
        + stats["GROUP BY"] * 2
        + stats["SELECT"] * 1
        + stats["Lines"] // 10
    )

    if score < 15:
        level = "🟢 Low"

    elif score < 30:
        level = "🟡 Medium"

    elif score < 50:
        level = "🟠 High"

    else:
        level = "🔴 Very High"

    return score, level