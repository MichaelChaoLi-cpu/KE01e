# Manuscript Revision Changes

Schema: `kila-revision-changes/v1`

## reviewer-2/comment-3

### part-01

- Location: Methods > Rainfall and Official Threshold Scenarios, paragraph beginning 'Moderate, Heavy, and Extreme rainfall...'
- Reason: Define the all-area 100% threshold case as a no-retention model baseline rather than a physical no-earthquake counterfactual.
- Kila decisions: KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:07:49Z
- Author: Mike Li
- Markup SHA-256 before: `9a5b2cc11405513e2b5ab0cfc2d0c2ee396e31a3dde22f285bbf7ff0414a2f2d`
- Markup SHA-256 after: `8ac98ca9d82c13169c772666088776c4bafb3cd2676b70bc5264e31cbdb2f43e`
- Revision IDs: `1`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120749422359.reviewer-2-comment-3.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Because the available municipality geometry does not distinguish the two official Yatsushiro subareas, the central municipality-wide analysis uses an analyst-defined midpoint of 0.75, bounded by separate 0.70 and 0.80 assignments; the midpoint is not an official Yatsushiro value.
~~~~

- After:

~~~~text
For the paired comparison, f = 1.00 is assigned throughout Kumamoto to disable threshold retention while holding rainfall, terrain, road, network, service, and simulation inputs fixed. This is a no-retention-adjustment model baseline, not a physical no-earthquake counterfactual. Because the available municipality geometry does not distinguish the two official Yatsushiro subareas, the central municipality-wide analysis uses an analyst-defined midpoint of 0.75, bounded by separate 0.70 and 0.80 assignments; the midpoint is not an official Yatsushiro value.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "For the paired comparison, f = 1.00 is assigned throughout Kumamoto to disable threshold retention while holding rainfall, terrain, road, network, service, and simulation inputs fixed. This is a no-retention-adjustment model baseline, not a physical no-earthquake counterfactual. "

## reviewer-2/comment-2

### part-01

- Location: Methods > Rainfall and Official Threshold Scenarios, Equation 4 explanation
- Reason: Report the quantitative compatibility test and retain Equation 4 only as a relative scenario index.
- Kila decisions: KILA-D-20260903-001, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:03Z
- Author: Mike Li
- Markup SHA-256 before: `8ac98ca9d82c13169c772666088776c4bafb3cd2676b70bc5264e31cbdb2f43e`
- Markup SHA-256 after: `67c6b0935770a9bf799f574cecabc28d222ee6a9c84235c81168c8df4ab0376d`
- Revision IDs: `2`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120804044709.reviewer-2-comment-2.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The analysis assigns equal weights of 0.25 to the 1, 3, 24, and 72 h windows.
~~~~

- After:

~~~~text
The analysis assigns equal weights of 0.25 to the 1, 3, 24, and 72 h windows. The equal-weight choice is a transparent central reference rather than an empirically optimized parameterization. Compatibility was evaluated against a JMA-type reconstruction based on the published tank equations and Level-4 grid curves for 2,438 eligible events. The pooled Spearman correlation was 0.862 (station-cluster bootstrap 95% CI, 0.842–0.884), and applying the official factors produced median and 95th-percentile absolute relative errors of 0.0022 and 0.0054 across 513,702 valid grid–rainfall cells. All prespecified compatibility criteria were met; Equation 4 is therefore retained as a relative scenario index and is not relabelled as the operational JMA indicator.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The equal-weight choice is a transparent central reference rather than an empirically optimized parameterization. Compatibility was evaluated against a JMA-type reconstruction based on the published tank equations and Level-4 grid curves for 2,438 eligible events. The pooled Spearman correlation was 0.862 (station-cluster bootstrap 95% CI, 0.842–0.884), and applying the official factors produced median and 95th-percentile absolute relative errors of 0.0022 and 0.0054 across 513,702 valid grid–rainfall cells. All prespecified compatibility criteria were met; Equation 4 is therefore retained as a relative scenario index and is not relabelled as the operational JMA indicator."

### part-02

- Location: Discussion > Compound-Hazard Interpretation, paragraph beginning 'We use threshold retention...'
- Reason: Bound the compatibility claim and distinguish robust road ordering from scenario-sensitive consequence magnitude.
- Kila decisions: KILA-D-20260903-001, KILA-D-20260903-002, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:09:04Z
- Author: Mike Li
- Markup SHA-256 before: `9253328055ed544d6d7849a44c4f94f9f48865cbbe23ca5a812a208c0b4a8915`
- Markup SHA-256 after: `abe3a86a53b116db4dcbd9ed94ed586256ac3b4f549bd1ef2b07fac5191eb22f`
- Revision IDs: `6`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120904216662.reviewer-2-comment-2.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
It therefore does not measure continuous shaking, estimate a location-specific change in soil strength, or identify a causal threshold shift.
~~~~

- After:

~~~~text
The quantitative comparison with the JMA-type reconstruction supports applying the official factors to Equation 4 for directional scenario screening in the present event sample, but it does not turn X or H into an operational warning indicator. Across the tested parameterizations, road-priority order is more stable than absolute isolation estimates; consequence magnitudes are therefore treated as scenario-sensitive. It therefore does not measure continuous shaking, estimate a location-specific change in soil strength, or identify a causal threshold shift.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "The quantitative comparison with the JMA-type reconstruction supports applying the official factors to Equation 4 for directional scenario screening in the present event sample, but it does not turn X or H into an operational warning indicator. Across the tested parameterizations, road-priority order is more stable than absolute isolation estimates; consequence magnitudes are therefore treated as scenario-sensitive. "

## reviewer-2/comment-4

### part-01

- Location: Methods > Rainfall and Official Threshold Scenarios, Equation 6 explanation
- Reason: State the tested gamma range and identify gamma = 1.00 as a transparent reference rather than an estimated local coefficient.
- Kila decisions: KILA-D-20260903-002, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:18Z
- Author: Mike Li
- Markup SHA-256 before: `67c6b0935770a9bf799f574cecabc28d222ee6a9c84235c81168c8df4ab0376d`
- Markup SHA-256 after: `0f1705cf2fc185ab4b0f1d3a06ecbf29eee19fcfb99f0d827b753dc667191aca`
- Revision IDs: `3`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120819002048.reviewer-2-comment-4.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The logarithm represents rainfall intensity and threshold retention as multiplicative changes while reducing saturation at high loading.
~~~~

- After:

~~~~text
Sensitivity analyses use γ = 0.50 and 2.00 around this central value under five rainfall-window weighting schemes; γ = 1.00 is therefore a declared transparent reference rather than an estimated local coefficient. The logarithm represents rainfall intensity and threshold retention as multiplicative changes while reducing saturation at high loading.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "Sensitivity analyses use γ = 0.50 and 2.00 around this central value under five rainfall-window weighting schemes; γ = 1.00 is therefore a declared transparent reference rather than an estimated local coefficient. "

### part-02

- Location: Methods > Robustness, paragraph beginning 'Compound-hazard conclusions...'
- Reason: Align the robustness description with the implemented baseline, rainfall-window-weight, and gamma sensitivity analyses.
- Kila decisions: KILA-D-20260903-002, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:35Z
- Author: Mike Li
- Markup SHA-256 before: `0f1705cf2fc185ab4b0f1d3a06ecbf29eee19fcfb99f0d827b753dc667191aca`
- Markup SHA-256 after: `404c27cd64d1c51b49250a9d08e1694c0ea1a588b40705d3c633f7a6dd99416f`
- Revision IDs: `4`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120835664094.reviewer-2-comment-4.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The implemented checks vary rainfall temporal support, the unresolved Yatsushiro threshold assignment, external-road targets, closure mappings, simulation size, intervention costs and effects, and ranking comparators.
~~~~

- After:

~~~~text
The implemented checks vary rainfall temporal support, five rainfall-window weighting schemes, γ = 0.50, 1.00, and 2.00, the all-area f = 1.00 baseline, the unresolved Yatsushiro threshold assignment, external-road targets, closure mappings, simulation size, intervention costs and effects, and ranking comparators.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: ", five rainfall-window weighting schemes, γ = 0.50, 1.00, and 2.00, the all-area f = 1.00 baseline"

### part-03

- Location: Results > Earthquake-Adjusted Rainfall and Slope Disruption, paragraph beginning 'The declared retention settings...'
- Reason: Summarize that threshold retention and rainfall parameters affect consequence magnitude more than spatial road ordering and direct readers to Appendix Table B5.
- Kila decisions: KILA-D-20260903-002, KILA-D-20260903-003, KILA-D-20260903-005, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:50Z
- Author: Mike Li
- Markup SHA-256 before: `404c27cd64d1c51b49250a9d08e1694c0ea1a588b40705d3c633f7a6dd99416f`
- Markup SHA-256 after: `9253328055ed544d6d7849a44c4f94f9f48865cbbe23ca5a812a208c0b4a8915`
- Revision IDs: `5`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120850465996.reviewer-2-comment-4.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The rainfall dimension therefore supports magnitude scaling and broader consequence scenarios, not spatial reprioritization of roads.
~~~~

- After:

~~~~text
The rainfall dimension therefore supports magnitude scaling and broader consequence scenarios, not spatial reprioritization of roads. The paired all-area f = 1.00 comparison and the 15-combination rainfall-parameter sensitivity are reported in Appendix Table B5. Official retention changes downstream consequence magnitude more strongly than road ordering, while alternative window weights and γ values leave road rankings stable but produce wider variation in expected isolation.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The paired all-area f = 1.00 comparison and the 15-combination rainfall-parameter sensitivity are reported in Appendix Table B5. Official retention changes downstream consequence magnitude more strongly than road ordering, while alternative window weights and γ values leave road rankings stable but produce wider variation in expected isolation."

