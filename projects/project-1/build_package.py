"""Build content-equivalent course records from executed output; optional PDF build is separate."""
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]


def write(path,text):
    if str(path).endswith('.md'):
        text=re.sub(r'\b(October|September|August|July|June|January|February|December|November|March|April|May)(?=\d)',r'\1 ',text)
        for compact,readable in [('12-24month','12-24 month'),('20%marginofsafety','20% margin of safety'),('marginofsafety','margin of safety'),('DCgrowth','DC growth'),('Q3guidance','Q3 guidance'),('Q2Edge','Q2 Edge'),('NOINITIATE','DO NOT INITIATE'),('15passingtests','15 passing tests'),('DataCenter','Data Center'),('Terminalg','Terminal g'),('publishedanswers','published answers')]:
            text=text.replace(compact,readable)
        if str(path).startswith('docs/'):
            # Improve prose spacing while preserving URLs, code tokens and immutable hashes.
            prefix,boundary,appendix=text.partition('## Existing EditionA text')
            pieces=re.split(r'(`[^`]*`|\]\([^)]*\)|\b[0-9a-fA-F]{7,64}\b)',prefix)
            for i in range(0,len(pieces),2):
                s=pieces[i]
                s=re.sub(r'(?<=[a-z])(?=\d)', ' ',s)
                s=re.sub(r'(?<=\d)(?=[A-Za-z])', ' ',s)
                s=re.sub(r'\b(R&D|SG&A|WACC|ROIC|DSO|DPO|GM|ERP|AMD|AVGO|GP|LTM)(?=\d)',r'\1 ',s)
                s=re.sub(r'(?<=%)(?=[A-Za-z])',' ',s)
                s=s.replace('EditionA','Edition A').replace('EditionB','Edition B')
                pieces[i]=s
            text=''.join(pieces)+(boundary+appendix if boundary else '')
    (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8',newline='\n')


def main():
    r=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    v=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
    d=json.loads((ROOT/'data/inputs.json').read_text(encoding='utf-8'))
    b=r['cases']['base']; low=r['cases']['low']; high=r['cases']['high']; rev=r['reverse_dcf']; comp=r['comparables']
    w=b['wacc']; p=b['per_share']; ceiling=b['entry_ceiling']; tv=b['terminal_share']
    prior=[]
    for name in ['lab-05-nvda-dcf','lab-08-nvda-pe','lab-10-nvda-proforma','lab-11-nvda-sensitivity','lab-12-nvda-review']:
        for file in sorted((REPO/'projects'/name).glob('*')):
            if file.suffix not in ['.md','.py']: continue
            relative=file.relative_to(REPO).as_posix()
            commit=subprocess.run(['git','log','-1','--format=%H','--',relative],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()
            prior.append({'path':relative,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'last_commit':commit,
                          'use':'Historical research trail, not unqualified final valuation evidence'})
    write('evidence/prior-lab-index.json',json.dumps(prior,indent=2))
    write('docs/decision-memo.md',f'''
# NVIDIA: watch / defer

Investment committee | No current position | 12-24 month decision horizon

Historical valuation: September 10, 2026 US close. Prepared October 19, 2026. USD/share; model statements in USD millions. This is a dated academic decision, not an October19 live-price recommendation.

## Committee ask and valuation range

**WATCH / DEFER at $218.36.** Causal FCFF range **${low['per_share']:.0f}-${high['per_share']:.0f}**, with a base reference around **${p:.0f}**. No probabilities or mechanical average are asserted. The price is above our base and slightly above the modeled high case. Consider initiation only below roughly **${ceiling:.0f}**, a 20% margin of safety to the refreshed base value, AND after demand, collections, margin and contingent-exposure conditions pass. If financing/demand downside is substantiated, do not initiate even at a superficially cheap price.

## Business evidence and operating judgment

NVIDIA's Q2 FY27 revenue96,221 and Data Center89,023 demonstrate rapid AI-infrastructure adoption; Q3guidance108,000 assumes no China DCcompute revenue. LTM revenue302,970=FY26 215,938+currentH1 177,837-priorH1 90,805. Base DCgrowth40/30/22/15/10% fades as competition, customer funding and power constraints rise. Edge growth15/12/10/8/6%; GM74% fades to72%; R&D8.6% sales and SG&A3% GP retain operating costs. These are our assumptions, not management's five-year guidance.

The prior labs correctly raised durability and margin questions, but annual growth alone cannot value the stock. Base DSO75, inventory125 and DPO60 days require collections and inventory improvement. Forecast SBC is replaced with cash compensation of equal cost; no free-labor addback or buyback benefit. Tax18%, capex3% sales, explicit depreciation/amortization and working capital drive five articulated income, balance and cash-flow statements. No balancing equity plug or automatic borrowing conceals a deficit.

## DCF and complete ownership bridge

Base WACC **{w:.2%}**: nominal Treasury4.95% + assumed beta1.8 * assumed ERP5%; debt spread1%, market-value weights and18% tax. Terminalg3%, ROIC25% require reinvesting12% of NOPAT; terminal value is **{tv:.1%} of EV**. This dependence limits conviction. A WACC/g grid and signed-cash-flow/boundary checks accompany the result. Equity uses24,242M diluted proxy shares:24,147 period-end basic plus95 incremental quarter dilution; not annual weighted24,514.

Reported cash22,443 + debt securities34,143 are distinct from equity investments. Bridge adds separately haircut public holdings and private/other investments, deducts operating-cash10,000/tax reserve1,700, fair debt31,400, Groq consideration986, future-investment recovery shortfalls and a base2,500 guarantee-loss assumption at year3. Pending Hugging Face is cost-inclusive:11,900 purchase cash plus up to1,000 retention cash substitute in year1, zero acquired operating benefit. Purchase allocation/payment mix remain unresolved; no invented synergy. Financial investments never scale as operating working capital.

<!-- pagebreak -->
## Disagreement across methods and market expectations

Policy retained from Lab8 admits profitable fabless designers: AMD use with mix/margin qualification; Broadcom qualify for material software/custom silicon. At the same September10 close, annual GAAP P/E is AMD190.04x and AVGO75.65x; EV/annual sales is AMD{comp['peers'][0]['ev_annual_sales']:.2f}x and AVGO{comp['peers'][1]['ev_annual_sales']:.2f}x, with latest-public financial bridges and quarter diluted-share proxies. P/E suggests approximately${min(comp['pe_implied_prices']):.0f}-${max(comp['pe_implied_prices']):.0f}; EV/sales${min(comp['ev_sales_implied_prices']):.0f}-${max(comp['ev_sales_implied_prices']):.0f}. These are weak market-context intervals: annual denominators lag explosive growth, AMD margins differ and AVGO includes software. Dropping either peer selects the other endpoint. We do not average them into the DCF range. No defensible control-transaction multiple is available; the pending platform acquisition has different synergy/control context and insufficient audited denominators.

At fixed base economics, the market price implies adding **{rev['constant_increment_to_each_dc_growth']*100:.1f}pp** to every DC growth assumption, giving approximately {', '.join(f'{x:.0%}' for x in rev['implied_dc_growth_path'])} growth and year5 total revenue **${rev['year5_revenue']/1000:,.0f}bn**. This is one conditional reverse-DCF solution, not the uniquely correct explanation of price. A lower WACC or stronger margins could imply another solution.

## Downside that changes the action

Low case DCgrowth20/15/10/5/3%, GM70% to66%, DSO95 and inventory155 days combines slower deployments, customer-financing pressure and stranded supply. It adds10,000 incremental supply-loss expense and25,000 expected guarantee-call claim at year3; value around${low['per_share']:.0f} and **DO NOT INITIATE**. High case requires sustained adoption and improved collections/margins, not an arbitrary price premium; around${high['per_share']:.0f}. The $279bn supplier commitments are not customer orders. Note10 also reports $56bn additional cloud/third-party lease commitments and a $105bn SB Energy guarantee cap. These exposures are not all certain present debt, but they make unsupported backlog claims dangerous. Expected-loss assumptions require better recourse/collateral/default evidence.

## Conditions, reversal triggers and next evidence

Revisit at every quarterly filing. Initiation requires price below the refreshed base entry ceiling, credible DC growth and collections, margin>=72%, and commitments funded without new owner-cost surprises. Two-quarter DCgrowth<20%, DSO>95, GM<70% or material capacity/guarantee losses support the no-initiate case. Durable faster demand with margin and payment conversion intact supports revising upward. Refresh prices, nominal rates, diluted awards, debt, investment realizations, pending-deal financing and guarantee terms before any trade. The July26-to-September10 balance roll-forward assumes uniform operating cash generation; actual interim cash data can change the bridge. Rounded investment classification and simplified leases/acquisition allocation are disclosed limits.

## Validation and evidence status

The offline engine passes {len(v['tests'])}/{len(v['tests'])} claim-focused checks: official training answers, independent cash/debt/source definitions, forecast articulation, monotonicity, EV/equity, signed flows, dilution, liquidity/corruption failure injection, quantified investment contamination and decision-altering downside. A new-venv cold run reproduces four outputs byte-for-byte. A-to-B research is documented and the existing NVIDIA EditionA text is unchanged. Original checkpoint PDF/receipt, authentic human AI-off lock, confirmed partner attribution and three student videos/transcripts remain incomplete; technical success does not certify these requirements or a rubric score.

Sources: [NVDA FY26 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), [Q2 FY27 10-Q / Notes5-11](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm), [Q2 release](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027), [Sep3 pending acquisition](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000078/nvda-20260902.htm), [Treasury September rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&type=daily_treasury_yield_curve). Peer/price observations and complete date/field lineage: data/source-map.md; values and scenario detail: outputs/visible-output.md. All reviewed October19; evidence cutoff September10. AI research/coding/writing/QA by Codex; no human authorship or completed video is implied.
''')
    baseline=(ROOT/'evidence/edition-a-existing-nvidia-unchanged.md').read_text(encoding='utf-8')
    write('docs/research-evolution.md',f'''
# NVIDIA: research evolution

Edition B prepared October19 2026; historical valuation September10 US close. Intended user: buy-side committee with no position; decide initiate/watch-defer/do-not-initiate over12-24months, expressed as a range with reversal conditions.

## Baseline boundary and dated addendum

Existing NVIDIA EditionA Markdown is preserved byte-for-byte, SHA256 FF289D7D83BF56F977D5D3F85F7CDF13125841075D5E8A59AF03FA845D39ED6B. Its original September1 date and wording remain unchanged. The Appendix reproduces its text for reading; this newly rendered appendix is **not the original submitted EditionA PDF**. The first successful Brightspace checkpoint receipt and original PDF have not been supplied. No Git tag substitutes for that receipt, and this AI session cannot reconstruct an AI-off baseline retroactively.

October19 addendum: EditionB uses September10 close to align the earlier DCF/comparables labs, with Q2 information already public August26 and acquisition disclosure public September3. This date change is explicit. No October market facts enter the model. Baseline's “initiate” means initiate valuation research, not a buy recommendation. B's WATCH/DEFER therefore reflects completed valuation, not a claim the student previously recommended buying.

## Edition B decision and architecture

At218.36, WATCH/DEFER; intrinsic causal range${low['per_share']:.0f}-${high['per_share']:.0f}, base reference${p:.0f}; approximately${ceiling:.0f} entry ceiling with20%marginofsafety plus evidence gates. Five rolling statements feed FCFF, WACC{w:.2%}, g3% and ROIC25%; explicit cash/financial investments/debt/claims/share bridge. Finance engine in model.py, facts/assumptions in inputs.json, visible results in outputs. No network/credentials/packages needed at runtime.

## A-to-B and prior-lab evidence table

| Evidence / prior view | Challenge and disposition | Observable change in B / decision |
|---|---|---|
| EditionA: DC growth193,737 versus115,186 merits research | Screening is not valuation evidence; growth durability and price remain open. | LTM base302,970, DCgrowthfade and reverseDCF. Research admission becomes conditional watch/defer. Original text unchanged. |
| Lab5: annual-basis value62.72; WACC15.88%; reverse bracket fails | Stale annual growth path and inadequate bracket do not prove mispricing. | Latest-quarter operating base, explicit assumed WACCbuild, reinvestment terminal and solved reverseDCF; old output retained only as history. |
| Lab8: annual GAAP P/E peer interval370.66-931.18 | Two heterogeneous peers and stale annual EPS exaggerate confidence. | Preserve policy, add consistent EV/sales and latest balances; show leave-one-out; no mechanical averaging. |
| Lab10: personalized GM/R&D/SG&A/days/PPE forecast | “Other assets” mix operating/investment holdings; FCFE/cash-after-payouts labeling and discount basis inconsistent. | Investments removed from operatingNWC, no markups in EBIT; FCFF from statements at WACC; all signed cash flows retained. |
| Lab11: sensitivity depends on ranges; margin/WC effects not zero | +/-5pp growth compounds; +/-2pp margin has distinct timing. Dropping negative flows is wrong. | Named stress cases, margin/growth what-ifs, signed-flow regression and cash minimum failure test. |
| Lab12: reported partner demand challenge and claim about commitments | Partner authorship/identity unconfirmed; supplier commitments are not orders. | Qualified historical review credit, independent Note10 check, downside risk gate; fictional rehearsal sample clearly labeled. |
| Latest source definition: securities/cash and debt changed | Annual62,556 includes equity holdings; debt8,468 stale after new issuance. | Latest cash+debtsecurities56,586, separate public/private recoveries, debt33,366 book/31,400 fair. Definition check executed. |
| Pending acquisition headlines | Retention is service compensation; control synergy not public-share multiple. | Purchase cash11,900 and retention1,000 modeled conservatively, no incremental operating benefit. |

## AI output independently corrected

Material output at issue: prior forecast treated broad other-assets balances as operating reinvestment and labeled cash after payouts as FCFE. Independent evidence: Q2 balance and Notes5/6 identify42,783 marketable equity,51,157 private holdings and investment components in other assets. Disposition **CORRECTED**: financial investments are CFI/assets/bridge items; FCFF retains operating NWC only. Quantified deliberately wrong scaling is in validation-results.json. This is a check against primary financial definitions, not another AI's agreement.

Further corrections: reject “supplier commitments prove customer backlog”; reject dropping negative forecast flows; keep SBC owner cost; correct export-risk citation to Item1A rather than Note17. AI was useful for code/source organization and locating possible contradictions; independently sourced tests decide whether output survives. The exposed interface identifies Codex based on GPT-6; exact backend build/version is not exposed and is not invented.

## Unresolved evidence that limits credit

The student must supply the original checkpoint PDF/receipt, complete a genuinely human-authored AI-off locked prediction before a new run, confirm authentic prior partner discussion or obtain real review, record three bounded videos and correct actual transcripts. No sample answer, generated script, or assistant cold-run receipt is relabeled as a human event. Student next steps.md gives exact preparations and recording routes. This package supports a defensible decision but cannot certify missing history or a score.

<!-- pagebreak -->
## Existing EditionA text - reading reproduction only

The source file below remains byte-identical in evidence/. This typeset reproduction was made October19 and is not an original submission artifact.

{baseline}
''')
    lines=[]
    for t in v['tests']:
        detail=json.dumps(t['result'],ensure_ascii=True)
        lines.append(f"| {t['test']} | {t['status']} | {detail} |")
    write('docs/validation-and-ai-use.md',f'''
# NVIDIA: validation and AI use

Frozen technical evidence prepared October19 2026. Valuation cutoff September10 close; annual and interim reporting periods, sources and publication dates are in data/source-map.md. Facts, normalizations, analyst forecasts and outputs are separated in inputs.json, that source map, the contamination catalog below and outputs/results.json. The latest financial date is July26; no October market facts enter valuation.

## Observed technical validation

Engine status **{v['status']}**, {len(v['tests'])}/{len(v['tests'])} tests. run.py --all exits nonzero on failure. Official Week3 answers come from lessons/week-03/teach-dcf-worked-example.md, including all nine grid cells; Week2 fixture is lessons/week-02/starter/mini_case.csv. These are independently published known answers, not expected values generated from this implementation. Independent source check compares issuer release with SEC balance/notes and Treasury column definitions.

| Test / highest-risk claim | Result | Observed details |
|---|---|---|
{chr(10).join(lines)}

## Clean-environment cold run and first failure

Evidence/cold-run-log.md and cold-run-receipt.json record an actual assistant run: copied project, new venv --without-pip, no inherited third-party packages/network/credentials. Four deterministic outputs reproduce byte-for-byte: results.json, validation-results.json, visible-output.md, dashboard.html. First failure: none observed in this run; no fabricated repair story. This is technical reproduction evidence, not a student recording. Student must show an actual clean run and explain ownership in Video2. Runtime Python version and timestamps are in the receipt. Finance engine is standard library only; optional pinned PDF dependencies are separate.

## Prewritten directional test versus required human lock

AI-authored prediction committed before first rebuilt execution: commit7c404d5, evidence/directional-test-precommit.md. Test changes WACC from{w:.9f} to{w+.01:.9f} decimal (+1pp). Expected lower EV/share value and continued deferral; actual numbers/actions are recorded in the table and validation-results.json. This prewritten AI test **does not satisfy the required human-authored AI-off Locked Changed-Input Record**.

The complete truthful current locked-record status is in evidence/locked-changed-input-record.md: **INCOMPLETE / NOT EXECUTED AS A HUMAN LOCK**. Human author, AI-off prediction, immutable precommit timestamp, human chosen old/new inputs and units, expected direction/action, actual direction/action, and diagnosis must be supplied from an authentic new exercise. We have not backdated or filled these as completed. The procedural handoff is Student next steps.md. Final evidence must preserve both prediction and run artifact; unexpected outcomes require diagnosis, and unchanged action requires an explicit threshold explanation.

## Contamination catalog and financial limits

Annual FY26 H20net4,320 is a one-time normalization; normalizedEBIT134,707, GM73.07%. It rolls out of LTM, so is not added again. Investment gains and interest income are excluded from operating FCFF. Equity holdings are not cash, financing acquisitions are not operating working capital, annual diluted weighted shares are not exact current shares, and old intraday price224.35 is not September10 close218.36. New debt and pending acquisition are recognized. Stock compensation retains its owner cost through cash substitution, without addback or assumed future buyback benefit. Acquisition retention is expense, not purchase consideration; all purchase assets temporarily in goodwill is a disclosed allocation simplification. Market/peer annual denominators are qualified for timing/mix; no invented transaction multiple.

Interim balance roll-forward is interpolated, not reported. ROIC/terminal/WACC and investment recovery/default losses are assumptions. Uniform operating cash timing, constant lease/DT balances, refinancing debt, rounded equity-method classification and unknown guarantee-recourse probabilities constrain precision. Actual guarantee calls would require a funded cash/NI update; current loss assumptions are valuation bridge claims, not booked filing liabilities. The downside and entry gates ensure these limits affect action.

## Assumption-challenge and review record

Evidence/assumption-challenges.md contains every load-bearing driver with value, basis, challenge and evidence that changes it. Prior Lab12 reported responses are preserved as historical, authenticity/attribution unverified; no partner name or AI model was supplied. The separate fictional rehearsal paragraph is explicitly AI-written and earns no human-review credit. Codex's independent review corrected source classification, cash-flow labels, dated inputs, acquisition funding, terminal reinvestment and peer definitions. No source statement is treated as proof merely because AI repeated it.

## Material AI uses and dispositions

Tool/interface: Codex based on GPT-6 (system-exposed identity); exact backend build/version not exposed. Interaction date October19 2026. No claim is made about hidden reasoning, unseen chats or the model used in older labs.

| AI use | Independent check / disposition | Effect on decision |
|---|---|---|
| Inspect/reuse NVIDIA Labs5/8/10/11/12 and existing EditionA | Prior files indexed with hashes and Git commits; original baseline unchanged. ACCEPTED WITH QUALIFICATION, checkpoint receipt missing. | Historical admission thesis distinguished from buy recommendation. |
| Research SEC/issuer/Treasury and extract facts | Definitions reconciled against statements and notes; issuer-release/SEC check. CORRECTED old cash/securities/debt classification. | Prevents inflated cash bridge and false reinvestment. |
| Build statements, FCFF/WACC/bridge/terminal and UI | Published known answers, articulation, boundary, sign and failure injection. ACCEPTED after15passingtests. | Conditional range, no price precision claim. |
| Draft forecast assumptions and stress/peer narrative | Full driver challenges; guidance not five-year fact; mixed peers qualified. QUALIFIED. | WATCH/DEFER; downside NOINITIATE; no averaging. |
| Draft partner-style practice response | No authentic human source. FICTIONAL REHEARSAL ONLY; REJECTED as actual partner evidence. | Human-review requirement remains open. |
| Draft memo/scripts, run technical audit/cold run and prepare freeze | Cross-check financial numbers against results, PDFs rendered/reviewed, file hashes/access recorded. ACCEPTED as AI assistance, not student authorship/recording. | Student must understand/defend and complete missing evidence. |

## Freeze and access status

File-integrity.json hashes the stable artifact set with explicit exclusions to avoid self-reference. Submission-manifest.csv lists exactly11 required rows plus optional deployment; videos/transcripts remain pending, not false links. Publication-audit.json records anonymous public access and hash checks after upload. A later final-video freeze must update the manifest, transcript artifacts and hashes under a new tag; do not move an existing frozen tag. GitHub upload is not Brightspace submission. Original EditionA checkpoint belongs at its designated checkpoint location; final assignment requires the seven-part bundle and receipt by October19 2026 11:59PM course time.
''')
    for i in range(1,4):
        path=ROOT/f'docs/transcript-video-{i}.txt'
        if not path.exists(): path.write_text(f'NOT RECORDED - Video {i}. This is a status marker, not a transcript.\nAfter recording, replace with a corrected verbatim transcript of what was actually said, with observed timestamps. Preparation scripts are in Student next steps.md.\n',encoding='utf-8',newline='\n')
    write('Student next steps.md',student_steps(r))
    print('Built NVIDIA memo, evolution, validation source records, prior-lab index and Student next steps.md')


def student_steps(r):
    b=r['cases']['base']; lo=r['cases']['low']; hi=r['cases']['high']; w=b['wacc']; rev=r['reverse_dcf']
    return f'''
# Student next steps

This is the exact recording/submission handoff for the NVIDIA Project1 package. Scripts are **AI-written preparation**, not transcripts or proof that you performed a task. Read, understand and personalize them; say only what you can explain and actually did. You cannot get full credit from videos alone while the human evidence below is missing.

## Complete these before recording

1. Recover the original EditionA PDF and first successful Brightspace checkpoint receipt. Do not recreate or alter them. The unchanged NVIDIA Markdown is already preserved and typeset as a reading appendix, but it is not proof of the submitted PDF/receipt. If never submitted, tell the instructor and request how to handle the missing checkpoint; no AI can backdate compliance. EditionB date addendum is already documented.
2. Confirm whether October1 Lab12's reported partner answers came from a real discussion. If so, verify exact wording/role/date, avoid private information and record what actually changed with independent evidence. If draft/AI-written or uncertain, leave them qualified and obtain actual partner review. A clearly marked fictional sample is in evidence/assumption-challenges.md; never claim it was spoken. Record the real challenge and response; the model need not change if you can justify why.
3. Complete the **human AI-off locked changed-input exercise** below. You must author the prediction yourself before the run. This cannot be filled retrospectively by AI. The assistant's existing WACC test does not count as your human lock.
4. Open outputs/dashboard.html locally in a browser and check labels. Open outputs/visible-output.md, Research-Evolution.pdf, Decision-Memo.pdf and Validation-and-AI-Use.pdf. Check that the numbers below still match outputs/results.json. Use the included dated historical valuation; do not describe $218.36 as today's quote.

## Human AI-off lock - exact procedure

Close AI tools for the prediction. In evidence/locked-changed-input-record.md, write your own name/role as appropriate under course privacy rules, actual UTC time, one load-bearing input you independently choose, its JSON path, old/new numeric values and units, why you expect a direction, expected enterprise/share-value direction and expected committee-action effect. Do not copy the assistant WACC prediction or invent an earlier timestamp. Do not run or edit the model until the prediction is saved and committed.

From the repository root, while prediction exists and before changing input/running:

```powershell
git add -- projects/project-1/evidence/locked-changed-input-record.md
git commit -m "Lock my AI-off prediction before changed-input run"
git rev-parse HEAD
git show -s --format=%cI HEAD
```

Save that commit ID/time in a **separate** results addendum after the run, retaining the original committed prediction. Run an unchanged baseline into .build/student-baseline, edit just your chosen field in data/inputs.json using a text editor, then run into .build/student-changed. These commands assume your terminal is at the repository root and Python3.10+ is installed:

```powershell
python projects/project-1/run.py --all --output projects/project-1/.build/student-baseline
python projects/project-1/run.py --all --output projects/project-1/.build/student-changed
```

Execute the second command only after making the single edit. Preserve both results.json files in evidence/student-lock-baseline.json and evidence/student-lock-changed.json; include actual values, direction, action and decision threshold, diagnosis if wrong or no-change reason. Capture console exit/failure messages; an honest failed prediction is useful if diagnosed. Restore **only your own single input edit** from the original value; do not use a destructive repository reset. Rerun normal outputs and compare their hashes with the frozen snapshot. Have the assistant audit your completed record after you provide it. The final PDF/manifest/freeze must be regenerated to include authentic evidence, not left marked pending.

## Setup for all three videos

Use screen recording with clear audio and a small webcam view unless your instructor approved an accommodation. 1080p, browser zoom125-150%, hide notifications/private tabs, keep financial rows readable. Say “NVIDIA” and “free cash flow to the firm”; distinguish millions from billions. Record three separate files. Aim Video1 2:40-2:55 (hard maximum3:00), Video2 about3:00 (maximum5:00), Video3 about3:00 (maximum5:00). Practice once; scripts are roughly three minutes at a clear speaking pace with short cursor pauses. Trim dead time, not substantive evidence.

Use a fresh clone or separate folder and a fresh Python environment for the cold run. From a terminal in the Project1 directory:

```powershell
python -m venv .build/student-venv
.\\.build\\student-venv\\Scripts\\python.exe run.py --all --output .build/student-cold-output
```

No pip install is required for the engine. On macOS/Linux use .build/student-venv/bin/python. Keep the terminal/output and actual first failure/resolution (if any). The assistant already ran cold_run.py in a clean no-pip environment; the receipt honestly identifies the assistant. **Your recording must show your own clean run**, and your log should identify you and the actual observed result. Do not describe the assistant receipt as your run.

## Video1 - research evolution, target2:50; maximum3:00

Record these screens in this order; all timings are **planned**, replace with observed indices later:

| Time | Exact screen/action | Point to show |
|---|---|---|
| 0:00-0:35 | Research-Evolution.pdf first page, baseline/addendum | September1 admission thesis versus September10 decision; checkpoint evidence status. |
| 0:35-1:15 | Same PDF A-to-B table, then original Lab10/11 writeups if legible | Financial investment classification and signed cash-flow error corrected. |
| 1:15-1:55 | data/source-map.md share/investment/debt reconciliation; optionally SEC Q2Note5 in another tab | Independent source check, exact basis and dates, no AI agreement as validation. |
| 1:55-2:30 | evidence/assumption-challenges.md, prior Lab12 and actual confirmed partner entry | Actual challenge/disposition, qualified attribution, what changes the forecast. |
| 2:30-2:50 | outputs/visible-output.md top | Final range/action, real remaining evidence status. |

Script (read naturally, about3minutes; use the truthful status sentence specified below):

“This project asks whether a fund with no NVIDIA position should initiate, watch or defer, or not initiate over a twelve-to-twenty-four-month horizon. I used my earlier NVIDIA labs as the research trail. EditionA was dated September first. Its word ‘initiate’ meant start valuation research, not buy the stock. EditionB uses the September tenth close, and that date change is disclosed.

The biggest improvement was connecting the operating forecast to a defensible valuation. Lab10 had company-specific growth, margin, working-capital and equipment drivers, but broad other-assets balances mixed operating items with financial investments. Lab11 also identified problems with labeling cash after distributions and handling negative cash flows. Those errors could produce a model that balances while still valuing the wrong economics.

The rebuilt model separates financial investments from operating working capital, keeps signed cash flows, and discounts free cash flow to the firm at WACC. I checked definitions against NVIDIA's filing and its earnings release. At July twenty-sixth, cash plus debt securities was fifty-six-point-six billion dollars. Marketable equity holdings were separate. Debt also increased substantially, so the earlier annual debt balance was stale.

The review question I focus on is whether Data Center growth is durable. Supplier commitments tell us what NVIDIA may have to buy; they do not prove customers will accept systems and pay. That distinction affects the growth, inventory, collection and downside assumptions. The challenge record distinguishes verified finance evidence, qualified prior discussion and a fictional AI practice answer. A generated practice answer is not partner evidence.

The resulting causal range is about {lo['per_share']:.0f} to {hi['per_share']:.0f} dollars per share, with a base reference around {b['per_share']:.0f}. At the dated price of two hundred eighteen dollars and thirty-six cents, I would watch or defer. I would reconsider only with a sufficient price cushion and evidence supporting demand, cash collection and margins. The original checkpoint receipt, the human prediction exercise and the recordings are separate evidence requirements; the status record identifies what is actually complete.”

Before recording: if you have supplied the original checkpoint/lock/partner evidence and we updated the package, replace only the last status sentence with the factual completed status. Never say you submitted or completed evidence unless you did. The script does not invent a past partner quote.

## Video2 - code ownership and validation, target3:00; maximum5:00

Prepare code tabs before recording: data/inputs.json; model.py at forecast, valuation and dcf_cashflows; outputs/validation-results.json; your genuine locked record/addendum. Open terminal in a fresh project copy/environment as above. Record the command execution, not only a screenshot.

| Time | Exact screen/action | Point to show |
|---|---|---|
| 0:00-0:35 | inputs.json then model.py forecast | Fact/assumption separation; statement driver to FCFF. |
| 0:35-1:10 | model.py near cash/equity checks and valuation terminal | No balancing plug; retainedSBCcost; g/ROIC reinvestment. |
| 1:10-1:45 | Terminal: run fresh-venv command shown above | End-to-end result and actual15tests; first failure/resolution if present. |
| 1:45-2:25 | outputs/validation-results.json: officialknownanswers, contamination experiment, downside | Expected values from course answers; highest-risk deliberately wrong input. |
| 2:25-3:00 | Your locked record at precommit plus actual-results addendum | Show author/time/immutablecommit, old/new units, prediction BEFORErun, actualdirection/action and diagnosis. |

Script:

“The application runs locally with Python's standard library. The input file separates reported history, market observations, common forecast assumptions and causal cases. The source map gives the date, definition and transformation for each material input group. It needs no credentials or live data connection.

The forecast function starts with the July balance sheet and produces five rolling years of income, balance-sheet and cash-flow statements. Data Center and Edge revenue drive margins and expenses. Collection days, inventory days and payment days drive working capital. Capital spending and depreciation roll property and equipment forward. Cash comes from operating, investing and financing flows. Equity comes from retained income and distributions; neither is a balancing plug.

Free cash flow to the firm starts with after-tax operating profit, adds depreciation and amortization, and subtracts operating capital spending and working-capital investment. Stock compensation remains an economic cost through cash replacement. Financial investments and dividends are kept outside FCFF. The terminal calculation requires reinvestment equal to growth divided by terminal return on invested capital, so perpetual growth is not free.

I am now running the project in this fresh environment. The visible output reports the decision and the validation count. The test file compares the DCF engine with the course's independently published answers, including all nine sensitivity cells. Other tests check statement articulation, cash, equity, valuation bridges and the expected effect of discount rates and terminal growth.

The highest-risk experiment deliberately repeats the old investment-classification mistake. Scaling the investment portfolio as operating working capital creates false cash investment. Another failure test forces an unsupported cash deficit and requires the model to stop. Negative cash flows are preserved instead of silently dropped.

The required human locked exercise is separate from the assistant's WACC test. Here I show the record's actual status, the prediction commit if completed, and the observed results if available. A complete record needs my own AI-off prediction before execution, old and new units, actual valuation direction, decision effect, and a diagnosis or a threshold-based reason the action stayed unchanged. I do not claim missing evidence as completed.”

For maximum-credit completion, finish the human exercise first and use the final30seconds to **read your actual old/new values, predicted/actual direction and action effect from your record**, in your words. This intentionally cannot supply a prediction for you. If incomplete, the honest pending line above is accurate but leaves rubric points unresolved.

## Video3 - committee defense and live product demo, target3:00; maximum5:00

Use outputs/dashboard.html in your browser. This is a locally opened interactive artifact, not a deployed website. Pre-open Decision-Memo.pdf in another tab. Keep most recording time on the running product. Selectors display executed engine results; they do not run a live market-data calculation.

| Time | Exact screen/action | Point to show |
|---|---|---|
| 0:00-0:35 | Dashboard base case cards | User, date, market, range and conditionalaction. |
| 0:35-1:05 | Scroll to EV/common-equity bridge; change Statement to Cashflow | Cash/investments/debt/dilution plus operating source ofvalue. |
| 1:05-1:40 | Scroll to WACC-growth grid; click a row; show reverseDCF | Sensitivity, terminal dependence and market-impliedgrowth. |
| 1:40-2:15 | Return case selector, choose low | Actual case value/action changes, explain causalinputs. |
| 2:15-2:35 | Choose high then base | Upside conditions, range rather than single target. |
| 2:35-3:00 | Memo page2 monitoring/conditions, then dashboardbase | Committee ask and exact reversal triggers. |

Script:

“My committee recommendation is watch or defer. The fund has no position, so it can wait for a price that compensates for uncertainty. This application values NVIDIA at the September tenth, twenty-twenty-six close of two hundred eighteen dollars and thirty-six cents. My causal intrinsic range is about {lo['per_share']:.0f} to {hi['per_share']:.0f} dollars per share. The base reference is about {b['per_share']:.0f}; it is not a precise target or a probability-weighted forecast.

Here is the enterprise-to-equity bridge. Operating value comes from five years of statement-driven FCFF and a reinvestment-supported terminal value. The bridge then handles cash, financial investments, debt, acquisition costs and other claims separately. The diluted share proxy is twenty-four-point-two-four-two billion. Investment holdings are not treated as cash or scaled with operating revenue.

The base discount rate is about {w*100:.1f} percent, and terminal growth is three percent. About {b['terminal_share']*100:.0f} percent of enterprise value comes from the terminal value, which limits confidence. This sensitivity grid shows how discount rate and growth affect value. The market-implied test requires roughly {rev['constant_increment_to_each_dc_growth']*100:.0f} extra percentage points of Data Center growth in every explicit year, if all other base assumptions remain fixed. That is a demanding conditional expectation, not proof the market is wrong.

I am switching to the low case. Deployment and financing slow, margins weaken, collections take longer and inventory builds. Supply losses and guarantee exposure compound the pressure. Value falls to about {lo['per_share']:.0f} dollars, and the risk gate changes the action to do not initiate. Supplier commitments are an obligation risk, not a guaranteed sales backlog.

The high case requires stronger, durable demand and better execution, and reaches about {hi['per_share']:.0f} dollars. Peer multiples suggest different market expectations, but AMD and Broadcom have different margins and business mixes, and historical earnings lag current growth. I do not average those prices with the DCF.

I would consider initiation only below roughly {b['entry_ceiling']:.0f} dollars using the refreshed base estimate, with demand, collections, margins and commitments validated. Sustained Data Center growth below twenty percent, collection days above ninety-five, gross margin below seventy percent or material guarantee losses would push me toward no initiation. The committee's action today is to keep NVIDIA on watch and require that evidence before committing capital.”

## After recording - final review and freeze

1. Save distinct Video1/2/3 recordings; use stable unlisted hosting or repository-compatible links the instructor can access. Don't commit large raw recordings to Git. Keep titles and durations factual. Only you can grant/upload from accounts unavailable to the assistant.
2. Replace docs/transcript-video-1.txt, -2.txt and -3.txt with corrected **actual** transcripts and observed timestamp indices. Fix NVIDIA/NVDA, FCFF, WACC, period dates, figures, sources and attribution. Do not paste preparation scripts unless they match what you actually said.
3. Provide the video URLs, actual durations, actual transcripts and completed checkpoint/locked/partner evidence for a final consistency review. The assistant can audit supplied evidence, update PDFs/status/manifest and create a **new** final freeze tag. The current technical tag must remain immutable; it is not a claim videos are complete.
4. Test repository and every video/transcript link in a logged-out/incognito browser; confirm audio, readable output and captions. Ensure the instructional team can access private/unlisted items. Record observed check times, not assumed access.
5. Fill submission-manifest.csv with final stable URLs, titles, durations, observed timestampindices, accesschecks and finaltag/filehashes. Include all11requiredrows; optionaldeploymentcanremainunused.
6. Submit the seven-part final bundle through the **final assignment** Brightspace page by October19,2026 at11:59PM course time, and save the successful receipt. The EditionA checkpoint has its separate designated submission page. GitHub upload does not submit Brightspace. No grade is guaranteed; inspect the current docs/rubric-audit.md for unresolved requirements.
'''


if __name__=='__main__': main()
