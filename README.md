# tka-10822-pipdeptree-urllib3-partial-scan

**Jira:** [TKA-10822](https://mend-io.atlassian.net/browse/TKA-10822)
**Customer:** Fidelity Investments (Strategic) — self-hosted Repository Integration (SCM scanner 26.7.1.1 / SCA agent 26.6.2)

## What this repo reproduces

Mend for GHE SCA marks a pip scan **partial** because of a `urllib3` version
installed by the scan's **own** `pipdeptree` step — not by the customer's project.

The contamination triangle:

1. `requirements.txt` pins `boto3~=1.26.64`, which forces `botocore<1.30`, which
   constrains `urllib3<1.27`. So `pip install -r requirements.txt` resolves
   **`urllib3 1.26.20`** ✅
2. With `python.resolveHierarchyTree=true` (the documented default), the scanner
   then runs `pip install pipdeptree` in the same virtualenv. `pipdeptree`'s
   transitive dependency **`nab-index>=0.0.11`** requires **`urllib3>=2.0`**,
   upgrading the venv to **`urllib3 2.7.0`** ⚠️
3. The scanner's skip-filter correctly recognizes `urllib3-2.7.0` as a
   pipdeptree-only package and skips it for the **repo-root** resolution path —
   but **fails to apply the same skip for the `requirements.txt` path**, emitting:

   ```
   RESOLUTION WARN: Failed to resolve the following dependencies: [urllib3-2.7.0]
   from /tmp/ws-scm/.../requirements.txt
   ```

   and, for that path, three lines of:

   ```
   dependency: urllib3-2.7.0 from .../requirements.txt, might not have been resolved completely
   ```

4. The `RESOLUTION` step for `requirements.txt` is recorded `success:false` →
   the scan is flagged **partial**, even though `urllib3-2.7.0` was never fetched
   for the project and the real tree resolved correctly.

`typing_extensions` (installed by both the project install and the pipdeptree
install, same version) produced no warning — confirming this is specific to the
version-**upgrade** conflict case.

## Expected behavior (after fix)

- `urllib3-2.7.0` is skipped for **both** the repo-root and `requirements.txt` paths.
- No `RESOLUTION WARN` is emitted for `urllib3-2.7.0`.
- The scan completes **without** a partial flag.
- `urllib3-2.7.0` does not appear in the dependency inventory (already true today).

## Files

| File | Role |
|---|---|
| `requirements.txt` | Pins `boto3~=1.26.64` (the upper-bound `urllib3<1.27` trigger) + `beautifulsoup4`, `requests`. |
| `setup.py` | A **named** setup.py (not bare) so the scan has a second manifest path — reproduces the multi-manifest condition without confounding TKA-10149's bare-setup bug. |
| `.whitesource` | `configMode: LOCAL` so the scanner reads `whitesource.config`. |
| `whitesource.config` | `python.resolveHierarchyTree=true`, `python.ignorePipInstallErrors=true`, `python.applyConstraints=false` — the exact toggles Fidelity ran. |
| `autotest_config.json` | Asserts the scanner-log fingerprint (`ne` on the urllib3-2.7.0 WARN). Test is `xfail` until the skip-filter fix ships. |

## How the assertion discriminates

The dependency tree is **correct** in both the buggy and fixed states (urllib3-2.7.0
is never really added), so an inventory check cannot tell them apart. The only
observable difference is the spurious partial-scan `RESOLUTION WARN` in the scanner
log — so `autotest_config.json` uses a negative log-line check (`ne`) on
`Failed to resolve the following dependencies: [urllib3-2.7.0]` as the discriminator.
