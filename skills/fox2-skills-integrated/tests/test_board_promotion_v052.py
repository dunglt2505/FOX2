import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]


class BoardPromotionContract(unittest.TestCase):
    def setUp(self):
        self.skill = (R / "skills" / "fox2-mgmt-delivery" / "SKILL.md").read_text(
            encoding="utf-8"
        )

    def test_ready_for_board_five_checks_are_explicit(self):
        for term in (
            "OUTCOME_DEFINED",
            "DEPENDENCIES_KNOWN",
            "SOURCE_READY_ENOUGH",
            "ACCEPTANCE_ACTIONABLE",
            "NEXT_SAFE_ACTION_KNOWN",
        ):
            self.assertIn(term, self.skill)

    def test_exact_promotion_decisions_are_explicit(self):
        for term in (
            "KEEP_IN_MASTER_PLAN",
            "PROMOTE_TO_BACKLOG",
            "PROMOTE_TO_DOING",
            "BLOCKED",
        ):
            self.assertIn(term, self.skill)

    def test_wip_is_not_readiness(self):
        self.assertIn(
            "WIP capacity decides `BACKLOG` versus `DOING`; it does **not** decide `READY_FOR_BOARD`.",
            self.skill,
        )

    def test_blocked_requires_real_prerequisite(self):
        self.assertIn("concrete prerequisite prevents the next safe action", self.skill)
        self.assertIn("never use BLOCKED for distant backlog work", self.skill)

    def test_promotion_keeps_same_logical_feature(self):
        self.assertIn("Preserve the same Feature/Whole-WP identity", self.skill)
        self.assertIn("SAME logical task", self.skill)

    def test_board_does_not_mirror_whole_master_plan(self):
        self.assertIn("Do not mirror the entire Master Plan onto the Board", self.skill)


if __name__ == "__main__":
    unittest.main()
