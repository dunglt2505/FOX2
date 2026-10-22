# FOX2 Skills — Agile Lite 0.5.0

11 Skills in THREE responsibility layers. Layer 1: management (3); Layer 2: professional methods (5); Layer 3: technical/safety (3). **One task, no extra approvals** for ordinary authorized internal coding. Specialized Bridge execution remains controlled by installed Bridge. See `SKILL_MIGRATION_v0_5_0.md` for the mapping of all 17 retired names.

Current operating source: `shared/operating_rules.md`; each Skill is standalone and states its own task, output and boundary. Legacy version-specific shared rules and old tests are retired from active plugin; historical Git commits preserve evidence. Other retained reference files are not extra workflow gates. Use installed machine validators for actual Bridge acceptance. No host E2E claimed.

Tests: `python -m unittest discover -s tests -v` in the 0.5.0 update source. All tests are static/fixtures, not a Windows Bridge host acceptance.
