# LIFE RPG / LIFEDEX — Contribution & Git Guidelines (CONTRIBUTING.md)

Welcome to the **LIFE RPG / LIFEDEX** team repository. Because 4 autonomous developer agents are collaborating simultaneously on this single repository, everyone must adhere to strict Git and code quality protocols.

---

## 1. Git Branching Strategy

- **`main`**: The single protected trunk representing tested, stable releases. Never commit directly to `main`.
- **Feature Branches**:
  - Person 1 (Backend & Systems): `feature/game-engine` or `feature/backend-*`
  - Person 2 (Frontend & UI/UX): `feature/frontend-*`
  - Person 3 (Database & Security): `feature/db-*`
  - Person 4 (QA, CI/CD & Deployment): `feature/qa-*` or `feature/cicd-*`

---

## 2. Strictly Prohibited Actions

To protect team integrity and avoid data loss:
- ❌ **NEVER** run `git push --force` or `git push -f`.
- ❌ **NEVER** run `git reset --hard` on shared branches.
- ❌ **NEVER** overwrite another developer's files without coordinating.
- ❌ **NEVER** delete another developer's remote branch.
- ❌ **NEVER** commit secrets, API keys, or `.env` files.

---

## 3. Pre-Commit Checklist

Before committing changes, ensure:
1. **Branch Verification**: Run `git branch` to ensure you are on your designated feature branch.
2. **Status Inspection**: Run `git status` to verify exactly what files are staged.
3. **Tests Pass**: Run the test suite:
   ```bash
   pytest backend/tests/
   ```
4. **No Type / Lint Violations**: Ensure clean formatting and valid type hints.

---

## 4. Commit Message Standard

Use the Conventional Commits specification:
- `feat(engine)`: New game mechanic or backend service.
- `feat(api)`: New REST API endpoint or route controller.
- `feat(ui)`: New frontend component or screen.
- `fix(streak)`: Bugfix in streak logic or date calculation.
- `docs(api)`: Updates to shared documentation or API contracts.
- `test(evolution)`: Added unit tests or edge case coverage.

Example:
```bash
git commit -m "feat(evolution): implement deterministic Tier 2 attribute dominance algorithm"
```

---

## 5. Merging & Integration Protocol

1. Keep feature branches short-lived and focused on single milestones.
2. Ensure working tree is clean and all documentation matches code reality.
3. Submit Pull Requests to `main` with a clear description of:
   - What was implemented.
   - What tests were added and verified.
   - Impacts on other team members (Person 2, 3, or 4).
