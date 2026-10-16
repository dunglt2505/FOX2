"""Package the existing integrated report; never regenerate readiness claims."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2]
    if not (root / 'reports/FOX2-SKILLS-INTEGRATED-RELEASE/report.md').is_file():
        raise SystemExit('Integrated report missing; complete review before packaging')
    runpy.run_path(str(Path(__file__).with_name('build_distribution.py')), run_name='__main__')
