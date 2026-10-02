# Systems author verification, 2026-10-02 UTC

This is maintainer verification of course artifacts, not learner-submitted evidence and not a passed learner gate.

## Environment and scope

The local interpreter reported Python 3.11.11. The L0 tools use the standard library. PyTorch was not installed; the explicit CUDA prerequisite attempt returned exit 2 with `CUDA backend requires an already installed, approved PyTorch environment`. Physical GPU work is NOT_RUN. No driver, firmware, networking, BMC, DCGM, power, thermal, or rack changes were made.

## Executed results

`python3 -m unittest discover -s labs/systems -p 'test_*.py' -v` ran 19 tests and passed. Tests cover model controls, partial repairs, numeric boundaries, invalid input, protected writes, reset preservation, source-fixture drift, checkpoint corruption, unpublished generations, backend consistency, and exact resumed/reference equality for Python.

All six scenarios were also executed through actual subprocess CLI invocations:

| Scenario | Initial check | Configured recovery | Healthy control | Reset to original |
|---|---|---|---|---|
| domains | FAIL, exit 1 | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| inventory | FAIL, exit 1 | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| gpu | FAIL, exit 1 | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| fabric | FAIL, exit 1 | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| telemetry | FAIL, exit 1 | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| workload | FAIL, exit 1 | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |

The queue's initial result had 80 requests over 16 s, throughput 5 requests/s, goodput 0.625 requests/s, and p99 7,000 ms. The recovered four-arrivals/s configuration had 40 requests over 9.8 s, throughput and goodput 4.0816 requests/s, and p99 800 ms. These are synthetic simulator outputs, not real serving measurements.

The Python training baseline completed step 40. A second run intentionally stopped after 23 with exit 3 and a published step-20 checkpoint. Resume completed from 20 to 40 with exit 0, and final predictions matched the uninterrupted reference exactly. The final reference weight was 1.9904202954179437, bias 0.9998670772004215, MSE 0.000057374380895317426, and all four predictions met the 0.1 absolute-error tolerance.

A deliberately corrupted checkpoint was rejected with exit 2 and `checkpoint checksum mismatch`. No attempt was made to hide that expected failure by modifying the manifest hash.

The author workflow outputs are retained locally under `learner-work/systems/author-validation-20261002/`, marked as AUTHOR TEST NOT LEARNER EVIDENCE. That ignored working directory is not a required distributed artifact; readers reproduce their own evidence from the documented commands.

## Documentation checks

The seven owned curriculum chapters and systems runbooks were checked for ASCII text, paired code fences, existing relative Markdown link targets, and source-ledger coverage. All checks passed. `git diff --check` passed at this point in the shared workspace. The source ledger contains 37 official-source records with actual access date, scope, support, limitations, and separate negative findings.

These checks do not prove instructional effectiveness, remote-source freshness after the access date, software support for an unspecified host, or physical behavior. The root coordinator separately reviewed chapter theory and reran the systems unit suite. Source-verification facts and unexecuted hardware boundaries are kept separate throughout the material.
