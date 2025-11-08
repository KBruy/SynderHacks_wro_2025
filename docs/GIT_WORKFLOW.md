# Git Workflow & Branching Strategy

> Przewodnik po strategii Git dla 3-osobowego zespołu

---

## Branching Model

### Branch Hierarchy

```
main (protected)
│
├── frontend/*        # Frontend features (Person 1)
│   ├── frontend/recommendation-cards
│   ├── frontend/product-list
│   └── frontend/analytics-dashboard
│
├── ai/*             # AI/ML features (Person 2)
│   ├── ai/market-analysis
│   ├── ai/price-optimization
│   └── ai/recommendation-engine
│
├── backend/*        # Backend features (Person 3)
│   ├── backend/shopify-connector
│   ├── backend/api-endpoints
│   └── backend/database-schema
│
└── hotfix/*         # Emergency fixes (anyone)
    └── hotfix/auth-bug
```

---

## Branch Protection Rules

### Main Branch

**Protected** - Cannot push directly, requires PR

**Rules**:
- ✅ Require pull request reviews (1 approval minimum)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ❌ No force push allowed
- ❌ No deletion allowed

**Setup on GitHub**:
1. Go to **Settings** → **Branches**
2. Add rule for `main`
3. Enable protections above

---

## Daily Git Workflow

### Morning Routine

```bash
# 1. Ensure you're on main and it's up to date
git checkout main
git pull origin main

# 2. Create or switch to your feature branch
git checkout -b <role>/<feature-name>
# OR if branch exists:
git checkout <role>/<feature-name>

# 3. Update your branch with latest main
git merge main

# 4. Start coding!
```

### During Development

```bash
# Stage changes (be selective)
git add src/components/NewComponent.tsx
git add src/types/recommendation.ts

# OR stage all changes
git add .

# Commit with meaningful message
git commit -m "feat(frontend): add recommendation card component"

# Push to remote (backup + visibility)
git push origin <your-branch-name>
```

**Commit Frequency**: Every 30-60 minutes, or when completing a logical unit of work

### End of Day

```bash
# Make sure all work is committed and pushed
git status  # Should be clean

git add .
git commit -m "feat(ai): WIP - market analysis prompt template"
git push origin <your-branch-name>

# Update team in Slack/Discord
```

---

## Commit Message Convention

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(frontend): add product filter` |
| `fix` | Bug fix | `fix(api): handle null product SKU` |
| `docs` | Documentation | `docs(api): update endpoint spec` |
| `refactor` | Code refactoring | `refactor(ai): simplify prompt logic` |
| `test` | Adding tests | `test(backend): add sync service tests` |
| `chore` | Maintenance | `chore(deps): update dependencies` |
| `style` | Code style/formatting | `style(frontend): fix indentation` |
| `perf` | Performance improvement | `perf(ai): cache GPT-4 responses` |

### Scopes

| Scope | Usage | Owner |
|-------|-------|-------|
| `frontend` | React components, UI | Person 1 |
| `backend` | API, controllers | Person 3 |
| `ai` | AI/ML services | Person 2 |
| `sync` | Platform sync logic | Person 3 |
| `api` | API endpoints/contracts | Person 3 |
| `db` | Database/Prisma | Person 3 |
| `docs` | Documentation | Anyone |

### Examples

**Good commits**:
```bash
feat(frontend): add recommendation card with apply action
fix(ai): correct price calculation in market analysis
docs(api): update recommendations endpoint schema
refactor(backend): extract Shopify auth to service
test(sync): add integration tests for WooCommerce sync
chore(deps): upgrade React to 18.3
```

**Bad commits** (avoid these):
```bash
fix stuff
WIP
asdf
Update file
Changes
Fixed bug
```

### Detailed Commit Body (when needed)

```bash
git commit -m "feat(ai): implement market analysis engine

- Add GPT-4 integration for competitive pricing
- Cache results in Redis for 1 hour
- Return confidence scores with recommendations
- Handle rate limiting with exponential backoff

Closes #42"
```

---

## Feature Branch Workflow

### 1. Create Feature Branch

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b <role>/<feature-name>

# Examples:
git checkout -b frontend/recommendation-hub
git checkout -b ai/market-analysis
git checkout -b backend/shopify-oauth
```

**Branch naming rules**:
- Lowercase only
- Use hyphens, not underscores
- Be descriptive but concise
- Include role prefix

### 2. Work on Feature

```bash
# Make changes, test locally
npm run dev

# Stage and commit
git add .
git commit -m "feat(frontend): add recommendation list view"

# Push to remote regularly
git push origin frontend/recommendation-hub
```

### 3. Keep Branch Updated

```bash
# At least once per day, merge latest main
git checkout main
git pull origin main

git checkout <your-branch>
git merge main

# Resolve conflicts if any (see below)
# Test that everything still works!
npm run dev

# Push updated branch
git push origin <your-branch>
```

### 4. Create Pull Request

**When branch is ready**:
1. Push final changes
2. Go to GitHub repository
3. Click **Pull requests** → **New pull request**
4. Select your branch
5. Fill out PR template (see below)
6. Request review from teammate
7. Post in team chat

### 5. Code Review

**As author**:
- Respond to comments promptly
- Make requested changes
- Push updates to same branch (PR auto-updates)
- Re-request review when ready

**As reviewer**:
- Review within 4 hours
- Check functionality, code quality, tests
- Approve or request changes
- Be constructive, not critical

### 6. Merge Pull Request

**After approval**:
1. Ensure all checks pass (CI/CD)
2. Resolve any conflicts with main
3. Click **Squash and merge** (preferred)
4. Delete branch after merge

**Squash merge**: Combines all commits into one clean commit on main

---

## Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] New feature (non-breaking change)
- [ ] Bug fix (non-breaking change)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Related Issues
Closes #<issue-number>

## How to Test
1. Step 1
2. Step 2
3. Expected result

## Screenshots (if UI change)
[Add screenshots or screen recording]

## API Changes
- [ ] No API changes
- [ ] API changes documented in `Backend/backend_api_spec.md`
- [ ] Frontend team notified

## Database Changes
- [ ] No database changes
- [ ] Migration included
- [ ] Team notified to run migrations

## Checklist
- [ ] Code builds without errors
- [ ] No TypeScript errors
- [ ] Linting passes
- [ ] Code formatted with Prettier
- [ ] Tested locally
- [ ] No console.log statements (except intentional logging)
- [ ] No commented-out code
- [ ] No secrets/API keys in code

## Additional Notes
Any other context about the PR
```

---

## Handling Merge Conflicts

### Prevention

1. **Pull from main daily**
2. **Keep PRs small** (1-2 days of work)
3. **Merge PRs quickly** (don't let them sit)
4. **Communicate** when working on same areas

### Resolution Steps

#### Step 1: Fetch latest main

```bash
git checkout main
git pull origin main
```

#### Step 2: Merge main into your branch

```bash
git checkout <your-branch>
git merge main
```

#### Step 3: Resolve conflicts

Git will mark conflicts in files:

```typescript
<<<<<<< HEAD
// Your changes
const apiUrl = 'http://localhost:3000';
=======
// Changes from main
const apiUrl = process.env.VITE_API_URL;
>>>>>>> main
```

**Edit file to keep correct version**:
```typescript
// Resolved version
const apiUrl = process.env.VITE_API_URL || 'http://localhost:3000';
```

**Remove conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)

#### Step 4: Mark as resolved

```bash
git add <conflicted-file>
```

#### Step 5: Complete merge

```bash
git commit -m "merge: resolve conflicts with main"
```

#### Step 6: Test!

```bash
npm run dev
# Make sure everything still works!
```

#### Step 7: Push

```bash
git push origin <your-branch>
```

### Complex Conflicts

**If stuck**:
1. Ask teammate for help (screen share)
2. Use VSCode merge conflict resolver
3. Or abort and start fresh:
   ```bash
   git merge --abort
   git stash  # Save your work
   git pull origin main
   git stash pop  # Reapply your work
   ```

---

## Special Scenarios

### Hotfix Workflow (Critical Bugs)

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/<bug-description>

# 2. Fix the bug
# ... make changes ...

# 3. Commit and push
git add .
git commit -m "fix(api): prevent null pointer in auth middleware"
git push origin hotfix/<bug-description>

# 4. Create PR with [HOTFIX] prefix
# Title: "[HOTFIX] Fix null pointer in auth"

# 5. Get immediate review
# Tag team in PR

# 6. Merge ASAP
# All team members pull main immediately
```

### Updating API Contract

**Process** (Backend Developer initiates):

```bash
# 1. Create branch
git checkout -b backend/api-recommendation-confidence

# 2. Update spec
# Edit Backend/backend_api_spec.md

# 3. Commit with clear message
git commit -m "docs(api): add confidence field to recommendations

BREAKING CHANGE: Recommendations now include confidence (0-1)

Frontend impact: Display confidence as percentage
AI impact: Must calculate and return confidence score"

# 4. Create PR with [API CHANGE] prefix
# Title: "[API CHANGE] Add confidence to recommendations"

# 5. Request review from ALL team members

# 6. Wait for approvals before merge

# 7. After merge, affected team members update their code
```

### Database Migration

**Process** (Backend Developer):

```bash
# 1. Create migration
cd backend
npx prisma migrate dev --name add_confidence_to_recommendations

# 2. Commit migration files
git add prisma/migrations/
git commit -m "feat(db): add confidence field to recommendations table"

# 3. Push and create PR
git push origin backend/db-confidence-field

# 4. In PR description, add:
# "⚠️ DATABASE MIGRATION - Team must run `npx prisma migrate dev` after pulling"

# 5. Post in team chat when merged
# "Migration merged! Run `cd backend && npx prisma migrate dev`"
```

**Team action after pull**:
```bash
git checkout main
git pull origin main
cd backend
npx prisma migrate dev
npx prisma generate
```

### Rollback Changes

**If something breaks after merge**:

#### Option 1: Revert commit

```bash
# Find commit hash
git log --oneline -10

# Revert the commit (creates new commit)
git revert <commit-hash>
git push origin main

# This is safe - doesn't rewrite history
```

#### Option 2: Fix forward (preferred)

```bash
# Create hotfix branch
git checkout -b hotfix/fix-broken-feature

# Fix the issue
# ... changes ...

# PR and merge quickly
```

---

## Git Best Practices

### DO ✅

- **Commit frequently** (small, logical units)
- **Write descriptive commit messages**
- **Pull from main daily**
- **Push to remote regularly** (backup)
- **Review your own diff before pushing**
  ```bash
  git diff  # See what changed
  ```
- **Test before creating PR**
- **Keep PRs small and focused**
- **Resolve conflicts immediately**
- **Delete branches after merge**

### DON'T ❌

- **Don't commit secrets/API keys**
  ```bash
  # Use .gitignore for .env files
  ```
- **Don't push directly to main**
- **Don't force push to shared branches**
  ```bash
  git push --force  # DANGER!
  ```
- **Don't commit large files** (images, videos, binaries)
- **Don't commit `node_modules/`** (should be in .gitignore)
- **Don't leave PRs open for >48 hours**
- **Don't rewrite history on shared branches**
  ```bash
  git rebase  # Use with caution
  ```

---

## Git Commands Cheat Sheet

### Daily Commands

```bash
# Status and info
git status                    # See what changed
git log --oneline -10        # Recent commits
git diff                     # See unstaged changes
git diff --staged            # See staged changes

# Branching
git branch                   # List local branches
git branch -a                # List all branches (including remote)
git checkout <branch>        # Switch branch
git checkout -b <branch>     # Create and switch to new branch
git branch -d <branch>       # Delete local branch

# Staging and committing
git add <file>               # Stage specific file
git add .                    # Stage all changes
git commit -m "message"      # Commit staged changes
git commit --amend           # Modify last commit (use carefully!)

# Syncing
git pull origin main         # Pull latest main
git push origin <branch>     # Push your branch
git fetch origin             # Fetch without merging

# Merging
git merge main               # Merge main into current branch
git merge --abort            # Abort merge if conflicts

# Stashing (temporary save)
git stash                    # Save changes temporarily
git stash pop                # Restore stashed changes
git stash list               # List stashes
```

### Less Common Commands

```bash
# Undoing changes
git restore <file>           # Discard changes in file
git restore --staged <file>  # Unstage file
git reset HEAD~1             # Undo last commit (keep changes)
git reset --hard HEAD~1      # Undo last commit (discard changes) ⚠️

# History
git log --graph --oneline --all  # Visual branch history
git log --author="Name"          # Commits by author
git log --since="2 days ago"     # Recent commits
git blame <file>                 # See who changed each line

# Remote
git remote -v                # Show remotes
git fetch --prune            # Clean up deleted remote branches

# Cleanup
git clean -fd                # Remove untracked files ⚠️
git gc                       # Garbage collection (optimize repo)
```

---

## Troubleshooting

### "I committed to main by accident"

```bash
# If not pushed yet
git reset HEAD~1             # Undo commit, keep changes
git checkout -b <role>/feature-name  # Create proper branch
git add .
git commit -m "proper message"

# If already pushed (contact team immediately!)
git revert <commit-hash>
git push origin main
```

### "I need to undo my last commit"

```bash
# Keep changes (most common)
git reset --soft HEAD~1

# Discard changes (careful!)
git reset --hard HEAD~1
```

### "I'm on the wrong branch"

```bash
# Move changes to correct branch
git stash                    # Save changes
git checkout <correct-branch>
git stash pop                # Apply changes
```

### "My branch is way behind main"

```bash
git checkout main
git pull origin main
git checkout <your-branch>
git merge main
# Resolve conflicts
# Test!
git push origin <your-branch>
```

### "I deleted a file by accident"

```bash
# Restore from last commit
git restore <file>

# Or restore from specific commit
git checkout <commit-hash> -- <file>
```

---

## GitHub Features

### Pull Request Reviews

**Requesting review**:
1. Create PR
2. Click **Reviewers** on right sidebar
3. Select teammate(s)
4. Post link in team chat

**Reviewing**:
1. Click **Files changed** tab
2. Add comments (line-by-line or general)
3. Click **Review changes** button
4. Choose: **Approve**, **Comment**, or **Request changes**

### GitHub CLI (optional)

```bash
# Install
brew install gh  # macOS
# OR download from: https://cli.github.com

# Login
gh auth login

# Create PR from command line
gh pr create --title "feat: add feature" --body "Description"

# List PRs
gh pr list

# Check out PR locally
gh pr checkout <PR-number>

# Merge PR
gh pr merge <PR-number> --squash
```

---

## Team Sync Checklist

### Before Creating PR
- [ ] Code builds without errors
- [ ] Tests pass (if written)
- [ ] Linting passes
- [ ] Code formatted
- [ ] Branch updated with latest main
- [ ] Manually tested feature
- [ ] PR description filled out

### Before Merging PR
- [ ] At least 1 approval
- [ ] All checks pass (CI/CD)
- [ ] No merge conflicts
- [ ] API changes documented (if any)
- [ ] Team notified of breaking changes (if any)

### After Merging PR
- [ ] Delete feature branch
- [ ] Post update in team chat
- [ ] Close related issues
- [ ] Pull main locally
  ```bash
  git checkout main
  git pull origin main
  ```

---

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)
- [Conventional Commits](https://www.conventionalcommits.org)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Questions?** Ask in #dev-general or create issue with `question` label

**Last Updated**: 2025-11-08
