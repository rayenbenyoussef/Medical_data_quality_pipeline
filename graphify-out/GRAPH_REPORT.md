# Graph Report - medical-data-quality-pipeline  (2026-07-02)

## Corpus Check
- 196 files · ~35,912 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 407 nodes · 426 edges · 72 communities (60 shown, 12 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e8fb61e1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_BaseDBConnection|BaseDBConnection]]
- [[_COMMUNITY_DatabaseConnectionError|DatabaseConnectionError]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_Contributing to `dbt-utils`|Contributing to `dbt-utils`]]
- [[_COMMUNITY_🏥 Medical Data Quality Pipeline|🏥 Medical Data Quality Pipeline]]
- [[_COMMUNITY_Generic Tests|Generic Tests]]
- [[_COMMUNITY_SQL generators|SQL generators]]
- [[_COMMUNITY_CHANGELOG|CHANGELOG.md]]
- [[_COMMUNITY_DOCUMENTING ARCHITECTURE DECISIONS|DOCUMENTING ARCHITECTURE DECISIONS]]
- [[_COMMUNITY_The future of `dbt_utils` - break it into more logical chunks|The future of `dbt_utils` - break it into more logical chunks]]
- [[_COMMUNITY_dbt utils v1.2.0|dbt utils v1.2.0]]
- [[_COMMUNITY_dbt utils v1.3.0|dbt utils v1.3.0]]
- [[_COMMUNITY_bug_report|bug_report.md]]
- [[_COMMUNITY_dbt utils v1.1.0|dbt utils v1.1.0]]
- [[_COMMUNITY_dbt utils v1.0.0|dbt utils v1.0.0]]
- [[_COMMUNITY_dbt-utils v0.8.5|dbt-utils v0.8.5]]
- [[_COMMUNITY_dbt-utils v0.7.0|dbt-utils v0.7.0]]
- [[_COMMUNITY_dbt-utils v0.8.6|dbt-utils v0.8.6]]
- [[_COMMUNITY_feature_request|feature_request.md]]
- [[_COMMUNITY_0.9.5|0.9.5]]
- [[_COMMUNITY_dbt-utils v0.6.0|dbt-utils v0.6.0]]
- [[_COMMUNITY_dbt-utils v0.8.3|dbt-utils v0.8.3]]
- [[_COMMUNITY_dbt-utils v0.8.1|dbt-utils v0.8.1]]
- [[_COMMUNITY_dbt-utils releases|dbt-utils releases]]
- [[_COMMUNITY_dbt-utils 0.9.0|dbt-utils 0.9.0]]
- [[_COMMUNITY_dbt-utils 0.7.5|dbt-utils 0.7.5]]
- [[_COMMUNITY_dbt-utils v0.6.5|dbt-utils v0.6.5]]
- [[_COMMUNITY_pull_request_template|pull_request_template.md]]
- [[_COMMUNITY_dbt-utils v0.8.0|dbt-utils v0.8.0]]
- [[_COMMUNITY_dbt-utils v0.7.4|dbt-utils v0.7.4]]
- [[_COMMUNITY_dbt-utils v0.7.4b1|dbt-utils v0.7.4b1]]
- [[_COMMUNITY_dbt-utils 0.9.2|dbt-utils 0.9.2]]
- [[_COMMUNITY_dbt-utils v0.6.4|dbt-utils v0.6.4]]
- [[_COMMUNITY_dbt-utils v0.7.2|dbt-utils v0.7.2]]
- [[_COMMUNITY_dbt utils v1.1.1|dbt utils v1.1.1]]
- [[_COMMUNITY_dbt utils v1.4.0|dbt utils v1.4.0]]
- [[_COMMUNITY_dbt utils v1.4.1|dbt utils v1.4.1]]
- [[_COMMUNITY_utils_minor_release|utils_minor_release.md]]
- [[_COMMUNITY_run_test.sh|run_test.sh]]
- [[_COMMUNITY_dbt-utils 0.9.1|dbt-utils 0.9.1]]
- [[_COMMUNITY_dbt-utils v0.6.1|dbt-utils v0.6.1]]
- [[_COMMUNITY_dbt-utils v0.6.6|dbt-utils v0.6.6]]
- [[_COMMUNITY_dbt-utils v0.7.3|dbt-utils v0.7.3]]
- [[_COMMUNITY_dbt-utils v0.8.4|dbt-utils v0.8.4]]
- [[_COMMUNITY_run_functional_test.sh|run_functional_test.sh]]
- [[_COMMUNITY_entrypoint.sh|entrypoint.sh]]
- [[_COMMUNITY_run_tests.sh|run_tests.sh]]
- [[_COMMUNITY_setup.sh|setup.sh]]
- [[_COMMUNITY_medical-data-pipeline|medical-data-pipeline]]

## God Nodes (most connected - your core abstractions)
1. `BaseDBConnection` - 19 edges
2. `Generic Tests` - 18 edges
3. `DatabaseConnectionError` - 17 edges
4. `MsSqlDBConnection` - 15 edges
5. `PostgresSqlDBConnection` - 15 edges
6. `SQL generators` - 15 edges
7. `🏥 Medical Data Quality Pipeline` - 14 edges
8. `DatabaseError` - 13 edges
9. `QueryError` - 9 edges
10. `Contributing to `dbt-utils`` - 8 edges

## Surprising Connections (you probably didn't know these)
- `MsSqlDBConnection` --uses--> `BaseDBConnection`  [INFERRED]
  src/db_connection/connectors/mssql.py → src/db_connection/base.py
- `PostgresSqlDBConnection` --uses--> `BaseDBConnection`  [INFERRED]
  src/db_connection/connectors/postgres.py → src/db_connection/base.py
- `ConnectionBuilder` --uses--> `BaseDBConnection`  [INFERRED]
  src/db_connection/builder.py → src/db_connection/base.py
- `DBReader` --uses--> `BaseDBConnection`  [INFERRED]
  src/db_connection/reader.py → src/db_connection/base.py
- `DBWriter` --uses--> `BaseDBConnection`  [INFERRED]
  src/db_connection/writer.py → src/db_connection/base.py

## Import Cycles
- None detected.

## Communities (72 total, 12 thin omitted)

### Community 0 - "BaseDBConnection"
Cohesion: 0.06
Nodes (12): ABC, ConfigManager, setup_logger(), BaseDBConnection, ConnectionBuilder, DBReader, DBWriter, CSVRawLoader (+4 more)

### Community 1 - "DatabaseConnectionError"
Cohesion: 0.12
Nodes (10): Exception, LiteralString, DatabaseConnectionError, DatabaseError, QueryError, MsSqlDBConnection, Row, PostgresSqlDBConnection (+2 more)

### Community 2 - "README.md"
Cohesion: 0.08
Nodes (25): Code of Conduct, Cross-database macros, Dispatch macros, get_column_values ([source](macros/sql/get_column_values.sql)), get_filtered_columns_in_relation ([source](macros/sql/get_filtered_columns_in_relation.sql)), get_query_results_as_dict ([source](macros/sql/get_query_results_as_dict.sql)), get_relations_by_pattern ([source](macros/sql/get_relations_by_pattern.sql)), get_relations_by_prefix ([source](macros/sql/get_relations_by_prefix.sql)) (+17 more)

### Community 3 - "Contributing to `dbt-utils`"
Cohesion: 0.08
Nodes (22): About this document, Adding CHANGELOG Entry, Contributing to `dbt-utils`, dbt Labs contributors, External contributors, Getting the code, Implementation guidelines, Installing git (+14 more)

### Community 4 - "🏥 Medical Data Quality Pipeline"
Cohesion: 0.09
Nodes (22): Applied from prior experience, 📊 Data Sources, ✅ Data Validation — Two Layers, 📦 Dependencies (`pyproject.toml`), ⚙️ Features, 🚀 Getting Started, Layer 1 — Python (Pandera), Layer 2 — SQL (dbt tests) (+14 more)

### Community 5 - "Generic Tests"
Cohesion: 0.11
Nodes (18): accepted_range ([source](macros/generic_tests/accepted_range.sql)), at_least_one ([source](macros/generic_tests/at_least_one.sql)), cardinality_equality ([source](macros/generic_tests/cardinality_equality.sql)), equal_rowcount ([source](macros/generic_tests/equal_rowcount.sql)), equality ([source](macros/generic_tests/equality.sql)), expression_is_true ([source](macros/generic_tests/expression_is_true.sql)), fewer_rows_than ([source](macros/generic_tests/fewer_rows_than.sql)), Generic Tests (+10 more)

### Community 6 - "SQL generators"
Cohesion: 0.13
Nodes (15): date_spine ([source](macros/sql/date_spine.sql)), deduplicate ([source](macros/sql/deduplicate.sql)), generate_series ([source](macros/sql/generate_series.sql)), generate_surrogate_key ([source](macros/sql/generate_surrogate_key.sql)), group_by ([source](macros/sql/groupby.sql)), haversine_distance ([source](macros/sql/haversine_distance.sql)), pivot ([source](macros/sql/pivot.sql)), safe_add ([source](macros/sql/safe_add.sql)) (+7 more)

### Community 7 - "CHANGELOG.md"
Cohesion: 0.14
Nodes (13): dbt-utils v0.5.1, dbt-utils v0.6.2, dbt-utils v0.6.3, dbt-utils v0.7.1, dbt-utils v0.8.2, dbt utils v1.3.3, Fixes, Fixes (+5 more)

### Community 8 - "DOCUMENTING ARCHITECTURE DECISIONS"
Cohesion: 0.14
Nodes (11): CONSEQUENCES, CONTEXT, DECISION, DOCUMENTING ARCHITECTURE DECISIONS, STATUS, CONSEQUENCES, CONTEXT, DECISION (+3 more)

### Community 9 - "The future of `dbt_utils` - break it into more logical chunks"
Cohesion: 0.18
Nodes (10): Considered Options, Context and Problem Statement, Decision Outcome, Definition in Core, implementation in adapters, Keep `dbt_utils` as-is, More Information, Pros and Cons of the Options, Split `dbt_utils` into multiple stand-alone packages (+2 more)

### Community 10 - "dbt utils v1.2.0"
Cohesion: 0.22
Nodes (9): 1.1.2, dbt utils v1.2.0, Documentation, Fixes, Fixes, New Contributors, New features, Under the hood (+1 more)

### Community 11 - "dbt utils v1.3.0"
Cohesion: 0.22
Nodes (9): 1.2.1, dbt utils v1.3.0, Documentation, Fixes, Fixes, New Contributors, New features, Under the hood (+1 more)

### Community 12 - "bug_report.md"
Cohesion: 0.22
Nodes (8): Actual results, Additional context, Are you interested in contributing the fix?, Describe the bug, Expected results, Screenshots and log output, Steps to reproduce, System information

### Community 13 - "dbt utils v1.1.0"
Cohesion: 0.25
Nodes (8): 1.0.1, Behind the scenes, dbt utils v1.1.0, Documentation, Fixes, New Contributors, New functionality, What's Changed

### Community 14 - "dbt utils v1.0.0"
Cohesion: 0.29
Nodes (7): Contributors:, dbt utils v1.0.0, Enhancements, Fixes, Migration Guide, New features, Under the hood

### Community 15 - "dbt-utils v0.8.5"
Cohesion: 0.29
Nodes (7): Contributors:, dbt-utils v0.8.5, 🚨 deduplicate ([#542](https://github.com/dbt-labs/dbt-utils/pull/542), [#548](https://github.com/dbt-labs/dbt-utils/pull/548)), Fixes, New features, Quality of life, Under the hood

### Community 16 - "dbt-utils v0.7.0"
Cohesion: 0.33
Nodes (6): Breaking changes, dbt-utils v0.7.0, Features, 🚨 get_column_values, 🚨 New dbt version, Under the hood

### Community 17 - "dbt-utils v0.8.6"
Cohesion: 0.33
Nodes (6): Contributors:, dbt-utils v0.8.6, Fixes, New features, Quality of life, Under the hood

### Community 18 - "feature_request.md"
Cohesion: 0.33
Nodes (5): Additional context, Are you interested in contributing this feature?, Describe alternatives you've considered, Describe the feature, Who will this benefit?

### Community 19 - "0.9.5"
Cohesion: 0.40
Nodes (5): 0.9.3 and 0.9.4, 0.9.5, 0.9.7, Fixes, Fixes

### Community 20 - "dbt-utils v0.6.0"
Cohesion: 0.40
Nodes (5): Breaking changes, dbt-utils v0.6.0, Features, Migration instructions, Quality of life

### Community 21 - "dbt-utils v0.8.3"
Cohesion: 0.40
Nodes (5): Contributors:, dbt-utils v0.8.3, Fixes, New features, Quality of life

### Community 22 - "dbt-utils v0.8.1"
Cohesion: 0.40
Nodes (5): Contributors:, dbt-utils v0.8.1, Fixes, New features, Under the hood

### Community 23 - "dbt-utils releases"
Cohesion: 0.40
Nodes (4): dbt-utils releases, Post-release, Release process, When do we release?

### Community 24 - "dbt-utils 0.9.0"
Cohesion: 0.50
Nodes (4): Changed functionality, dbt-utils 0.9.0, Documentation, Fixes

### Community 25 - "dbt-utils 0.7.5"
Cohesion: 0.50
Nodes (4): Contributors:, dbt-utils 0.7.5, Fixes, Under the hood

### Community 26 - "dbt-utils v0.6.5"
Cohesion: 0.50
Nodes (4): dbt-utils v0.6.5, Features, Fixes, Under the hood

### Community 27 - "pull_request_template.md"
Cohesion: 0.50
Nodes (3): Checklist, Problem, Solution

### Community 28 - "dbt-utils v0.8.0"
Cohesion: 0.67
Nodes (3): 🚨 Breaking changes, Contributors:, dbt-utils v0.8.0

### Community 29 - "dbt-utils v0.7.4"
Cohesion: 0.67
Nodes (3): Contributors:, dbt-utils v0.7.4, Fixes

### Community 30 - "dbt-utils v0.7.4b1"
Cohesion: 0.67
Nodes (3): Contributors:, dbt-utils v0.7.4b1, Under the hood

### Community 31 - "dbt-utils 0.9.2"
Cohesion: 0.67
Nodes (3): dbt-utils 0.9.2, New Contributors, What's Changed

### Community 32 - "dbt-utils v0.6.4"
Cohesion: 0.67
Nodes (3): dbt-utils v0.6.4, Fixes, Under the hood

### Community 33 - "dbt-utils v0.7.2"
Cohesion: 0.67
Nodes (3): dbt-utils v0.7.2, Features, Under the hood

### Community 34 - "dbt utils v1.1.1"
Cohesion: 0.67
Nodes (3): dbt utils v1.1.1, Fixes, New features

### Community 35 - "dbt utils v1.4.0"
Cohesion: 0.67
Nodes (3): dbt utils v1.4.0, New Contributors, What's Changed

### Community 36 - "dbt utils v1.4.1"
Cohesion: 0.67
Nodes (3): dbt utils v1.4.1, New Contributors, What's Changed

## Knowledge Gaps
- **228 isolated node(s):** `run_functional_test.sh script`, `run_test.sh script`, `DBT_PROFILES_DIR`, `medical-data-pipeline`, `entrypoint.sh script` (+223 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseDBConnection` connect `BaseDBConnection` to `DatabaseConnectionError`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `dbt utils v1.3.0` connect `dbt utils v1.3.0` to `CHANGELOG.md`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `dbt utils v1.2.0` connect `dbt utils v1.2.0` to `CHANGELOG.md`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `BaseDBConnection` (e.g. with `ConnectionBuilder` and `MsSqlDBConnection`) actually correct?**
  _`BaseDBConnection` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `DatabaseConnectionError` (e.g. with `MsSqlDBConnection` and `.commit()`) actually correct?**
  _`DatabaseConnectionError` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `MsSqlDBConnection` (e.g. with `BaseDBConnection` and `DatabaseConnectionError`) actually correct?**
  _`MsSqlDBConnection` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `PostgresSqlDBConnection` (e.g. with `BaseDBConnection` and `DatabaseConnectionError`) actually correct?**
  _`PostgresSqlDBConnection` has 4 INFERRED edges - model-reasoned connections that need verification._