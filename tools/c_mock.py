# Mock exam definition. Item ids must exist in problems.json, sql_problems.json, quiz_prompt.json or quiz_bigo.json (verify.py checks).
# Section weights are points out of 100 and follow the exam priorities: Prompt Engineering, Problem Solving and SQL Foundations count most.
MOCK = dict(
 title="Builder Prep mock exam", minutes=90, pass_percent=60,
 sections=[
  dict(id="prompt", name="Prompt Engineering", weight=30, kind="mixed", focus="#/study/pe_extract", items=["pe01", "pe04", "pe06", "pe09", "pe12", "pe17", "pw01", "pw03"]),
  dict(id="problem", name="Problem Solving", weight=30, kind="python", focus="#/practice", items=["sort_top3", "hm_two_sum", "gr_neighbors"]),
  dict(id="sql", name="SQL Foundations", weight=25, kind="sql", focus="#/sql", items=["sql_high_earners", "sql_austin_orders", "sql_big_departments"]),
  dict(id="bigo", name="Big O", weight=15, kind="mixed", focus="#/lesson/bigo", items=["bo02", "bo06", "bo10", "bo14"]),
 ])
FILES = {"mock_exam.json": MOCK}
