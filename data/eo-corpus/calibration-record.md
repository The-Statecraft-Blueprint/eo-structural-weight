# EO Structural Weight Score — Calibration Record
*Appendix A to eo-structural-weight-scoring-scheme.md v1.0*
*Produced before committing the scoring scheme to GitHub.*
*Purpose: confirm the scheme produces sensible rankings before pre-registration is finalized.*

---

## Method

Ten executive orders were selected across five tiers with expected score ranges stated *before* scoring. Flags were applied against the primary source text from the American Presidency Project corpus. Any discrepancy between expected and actual score is noted as a calibration finding. No adjustment to the scoring scheme is made on the basis of these findings unless a flag definition is shown to be operationally broken — a prediction being wrong is a finding, not a defect.

**Status mapping:** NOT APPLICABLE (excluded) | ABSENT = 0 | PRESENT = 1 | CRITICAL = 2

**Normalized score** = raw points ÷ (2 × applicable flag count)

---

## Tier 1 — Expected: ~0%

### EO-11069 (November 28, 1962 — Kennedy)
*Amending EO-11017 to add Secretary of Commerce to the Recreation Advisory Council*

56 words. Single sentence adding one cabinet member to an existing advisory council.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | NOT APPLICABLE | — | No decision authority created |
| 2 | Accountability Gaps | NOT APPLICABLE | — | No policy implementation |
| 3 | Bundling | ABSENT | 0 | Single provision, single purpose |
| 4 | Vague Enforcement | NOT APPLICABLE | — | No enforcement mechanism |
| 5 | Perverse Incentives | NOT APPLICABLE | — | No incentive structure |
| 6 | Sunset Provisions | NOT APPLICABLE | — | Inherits from parent EO 11017 |
| 7 | Preemption of Oversight | ABSENT | 0 | Amends rather than supersedes; parent EO preserved |
| 8 | Third-Party Incentive Gaps | NOT APPLICABLE | — | No compliance context |
| 9 | Second/Third-Order Effects | ABSENT | 0 | Ministerial addition; no systemic implications |
| 10 | Inter-Agency Cannibalization | ABSENT | 0 | Adds Commerce to existing council; no jurisdictional conflict |
| 11 | Exemptions Architecture | NOT APPLICABLE | — | No coverage scope |

**Applicable count:** 4 | **Raw:** 0 | **Max:** 8 | **Score: 0.00 (0%)**
**Expected:** ~0% ✓

---

### EO-12717 (June 18, 1990 — George H.W. Bush)
*Revoking EO-12691 (Points of Light Initiative Foundation Advisory Committee)*

60 words. Revokes a prior EO on the grounds that the committee has completed its tasks.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | NOT APPLICABLE | — | Termination order; removes rather than concentrates authority |
| 2 | Accountability Gaps | NOT APPLICABLE | — | Termination; no ongoing accountability question |
| 3 | Bundling | ABSENT | 0 | Single revocation action |
| 4 | Vague Enforcement | NOT APPLICABLE | — | No enforcement |
| 5 | Perverse Incentives | NOT APPLICABLE | — | No incentive structure |
| 6 | Sunset Provisions | ABSENT | 0 | This EO *is* the termination mechanism; parent EO is closed |
| 7 | Preemption of Oversight | ABSENT | 0 | Clean revocation of completed committee; no oversight removed |
| 8 | Third-Party Incentive Gaps | NOT APPLICABLE | — | No compliance context |
| 9 | Second/Third-Order Effects | ABSENT | 0 | Natural completion; no downstream implications |
| 10 | Inter-Agency Cannibalization | NOT APPLICABLE | — | No agency mandates involved |
| 11 | Exemptions Architecture | NOT APPLICABLE | — | No coverage scope |

**Applicable count:** 4 | **Raw:** 0 | **Max:** 8 | **Score: 0.00 (0%)**
**Expected:** ~0% ✓

*Calibration note:* EO-12717 scores ABSENT on Sunset because it *provides* the termination the parent EO (12691) lacked. If scoring EO-12691, the Sunset flag would fire PRESENT.

---

## Tier 2 — Expected: 15–30%

### EO-9981 (July 26, 1948 — Truman)
*Establishing the President's Committee on Equality of Treatment and Opportunity in the Armed Services*

414 words. Declares policy of equality in the armed services; creates a seven-member advisory committee.

**This is the critical calibration test.** An order of enormous historical significance. The score must come in substantially below EO-9066 to confirm the scheme is measuring structural architecture rather than importance.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | PRESENT | 1 | Implementation authority rests entirely with service secretaries; committee has advisory power only — cannot compel. "The Committee... shall make such recommendations to the President and to said Secretaries" (Sec. 3). |
| 2 | Accountability Gaps | PRESENT | 1 | No mechanism for consequence if service secretaries slow implementation. History confirms: Truman had to push military leadership for years after signing. No timeline, no compliance standard. |
| 3 | Bundling | ABSENT | 0 | Single coherent purpose throughout |
| 4 | Vague Enforcement | PRESENT | 1 | "As rapidly as possible, having due regard to the time required to effectuate any necessary changes without impairing efficiency or morale" (Sec. 1). No metric, no timeline, no definition of equality achieved. "Efficiency or morale" is an escape clause. |
| 5 | Perverse Incentives | PRESENT | 1 | Service personnel who resist desegregation create "morale impairment" — which becomes justification for slowing implementation under the EO's own language. Implementers have institutional interest in the status quo. |
| 6 | Sunset Provisions | ABSENT | 0 | Policy of equality is appropriately permanent. Committee has explicit presidential termination mechanism (Sec. 6). |
| 7 | Preemption of Oversight | NOT APPLICABLE | — | Does not preempt existing oversight; creates new mechanism |
| 8 | Third-Party Incentive Gaps | PRESENT | 1 | No mechanism for affected service members to compel implementation. Courts not given role. Citizens have no recourse under this EO. |
| 9 | Second/Third-Order Effects | ABSENT | 0 | Downstream effects are positive; EO text structure creates no harmful second-order implications |
| 10 | Inter-Agency Cannibalization | ABSENT | 0 | Committee supplements rather than conflicts with existing mandates |
| 11 | Exemptions Architecture | ABSENT | 0 | No exemptions |

**Applicable count:** 10 | **Raw:** 5 | **Max:** 20 | **Score: 0.25 (25%)**
**Expected:** 15–30% ✓

*Calibration finding — key result:* EO-9981 scores 25%. One of the most consequential civil rights actions in American history scores in the low range. This is the correct result. The EO declared a transformative policy using architecturally modest machinery — advisory committee, aspirational timeline, no enforcement mechanism. The score measures what the text actually deploys, not the moral weight of what it accomplished.

---

### EO-10924 (March 1, 1961 — Kennedy)
*Establishment and Administration of the Peace Corps in the Department of State*

316 words. Creates the Peace Corps within State Department; delegates functions to Director.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | PRESENT | 1 | "The Secretary of State shall delegate... such of the functions... as the Secretary shall deem necessary" (Sec. 2(b)) — open-ended delegation with no defined scope limits. Standard for subordinate agency creation but still unbounded. |
| 2 | Accountability Gaps | ABSENT | 0 | Clear accountability chain: Director → Secretary of State → President |
| 3 | Bundling | ABSENT | 0 | Single purpose instrument |
| 4 | Vague Enforcement | NOT APPLICABLE | — | Organizational EO; no regulatory enforcement context |
| 5 | Perverse Incentives | ABSENT | 0 | Incentives aligned with mission |
| 6 | Sunset Provisions | PRESENT | 1 | No review mechanism, no expiration. Peace Corps continues indefinitely. (Superseded quickly by the Peace Corps Act of 1961, but this EO contains no termination provision.) |
| 7 | Preemption of Oversight | ABSENT | 0 | Section 4 explicitly preserves EO 10893 |
| 8 | Third-Party Incentive Gaps | NOT APPLICABLE | — | No regulatory compliance context |
| 9 | Second/Third-Order Effects | ABSENT | 0 | Standard organizational creation |
| 10 | Inter-Agency Cannibalization | ABSENT | 0 | New function, no mandate conflict |
| 11 | Exemptions Architecture | NOT APPLICABLE | — | No coverage scope |

**Applicable count:** 8 | **Raw:** 2 | **Max:** 16 | **Score: 0.125 (12.5%)**
**Expected:** 15–30% — *prediction slightly high*

*Calibration finding:* EO-10924 scores 12.5% against a predicted 15–30%. The EO is architecturally leaner than assumed — four-section instrument, clear hierarchy, saves existing authorities. The main weaknesses are the open-ended delegation scope and absence of a sunset, neither of which fires above PRESENT. The prediction's lower bound was close; the actual score came in just below it. No scheme adjustment warranted — the prediction was marginally off, not the scoring.

---

## Tier 3 — Expected: 35–55%

### EO-14412 (June 22, 2026 — Trump II)
*Securing the Nation Against Advanced Cryptographic Attacks*

1,458 words. Federal transition to post-quantum cryptography with defined deadlines, distributed agency roles, and contractor requirements.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | ABSENT | 0 | Authority distributed: OMB coordinates civilian, NSA handles National Security Systems, CISA provides guidance, FAR Council handles procurement. No single actor controls the outcome. |
| 2 | Accountability Gaps | ABSENT | 0 | NSA Director reports annually to President on National Security Systems (Sec. 5(c)). OMB must issue guidance within 90 days. Specific deadlines assigned per agency. |
| 3 | Bundling | ABSENT | 0 | Coherent single purpose throughout |
| 4 | Vague Enforcement | PRESENT | 1 | Section 6(c)/(d) require FAR Council to publish proposed rules requiring "covered contractors" to comply — but "covered contractors" is undefined in this EO. Compliance standard won't exist until FAR rules are finalized. December 31, 2030 deadline exists without a defined obligated party. |
| 5 | Perverse Incentives | ABSENT | 0 | Agencies have genuine security interest in implementing PQC |
| 6 | Sunset Provisions | ABSENT | 0 | The 2030/2031 transition deadlines create a natural completion framework. "Annually thereafter until PQC migration is complete" implies a defined endpoint. |
| 7 | Preemption of Oversight | ABSENT | 0 | Does not preempt existing oversight; adds to it |
| 8 | Third-Party Incentive Gaps | PRESENT | 1 | Critical infrastructure transition (Sec. 5(a)): SRMAs "shall work with... CISA to assist critical infrastructure owners and operators in *developing their PQC migration plans*." No binding obligation for private critical infrastructure owners. Power grids, water systems, financial infrastructure have no legal compliance requirement from this EO. Voluntary for privately-owned infrastructure. |
| 9 | Second/Third-Order Effects | ABSENT | 0 | Positive second-order security effects; no harmful downstream architectural implications |
| 10 | Inter-Agency Cannibalization | ABSENT | 0 | Roles clearly differentiated: NIST sets standards, CISA coordinates, NSA handles NSS, OMB coordinates civilian agencies |
| 11 | Exemptions Architecture | PRESENT | 1 | National Security Systems excluded from civilian transition requirements (Sec. 4(b)(i)). NSA handles separately with annual reporting. Two-track system is reasonable but creates exemption that covers the most sensitive systems. |

**Applicable count:** 11 | **Raw:** 3 | **Max:** 22 | **Score: 0.136 (13.6%)**
**Expected:** 35–55% — *prediction significantly high*

*Calibration finding — notable result:* EO-14412 scores 13.6% against a predicted 35–55%. This is the largest prediction miss in the calibration set, and it's a genuine finding about what the scheme measures. The EO is well-architected: clear deadlines, distributed authority, defined agency roles, preserved oversight. The main structural weaknesses are the undefined contractor population and the voluntary status of private critical infrastructure — real gaps, but neither rises to CRITICAL. The prediction assumed technical complexity would translate to structural weight. It doesn't. A technically complex EO with clean architecture scores low. This is what the scheme is supposed to do.

---

### EO-12291 (February 17, 1981 — Reagan)
*Federal Regulation*

3,106 words. Establishes OMB/OIRA regulatory review; requires cost-benefit analysis for major rules.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | CRITICAL | 2 | OMB Director can designate any rule as "major" (triggering full RIA), waive requirements for any major rule (Sec. 6(a)(4)), delay publication of any proposed rule, and require agencies to obtain additional data. "Subject to the direction of the Task Force" is nominal political oversight with no external check. The Director's waiver authority in Sec. 6(a)(4) is essentially unconstrained. Section 9 explicitly forecloses judicial review. |
| 2 | Accountability Gaps | PRESENT | 1 | If OMB is blocking rules for political rather than cost-benefit reasons, no external accountability mechanism exists. Task Force reviews Director decisions but is itself a political body. Sec. 9 bars judicial review of Director determinations. |
| 3 | Bundling | ABSENT | 0 | Single coherent purpose (regulatory reform) |
| 4 | Vague Enforcement | PRESENT | 1 | "Maximize the net benefits to society" (Sec. 2(c)) and "maximize the aggregate net benefits" (Sec. 2(e)) provide no defined methodology. What constitutes a "benefit"? Who decides? The RIA process specifies inputs but the ultimate standard is inherently subjective. |
| 5 | Perverse Incentives | PRESENT | 1 | Agencies are incentivized to game RIA methodology to produce favorable cost-benefit ratios. Industries with concentrated costs have strong incentive to lobby OMB rather than engage rulemaking. Sec. 6(a)(4) waiver authority creates a political pressure valve. |
| 6 | Sunset Provisions | PRESENT | 1 | No review mechanism; no expiration. EO 12291 ran for 12 years until Clinton's EO 12866 (1993). |
| 7 | Preemption of Oversight | PRESENT | 1 | Establishes OMB review before notice-and-comment publication — inserting a political review layer not required by APA. OMB review phase is not subject to public participation. Revokes prior regulatory review EOs (12044, 12174). |
| 8 | Third-Party Incentive Gaps | PRESENT | 1 | Affected parties have no formal standing in OMB review phase. Sec. 3(h) requires public availability of RIAs but no comment mechanism exists for the OMB review itself. The APA participation rights are effectively bypassed during this pre-publication phase. |
| 9 | Second/Third-Order Effects | CRITICAL | 2 | EO 12291 fundamentally restructured the regulatory state. By inserting a political cost-benefit veto before publication, it systematically disadvantaged regulations where benefits are diffuse and hard to monetize (health, safety, environment, civil rights) relative to those where costs are concentrated and quantifiable. This structural bias persisted in every subsequent regulatory review framework. The OIRA review system created in 1981 is still the operative model today. |
| 10 | Inter-Agency Cannibalization | PRESENT | 1 | Inserts OMB into a pre-publication role that had belonged to agencies and their statutory oversight structures. Creates tension between OMB's cost-benefit mandate and agencies' statutory mandates (e.g., agency required by statute to protect worker health must now satisfy OMB cost-benefit review). |
| 11 | Exemptions Architecture | PRESENT | 1 | Section 8(b): Director "may... exempt any class or category of regulations from any or all requirements of this Order" — essentially unlimited discretion to grant exemptions. Emergency rule exemption (Sec. 8(a)(1)) is legitimate; the blanket Director waiver authority is not bounded. |

**Applicable count:** 11 | **Raw:** 12 | **Max:** 22 | **Score: 0.545 (54.5%)**
**Expected:** 35–55% ✓ (at upper bound)

---

## Tier 4 — Expected: 60–75%

### EO-13228 (October 8, 2001 — George W. Bush)
*Establishing the Office of Homeland Security and the Homeland Security Council*

2,842 words. Creates OHS within EOP; designates Assistant to the President for Homeland Security as lead coordinator for domestic terrorist response.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | CRITICAL | 2 | APHS (White House staff, no Senate confirmation, no congressional accountability) designated as "the individual primarily responsible for coordinating the domestic response efforts of all departments and agencies" in terrorist events (Sec. 3(g)). Receives Top Secret classification authority (Sec. 6). No statutory basis. |
| 2 | Accountability Gaps | CRITICAL | 2 | OHS is within EOP with no IG, no independent audit, no congressional testimony obligation. When coordination fails, responsibility is diffuse across all coordinating agencies with no clear locus. The 9/11 Commission's findings later confirmed this accountability gap was real and operationally damaging. |
| 3 | Bundling | ABSENT | 0 | Single mission: coordinate homeland security |
| 4 | Vague Enforcement | PRESENT | 1 | "Coordinate" is the operative verb throughout with no definition of what adequate coordination requires, no standard for coordination failure, no enforcement mechanism if agencies don't cooperate. "Executive departments and agencies shall... make available to the Office all information" (Sec. 3(b)(ii)) — but no consequence for non-compliance. |
| 5 | Perverse Incentives | PRESENT | 1 | White House proximity creates incentive for agencies to route security decisions through political channel rather than technical interagency processes, biasing operational decisions toward political considerations. Agencies defer to APHS to avoid political friction. |
| 6 | Sunset Provisions | PRESENT | 1 | No sunset, no review mechanism. OHS was eventually replaced by DHS (legislation, 2002) but not through any process envisioned by this EO. |
| 7 | Preemption of Oversight | PRESENT | 1 | Sec. 9 amends EO 12656 to shift emergency planning responsibility from NSC processes to HSC, sidelining decades of NSC-developed oversight mechanisms. Sec. 3(l) budget certification role inserts APHS into agency budget processes. |
| 8 | Third-Party Incentive Gaps | PRESENT | 1 | Sec. 3(j): state/local participation is by "encourage and invite" — purely aspirational. No mechanism for state/local governments or private sector to enforce coordination standards or seek remedy for federal coordination failure. |
| 9 | Second/Third-Order Effects | CRITICAL | 2 | Established precedent for White House-based coordination without statutory authority for major national security functions. Classification authority delegation to APHS (Sec. 6) set precedent for concentrating classification power in White House. The OHS's coordination failures directly shaped the DHS legislation that followed. |
| 10 | Inter-Agency Cannibalization | CRITICAL | 2 | OHS given coordination authority over DOD, DOJ, FBI, CIA, FEMA, State, Treasury, HHS, Transportation — all with existing statutory mandates. Creates parallel structure explicitly overlapping with NSC (Sec. 9) and FEMA's emergency role. Sec. 7's "this order does not alter existing authorities" is contradicted by Sec. 3(g)'s designation of APHS as "primarily responsible" for domestic response coordination. |
| 11 | Exemptions Architecture | NOT APPLICABLE | — | Organizational/coordination EO; no coverage population or exemption structure |

**Applicable count:** 10 | **Raw:** 13 | **Max:** 20 | **Score: 0.65 (65%)**
**Expected:** 60–75% ✓

---

### EO-13769 (January 27, 2017 — Trump I)
*Protecting the Nation From Foreign Terrorist Entry Into the United States*

2,883 words. 90-day entry suspension from seven countries; 120-day refugee program suspension; indefinite Syria refugee suspension.

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | CRITICAL | 2 | Syria refugee suspension: "until such time as I have determined that sufficient changes have been made" (Sec. 5(c)) — president alone decides. 50,000 refugee cap: "until such time as I determine that additional admissions would be in the national interest" (Sec. 5(d)). Case-by-case waivers: "when in the national interest" (Sec. 3(g)) — purely subjective. |
| 2 | Accountability Gaps | CRITICAL | 2 | Waiver denials have no defined criteria, no appeal mechanism, no record requirement. Courts found the waiver process effectively illusory. Who is responsible for arbitrary denials? No defined locus of accountability in the EO framework. |
| 3 | Bundling | PRESENT | 1 | Bundles: country entry suspension (INA 212(f)), refugee suspension (USRAP statute), Syria indefinite suspension, visa interview program suspension, new screening standards development, biometric tracking acceleration, visa reciprocity review, religious minority prioritization. Distinct legal mechanisms on different statutory bases bundled into one binary instrument. |
| 4 | Vague Enforcement | CRITICAL | 2 | Waiver standard: "when in the national interest" (Sec. 3(g)) — no criteria. "In their discretion" (Sec. 5(e)) — subjective. Referenced countries are in "section 217(a)(12) of the INA" without listing them — list is implicit in another statute. Courts consistently found enforcement standards unconstitutionally vague. |
| 5 | Perverse Incentives | PRESENT | 1 | Consular officers face career risk for granting waivers in the politically charged environment this EO created, but face no risk for denying them. Creates systematic over-denial incentive. |
| 6 | Sunset Provisions | PRESENT | 1 | 90-day and 120-day suspensions have time limits (positive). Syria suspension (Sec. 5(c)) and refugee cap (Sec. 5(d)) have no termination mechanism or standards. |
| 7 | Preemption of Oversight | PRESENT | 1 | Sec. 8 immediately suspends Visa Interview Waiver Program (which had its own review process). Sec. 6 directs reconsideration of existing terrorism-grounds exercises — potentially removing existing protections. |
| 8 | Third-Party Incentive Gaps | PRESENT | 1 | Applicants have no standing to challenge denials. No formal mechanism for legal organizations, employers, or family members to participate in waiver determinations. |
| 9 | Second/Third-Order Effects | CRITICAL | 2 | Established precedent for using INA 212(f) for sweeping categorical bans rather than case-by-case determinations. Hawaii v. Trump (SCOTUS 2018) shaped all subsequent presidential immigration authority. Religious minority prioritization (Sec. 5(b)) set precedent for religiously-differentiated refugee policy. The immediate nationwide confusion and airport detentions revealed the absence of implementation coordination. |
| 10 | Inter-Agency Cannibalization | PRESENT | 1 | Sec. 4 uniform screening standards create new cross-agency authority without clearly defining jurisdictional lines among State, DHS, DNI, FBI. |
| 11 | Exemptions Architecture | CRITICAL | 2 | Waiver criteria so open-ended (Sec. 3(g), 5(e)) that relief becomes entirely discretionary with no standards, no appeal, no accountability. Simultaneously too narrow (excluding entire country populations) and too vague (providing no real relief mechanism). Courts found waiver process inadequate. By December 2017 the third version (PP 9645) had to add defined waiver criteria to survive judicial review — confirming this EO's exemptions were structurally broken. |

**Applicable count:** 11 | **Raw:** 16 | **Max:** 22 | **Score: 0.727 (72.7%)**
**Expected:** 60–75% ✓ (near upper bound)

---

## Tier 5 — Expected: 80%+

### EO-9066 (February 19, 1942 — Roosevelt)
*Authorizing the Secretary of War to Prescribe Military Areas*

531 words. Grants Secretary of War and military commanders authority to designate exclusion zones and exclude "any or all persons."

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | CRITICAL | 2 | "Whatever restrictions the Secretary of War or the appropriate Military Commander may impose in his discretion" — unconstrained authority. No defined scope, no defined population, no external check. Supersedes AG authority (Sec. 3). |
| 2 | Accountability Gaps | CRITICAL | 2 | No remedy mechanism, no appeal process, no oversight body. Supersession of AG authority (Sec. 3) removes even limited civil rights protection. When property is seized and fundamental rights violated, no accountability path exists in this EO. |
| 3 | Bundling | ABSENT | 0 | Single (terrible) purpose |
| 4 | Vague Enforcement | CRITICAL | 2 | "Any or all persons" — zero definition of who is subject. "Such restrictions... may impose in his discretion" — completely open scope. "Whenever he or any designated Commander deems such actions necessary or desirable" — purely subjective trigger with no standard. |
| 5 | Perverse Incentives | CRITICAL | 2 | Military commanders have no downside for broader exclusion, potential upside (political cover, resources) for wider application. "As may be necessary, in the judgement of the Secretary of War" makes the Secretary's judgment the only check, and wartime creates pressure toward more restriction. |
| 6 | Sunset Provisions | PRESENT | 1 | No sunset; continued until revoked by EO 9742 (1946). |
| 7 | Preemption of Oversight | CRITICAL | 2 | Explicitly supersedes AG authority under December 1941 Proclamations (Sec. 3). Directs all federal agencies to cooperate. Creates military exclusion zones exempt from normal civil and judicial oversight. |
| 8 | Third-Party Incentive Gaps | CRITICAL | 2 | No judicial review pathway, no advocacy mechanism, no congressional oversight created. Military determinations are unchallengeable under this EO's framework. Korematsu v. United States (1944) confirmed courts would not review military necessity determinations. |
| 9 | Second/Third-Order Effects | CRITICAL | 2 | Established precedent for mass deprivation of constitutional rights of citizens on ethnic basis under emergency claims. Created the legal framework for WRA and camp system holding 120,000+ people. As precedent, available for subsequent invocations until formally repudiated by Congress (Civil Liberties Act, 1988). |
| 10 | Inter-Agency Cannibalization | CRITICAL | 2 | Supersedes AG's operational authority in designated areas. Transfers civil law enforcement to military. Directs all federal agencies to subordinate their functions to military commanders in exclusion zones. |
| 11 | Exemptions Architecture | ABSENT | 0 | No exemptions exist — the flag asks whether exemptions undermine the stated purpose. Here there are no exemptions, and the EO's stated purpose is served by their absence. The human catastrophe is captured by other flags (Power Concentration, Vague Enforcement, Accountability Gaps). |

**Applicable count:** 11 | **Raw:** 17 | **Max:** 22 | **Score: 0.773 (77.3%)**
**Expected:** 80%+ — *prediction slightly high*

*Calibration finding:* EO-9066 scores 77.3% against a predicted 80%+. The EO is below the Tier 5 threshold because Bundling (ABSENT) and Exemptions Architecture (ABSENT) don't fire — the EO is single-purpose and contains no exemptions. These are correct technical calls. The prediction overstated the score slightly. Crucially, EO-9066 scores *lower* than EO-14257, which is counterintuitive on historical importance grounds but correct on structural-machinery grounds: EO-14257 deploys more complex structural apparatus (more flags firing at CRITICAL) than EO-9066's brutal simplicity.

---

### EO-14257 (April 2, 2025 — Trump II)
*Regulating Imports With a Reciprocal Tariff*

17,734 words (policy sections: ~4,000 words; remainder is tariff rate annexes). Declares national emergency over trade deficits; imposes 10% universal tariff with country-specific rates.

*Note: Scored from policy sections only (through Sec. 7). Annexes contain rate tables, not structural provisions.*

| # | Flag | Status | Pts | Justification |
|---|------|--------|-----|---------------|
| 1 | Power Concentration | CRITICAL | 2 | Emergency termination: "until such time as I determine that the underlying conditions described above are satisfied, resolved, or mitigated" (Sec. 2) — president alone decides. Modification: Sec. 4 grants president unilateral authority to increase, decrease, or expand scope with no external trigger or standard. Sec. 5 delegates "all powers granted to the President by IEEPA" to USTR and Commerce. Tariff-setting authority belongs to Congress (Art. I, Sec. 8) — confirmed by SCOTUS in *Learning Resources v. Trump* (Feb. 2026). |
| 2 | Accountability Gaps | CRITICAL | 2 | No metric for what resolves the trade deficit emergency. "Satisfied, resolved, or mitigated" undefined. Congressional reporting (Sec. 6) required but not binding — Congress cannot compel termination except by legislation. Affected importers and businesses have no administrative appeal mechanism under this EO. |
| 3 | Bundling | PRESENT | 1 | Bundles: universal 10% tariff, country-specific rates (Annex I), product exemptions (Annex II), de minimis rules, foreign trade zone treatment, U.S. content calculation rules, termination of prior presidential trade actions (Sec. 3(l)). Distinct mechanisms, though all in service of coherent purpose. |
| 4 | Vague Enforcement | CRITICAL | 2 | "Satisfied, resolved, or mitigated" (Sec. 2): undefined. "Significant steps to remedy non-reciprocal trade arrangements" (Sec. 4(c)): undefined. "Align sufficiently with the United States on economic and national security matters" (Sec. 4(c)): undefined. "Continue to worsen" (Sec. 4(d)): no threshold defined. Emergency trigger itself ("large and persistent annual U.S. goods trade deficits") has no defined resolution standard. |
| 5 | Perverse Incentives | CRITICAL | 2 | **Zombie Emergency Trap sub-flag fires.** Termination criteria purely presidential (Sec. 2). Tariffs generate revenue ($166B collected before SCOTUS ruling); the "emergency" framework provides ongoing legal authority; administration has institutional incentive to maintain the declared emergency. Sec. 4(a): if action is "not effective in resolving the emergency," the remedy is *more* tariffs — no resolution path requires Congress or terminates the emergency. |
| 6 | Sunset Provisions | CRITICAL | 2 | No sunset, no review mechanism. Termination is purely presidential discretion. SCOTUS had to strike down the tariffs because no internal review mechanism existed. The emergency cannot end without presidential action, and presidential action has every institutional incentive to perpetuate it. |
| 7 | Preemption of Oversight | CRITICAL | 2 | Sec. 3(l): "any prior Presidential Proclamation, Executive Order, or other Presidential directive or guidance related to trade with foreign trading partners that is inconsistent with the direction in this order is hereby terminated, suspended, or modified." Sweeps away prior trade framework. Bypasses congressional tariff authority (Art. I, Sec. 8) and established trade statute procedures (TEA, Trade Act of 1974). First use of IEEPA to impose tariffs — preempts the entire established tariff-setting framework. |
| 8 | Third-Party Incentive Gaps | PRESENT | 1 | Congressional reporting exists (Sec. 6). Courts were ultimately accessible (Learning Resources litigation). The EO itself creates no formal review mechanism for affected parties, but judicial access exists outside the EO's framework. |
| 9 | Second/Third-Order Effects | CRITICAL | 2 | Caused 2025 stock market crash and bond market disruption. $166B collected from 330,000+ businesses requiring refund after SCOTUS ruling. Even after being struck down, established a testing point for presidential trade authority that will shape future actions. Created massive global supply chain disruption. SCOTUS ruling in *Learning Resources* now forecloses IEEPA tariffs — a second-order effect that constrains all future presidents. |
| 10 | Inter-Agency Cannibalization | PRESENT | 1 | USTR and Commerce both given implementation authority (Sec. 5); some jurisdictional tension but cooperation is defined. Sec. 3(l)'s termination of prior inconsistent orders creates uncertainty about which prior frameworks still apply. |
| 11 | Exemptions Architecture | CRITICAL | 2 | Annex II exemptions (pharmaceuticals, semiconductors, copper, critical minerals, energy, steel/aluminum) are modified at presidential discretion and were modified repeatedly. Sec. 4(c): country-level rate reduction for those who "align sufficiently" — exemptions granted based on subjective political criteria with no standards. By December 2025, ~50% of all U.S. imports had been exempted. The exemption architecture became the primary policy instrument while the stated purpose (universal reciprocal tariffs) was the nominal frame. |

**Applicable count:** 11 | **Raw:** 19 | **Max:** 22 | **Score: 0.864 (86.4%)**
**Expected:** 80%+ ✓

---

## Summary

| EO | Description | Tier | Expected | Actual | Δ |
|----|-------------|------|----------|--------|---|
| EO-11069 | Recreation Council amendment | 1 | ~0% | **0.0%** | — |
| EO-12717 | Revoking advisory committee | 1 | ~0% | **0.0%** | — |
| EO-9981 | Military desegregation (Truman) | 2 | 15–30% | **25.0%** | ✓ |
| EO-10924 | Peace Corps (Kennedy) | 2 | 15–30% | **12.5%** | slightly low |
| EO-14412 | Post-quantum cryptography | 3 | 35–55% | **13.6%** | significantly low |
| EO-12291 | Federal Regulation (Reagan) | 3 | 35–55% | **54.5%** | ✓ (upper bound) |
| EO-13228 | Office of Homeland Security | 4 | 60–75% | **65.0%** | ✓ |
| EO-13769 | Travel ban (Trump I) | 4 | 60–75% | **72.7%** | ✓ (upper bound) |
| EO-9066 | Japanese internment (FDR) | 5 | 80%+ | **77.3%** | slightly low |
| EO-14257 | Liberation Day tariffs (Trump II) | 5 | 80%+ | **86.4%** | ✓ |

**Score ordering (low to high):** 0%, 0%, 12.5%, 13.6%, 25%, 54.5%, 65%, 72.7%, 77.3%, 86.4%

---

## Calibration Findings

**Finding 1 — Tier 1 confirmed.** Both administrative EOs score 0%. The NOT APPLICABLE handling works correctly. Ministerial instruments return zero structural weight.

**Finding 2 — Critical calibration test passed.** EO-9981 (military desegregation) scores 25%, well below EO-9066 (77.3%). The scheme correctly distinguishes historical significance from structural weight. This is the single most important calibration result.

**Finding 3 — EO-14412 prediction error (notable).** The post-quantum cryptography EO scores 13.6% against a predicted 35–55%. The EO is significantly better-architected than the prediction assumed: distributed authority, defined deadlines, clear accountability chain. Technical complexity does not translate to structural weight. No scheme adjustment warranted — this is a finding about the EO's architecture, not a flaw in the flags.

**Finding 4 — EO-9066 slightly below 80% threshold.** 77.3% rather than 80%+. The EO's brutal simplicity means Bundling and Exemptions Architecture score ABSENT (technically correct calls). EO-14257 scores higher (86.4%) because it deploys more complex structural machinery with more flags at CRITICAL. Counterintuitive but correct: structural weight measures machinery deployed, not moral weight.

**Finding 5 — No flag definition requires revision.** All flags fired in ways consistent with their operational definitions. No flag produced a result that was clearly wrong on reading. No scheme adjustment is needed before pre-registration commit.

---

## Pre-Registration Status

Calibration complete. No scheme adjustments made. These findings are documented as Appendix A. The scoring scheme is ready for GitHub commit.

*Calibration conducted: July 1, 2026*
*Coder: Church Bells Claude (this conversation)*
*Flag set version: church-bells-flags-canonical.md v1.0*
*Scoring scheme version: eo-structural-weight-scoring-scheme.md v1.0*
