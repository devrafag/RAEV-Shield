# RAEV Shield — product roadmap

Every release must advance three tracks together:

1. **Privacy:** measurable protection with fail-closed behavior.
2. **Experience:** fewer steps, clearer language, and safer defaults.
3. **Design:** a more coherent, accessible, and polished interface.

A version is not complete until its security claims are covered by tests and its main workflow has been visually reviewed on Windows.

## v0.2 — Truthful diagnostics

- Privacy: IP, Tor reachability, DNS, IPv4/IPv6, and proxy-bypass checks.
- Experience: one guided diagnostic with plain-language remediation.
- Design: real status dashboard, severity hierarchy, and accessible states.

## v0.3 — Fail closed

- Privacy: Windows firewall kill switch with recovery and uninstall cleanup.
- Experience: safe activation, rollback, and emergency-stop flow.
- Design: live protection timeline and clear blocked-traffic feedback.

## v0.4 — Transparent per-app routing

- Privacy: reviewed TUN/WFP routing for applications that ignore SOCKS.
- Experience: drag an executable into RAEV Shield and test compatibility.
- Design: visual route map and per-application privacy controls.

## v0.5 — Disposable identities

- Privacy: isolated profiles, temporary storage, and download quarantine.
- Experience: Personal, Private, and Disposable modes.
- Design: simplified mode selection with risk-aware explanations.

## v1.0 — Trusted release

- Privacy: independent audit, reproducible builds, signed updates, and published hashes.
- Experience: signed installer, automatic updates, onboarding, and recovery.
- Design: complete responsive Windows interface and consistent brand system.

## Release gate

Every release requires:

- automated tests passing;
- no unsupported anonymity claim;
- leak and failure-path testing for changed network behavior;
- keyboard and readable-contrast review;
- before/after interface review;
- updated limitations and threat model;
- a signed release when signing becomes available.

