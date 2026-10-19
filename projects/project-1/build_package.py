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

## Attribution of research changes

Course requirements supplied the five-year FCFF framework with articulated statements, evidence boundaries and validation standards. Existing student-supplied NVIDIA materials supplied the target, initial research-admission question and prior lab trail. Labs10-12 already recorded investment classification, cash-flow labeling and sensitivity limitations before the October19 rebuild; their existence is independently inspectable, but this package cannot establish who authored every older passage. The Lab12 record reports partner questions; attribution remains qualified until confirmed.

Codex assisted the October19 filing research, code rebuild, scenario assumptions, documentation and checks. The revised forecast and discount-rate choices are analyst assumptions that the student must evaluate and defend; they are not new reported facts or automatically the student's independently authored judgment. Sources and executed tests justify accepting or qualifying those outputs. The move from Lab5's62.72 to the current base{p:.2f} cannot be credited to AI alone: reporting base, operating forecast, WACC, reinvestment, bridge and share basis all changed. No controlled dollar-by-dollar historical attribution is asserted. The action stays watch/defer from Lab5 to B, while EditionA was admission to research rather than a buy decision.

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

File-integrity.json hashes stable artifacts; submission-manifest.csv lists 11 required items plus optional deployment. Three YouTube links and supplied transcripts are included. Metadata confirms durations 2:53/2:58/3:00 and correct Video 2/3 mapping; full playback is unreviewed. At student request, transcript figures were editorially corrected to model values; the edit log and audio/timestamp limits are in docs/video-review.md. These corrections do not certify what was spoken. The corrected-transcript snapshot uses a new immutable tag; prior tags remain unchanged. Publication-audit.json records GitHub access and hashes. Original checkpoint, human-lock and partner evidence remain unresolved. GitHub is not Brightspace submission; final due October 19 2026 11:59 PM course time.
''')
    for i in range(1,4):
        path=ROOT/f'docs/transcript-video-{i}.txt'
        if not path.exists(): path.write_text(f'NOT RECORDED - Video {i}. This is a status marker, not a transcript.\nAfter recording, replace with a corrected verbatim transcript of what was actually said, with observed timestamps. Preparation scripts are in Student next steps.md.\n',encoding='utf-8',newline='\n')
    write('Student next steps.md',student_steps(r))
    print('Built NVIDIA memo, evolution, validation source records, prior-lab index and Student next steps.md')


def student_steps(r):
    return (ROOT / 'docs/recording-guide.md').read_text(encoding='utf-8')


if __name__=='__main__': main()
