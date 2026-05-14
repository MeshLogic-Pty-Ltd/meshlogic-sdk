# Security Policy

MeshLogic Pty Ltd takes the security of our software seriously. This document describes how to report a vulnerability and what to expect.

The canonical, full vulnerability-management process is at [`docs/security/vulnerability-management.md`](https://github.com/MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod/blob/main/docs/security/vulnerability-management.md). What you see below is the quick reference.

---

## Reporting a Vulnerability

**Preferred:** Open a private GitHub Security Advisory at this repository's [Security tab](https://github.com/MeshLogic-Pty-Ltd/meshlogic-sdk/security/advisories/new).

**Alternative:** Email `security@meshlogic.ai` with:
- A description of the issue
- Steps to reproduce
- Affected component(s) + version(s) if known
- Your CVSS v3.1 estimate (if known)
- Whether you'd like to be publicly credited

We acknowledge **all** reports. SLAs:

| Severity | Acknowledge | Triage complete | Fix deployed |
|---|---|---|---|
| **Critical (CVSS 9.0+)** | 24h | 48h | 7 days |
| **High (CVSS 7.0–8.9)** | 72h | 7 days | 30 days |
| **Medium (CVSS 4.0–6.9)** | 7 days | 14 days | 90 days |
| **Low (CVSS 0.1–3.9)** | 14 days | 30 days | 180 days |

See [§3 of the canonical process](https://github.com/MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod/blob/main/docs/security/vulnerability-management.md#3-response-slas) for SLA clock definitions.

---

## Safe Harbor

MeshLogic supports good-faith security research. We will not pursue legal action against researchers who:

1. Make a good-faith effort to avoid privacy violations, destruction of data, and service interruption.
2. Only access the minimum data necessary to demonstrate the vulnerability.
3. Provide MeshLogic reasonable time (90 days by default) to address the issue before public disclosure.
4. Do not exploit the vulnerability beyond what is necessary to confirm it exists.

Full Safe Harbor terms (including scope authorisation rules) are at [§8 of the canonical process](https://github.com/MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod/blob/main/docs/security/vulnerability-management.md#8-safe-harbor).

---

## Out of Scope

Please do **not** report:

- **DoS / volumetric testing** against any MeshLogic-operated service
- **Social engineering** of MeshLogic personnel
- **Physical attacks** against MeshLogic facilities or personnel
- Issues in **third-party SaaS** we use but do not operate (Vanta, Sentry, etc. — report directly to that vendor)
- Issues in **customer-controlled tenants** without that customer's explicit written authorisation

---

## Recognition

Researchers acting in good faith are publicly acknowledged in the published advisory (with your permission) and on the [MeshLogic Trust Centre Hall of Fame](https://meshlogic.ai/security/program#hall-of-fame).

**MeshLogic does not currently offer a monetary bug bounty.** This is under consideration once we reach 3+ paying customers (tracked as [PRODSEC-010](https://github.com/MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod/issues?q=PRODSEC-010)).

---

## Disclosure Timeline

MeshLogic adopts the **Google Project Zero 90-day default**:

- **Day 0:** Report received, acknowledged within SLA
- **Day 0–30:** Triage, fix developed and tested
- **Day 30–90:** Coordinated disclosure window; patch deployed; advisory drafted
- **Day 90:** Advisory published; CVE assigned (if applicable); affected customers notified
- **Extension:** Up to 14 additional days may be granted for genuinely complex fixes (in writing)

---

## Public Documents

- **Disclosure policy:** *(forthcoming)* will be mirrored at [meshlogic.ai/security/disclosure-policy](https://meshlogic.ai/security/disclosure-policy) once the marketing-site change ships. Canonical version lives at [`docs/security/vulnerability-management.md`](https://github.com/MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod/blob/main/docs/security/vulnerability-management.md) in the meantime.
- **security.txt (RFC 9116):** *(forthcoming)* will be served from [meshlogic.ai/.well-known/security.txt](https://meshlogic.ai/.well-known/security.txt) alongside the disclosure-policy publication.
- **Trust Centre:** *(forthcoming)* [meshlogic.ai/security/program](https://meshlogic.ai/security/program) — Hall of Fame + advisory archive will publish once active.

---

## About this repository

This SECURITY.md lives in `MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod`. The same template is published across all MeshLogic-Pty-Ltd repositories with the per-repo Security tab URL above adjusted to the appropriate repository. Reports against a specific repository may be made via its Security tab; reports against MeshLogic infrastructure or unclear scope should go to `security@meshlogic.ai`.

For multi-repo or supply-chain vulnerabilities, prefer `security@meshlogic.ai` so we can route to all affected repos.

---

*Last updated 2026-05-14. Reviewed annually under [PRODSEC-009](https://github.com/MeshLogic-Pty-Ltd/MeshLogic-Platform-Prod/issues?q=PRODSEC-009).*