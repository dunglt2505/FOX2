---
name: fox2-method-research-validation
description: "Evaluate FOX2 trading/portfolio/risk research quality before an engineering decision."
---

# fox2-method-research-validation

**FOX2 Layer 2 — Domain methods — Agile Lite 0.5.0**

## Activate when
Owner asks to assess a financial, trading, portfolio, AI or model research claim/backtest.

## Input
Paper/experiment, as-of data, method, test and baseline evidence.

## Work to perform
1. Check provenance, sample length, data leakage/look-ahead, survivorship, regime and calibration assumptions.
2. Evaluate out-of-sample, walk-forward, reproducibility, transaction costs/slippage, drawdown, sensitivity and alternative baselines.
3. Distinguish **hypothesis**, synthetic fixture, backtested evidence, independently reproduced study and production-ready behavior. Do not translate a promising study directly into broker/LIVE authorization.
4. Deliver method, strengths/limits, measurable follow-up and whether a narrow safe test is justified. No governance ceremony for a research answer.

## Output
Concise research-evidence verdict and next falsifiable test.

## Responsibility boundary
Owns research validity only. Does NOT certify software, authorize real trades or control code deployment.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
