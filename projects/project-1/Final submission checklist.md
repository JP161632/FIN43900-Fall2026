# NVIDIA Project 1 - final submission review

Reviewed October 19, 2026. **Technical checks pass; final submission is not yet verified complete.** Three video links and supplied transcripts are now included; durations pass. Material transcript/speech discrepancies and timestamp indices require closure; see docs/video-review.md. This review does not change the earlier frozen evidence or certify a rubric score.

## Upload videos and obtain transcripts

1. Sign in at https://studio.youtube.com. Select Create > Upload videos and select each recording. Use distinct titles: NVIDIA Project 1 - Video 1 Research Evolution; Video 2 Code and Validation; Video 3 Committee Decision.
2. Finish the details and choose Unlisted under Visibility, then Save. Copy each watch URL. Test playback in a signed-out/private browser window. Video 1 must be at most 3:00; Videos 2 and 3 at most 5:00 each.
3. When captions are available, open Studio > Subtitles > the video > the language. For automatic captions, choose Duplicate and edit. Correct finance terms, numbers, dates, units and attribution against the actual recording; Publish.
4. On the video watch page, expand the description and choose Show transcript. Copy the corrected text and timestamps into UTF-8 plain-text files named transcript-video-1.txt, transcript-video-2.txt and transcript-video-3.txt. Alternatively, the Studio caption editor offers Options > Download subtitles; retain the downloaded caption file as backup and prepare the required readable .txt transcript.
5. Replace the three status-marker files in docs/ with the actual transcripts. Captions may take time to appear. A preparation script is not evidence of what was actually said.

Official instructions: https://support.google.com/youtube/answer/57407 ; https://support.google.com/youtube/answer/2734705 ; https://support.google.com/youtube/answer/15930243 .

## Required final bundle

All paths below are relative to projects/project-1/.

| Submit or link | Current file/location | Closure needed |
|---|---|---|
| Research evolution, unchanged Edition A and Edition B | Research-Evolution.pdf | Recover original submitted Edition A PDF and first successful Brightspace checkpoint receipt; the preserved Markdown alone does not prove the checkpoint. |
| Accessible runnable repository and visible executed result | README.md; source/data/evidence; outputs/visible-output.md | Preserve source/dependencies and use a stable final repository URL. |
| Committee memo (maximum two pages) | Decision-Memo.pdf | Present, length checked. |
| Validation, AI-use record and complete locked-input evidence | Validation-and-AI-Use.pdf; evidence/locked-changed-input-record.md | Locked record remains incomplete; incorporate actual evidence or the instructor's documented replacement requirement. Do not relabel the assistant's past test as a prior human prediction. |
| Research-evolution video and corrected transcript | Video 1 URL; docs/transcript-video-1.txt | URL/duration/text supplied; observed index and speech/caption confirmation pending. |
| Code/validation video and corrected transcript | Video 2 URL; docs/transcript-video-2.txt | Same; verify the recording demonstrates an actual run and explains validation. |
| Committee video and corrected transcript | Video 3 URL; docs/transcript-video-3.txt | Same; verify the decision, range, conditions and reversal triggers. |
| Submission manifest | submission-manifest.csv | Six video/transcript entries populated; observed indices and full playback review pending. |

The videos may be linked rather than uploaded as large repository binaries. Recording-Charts.pdf, Student next steps.md and the Colab notebook are supporting aids, not substitutes for required deliverables. Submit the final bundle/links to the final Brightspace assignment, not the separate Edition A checkpoint. Save the final submission receipt. Due: October 19, 2026, 11:59 PM as stated in the assignment.

## Rubric review and remaining gaps

| Criterion | Evidence reviewed | Remaining completion risk |
|---|---|---|
| Problem definition, 45 | Explicit user, action, horizon, historical valuation date and conditional recommendation | Missing original checkpoint evidence weakens the Edition A/B boundary. |
| Data integrity, 45 | Source map, definitions, normalizations, dates, exclusions and preserved-file hashes | Historical assumptions remain disclosed judgments; no claim that tests prove forecasts. |
| Financial judgment, 60 | Five-year articulated statements, FCFF, WACC, terminal reinvestment, bridge, causal cases, sensitivity, reverse DCF and peer definitions | Unseen committee recording must agree with the model and state conditions. |
| Technical execution, 45 | Application rerun successfully; existing clean-environment receipt and usable visible output | Student recording and actual reproducibility demonstration not yet reviewed. |
| Validation, 75 | 15/15 tests pass on this review; frozen hashes and dashboard audit pass | Human locked-input evidence incomplete; real partner challenge attribution unconfirmed. Supply actual review or applicable instructor-approved alternative. |
| Communication, 30 | Required PDFs, two-page memo, recording charts/scripts and manifest structure | Links/text supplied; material numerical discrepancies and observed timestamp indices need closure. |

Commands executed in this review:

```powershell
.\.venv\Scripts\python.exe projects/project-1/submission_audit.py
.\.venv\Scripts\python.exe projects/project-1/run.py --all --output projects/project-1/.build/final-review-output
```

Observed: technical audit PASS; model PASS 15/15; base value $118.58 per share; WATCH / DEFER. The manifest now includes supplied video/transcript links; text review and observed index still need closure. GitHub submission/main had no newer commits than local HEAD when checked. No final-completion claim is justified until the missing evidence is incorporated, the PDFs/status/manifest are reconciled, a final immutable snapshot is made and actual access is checked. Preserve the earlier freeze; do not run a generator that resets newly supplied evidence to pending.
