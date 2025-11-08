# Team Workflow & Collaboration Guide

> **Cel**: Efektywna współpraca 3-osobowego zespołu z minimalnymi konfliktami i maksymalną produktywnością

---

## Team Composition

| Role | Primary Focus | Branches | Key Files |
|------|--------------|----------|-----------|
| **Person 1: Frontend** | React UI, UX, komponenty | `frontend/*` | `/frontend/src/**` |
| **Person 2: AI/Analysis** | GPT-4, rekomendacje, analiza | `ai/*` | `/backend/src/ai/**` |
| **Person 3: Backend/Sync** | API, connectors, sync | `backend/*` | `/backend/src/api/**`, `/backend/src/connectors/**` |

---

## Daily Workflow

### Morning (Start of Day)
```bash
# 1. Pull latest changes from main
git checkout main
git pull origin main

# 2. Create/switch to your feature branch
git checkout -b <role>/<feature-name>
# Example: frontend/recommendation-cards

# 3. Check for updates in API spec (if backend changed contracts)
git log --oneline Backend/backend_api_spec.md
```

### During Work
- **Commit early, commit often** (every 30-60 min)
- **Push to remote** at least 2x per day (backup + visibility)
- **Communicate blockers immediately** in team chat

### End of Day
```bash
# 1. Commit and push your work
git add .
git commit -m "feat(frontend): WIP recommendation card layout"
git push origin <your-branch>

# 2. Update team on progress (Slack/Discord)
# - What you completed
# - What's in progress
# - Any blockers for tomorrow
```

---

## Avoiding Merge Conflicts

### Rule 1: Clear File Ownership

**Frontend Developer owns**:
- `/frontend/**` (all files)
- **Never touch**: `/backend/**` (except reading for reference)

**AI/Analysis Developer owns**:
- `/backend/src/ai/**`
- `/backend/src/services/analysis/**`
- **Can touch**: `/backend/src/types/**` (coordinate with Backend dev)

**Backend/Sync Developer owns**:
- `/backend/src/api/**`
- `/backend/src/connectors/**`
- `/backend/src/sync/**`
- `/backend/prisma/**`
- `/backend/src/types/**` (source of truth for types)
- **Can touch**: Shared utilities, middleware

### Rule 2: API Contract is Sacred

**Process for API changes**:
1. Backend dev proposes change in `Backend/backend_api_spec.md`
2. Creates PR with `[API CHANGE]` prefix
3. **ALL team members must review and approve** before merge
4. Frontend dev updates API client after merge
5. AI dev updates service calls if needed

**Example**:
```
PR Title: [API CHANGE] Add confidence field to recommendations
Description: Adding confidence score (0-1) to recommendation response
Impact: Frontend needs to display this, AI needs to calculate it
```

### Rule 3: Shared Types Sync

**Workflow**:
1. Backend dev creates/updates type in `/backend/src/types/`
2. Commits and pushes
3. **Immediately notifies Frontend dev** (Slack/Discord)
4. Frontend dev pulls and copies to `/frontend/src/types/`
5. Frontend dev confirms sync complete

**Alternative (better for larger project)**:
- Create shared types as npm package
- Import in both frontend and backend

---

## Branch Strategy

### Creating Feature Branch

```bash
# Pattern: <role>/<short-description>
git checkout main
git pull origin main
git checkout -b frontend/recommendation-hub
```

**Good branch names**:
- `frontend/recommendation-cards`
- `ai/market-analysis-prompt`
- `backend/shopify-connector`
- `backend/prisma-schema`

**Bad branch names**:
- `fix-stuff`
- `my-changes`
- `test-123`

### Working on Branch

```bash
# Make changes
git add .
git commit -m "feat(frontend): add recommendation card skeleton"

# Push regularly
git push origin frontend/recommendation-hub

# Keep branch up to date with main (once per day)
git checkout main
git pull origin main
git checkout frontend/recommendation-hub
git merge main
# Resolve conflicts if any
git push origin frontend/recommendation-hub
```

### Creating Pull Request

**When to create PR**:
- Feature is complete (not perfect, just working)
- All tests pass (if you wrote tests)
- Code is formatted (Prettier)
- No console errors

**PR Template**:
```markdown
## What does this PR do?
Brief description of the feature/fix

## Type of change
- [ ] Frontend feature
- [ ] Backend API
- [ ] AI/Analysis
- [ ] Database schema
- [ ] Bug fix
- [ ] Documentation

## Testing
How to test this:
1. Step 1
2. Step 2

## Screenshots (if UI change)
[Add screenshots]

## API Changes (if any)
- [ ] Updated backend_api_spec.md
- [ ] Frontend updated API client
- [ ] All team members notified

## Checklist
- [ ] Code builds without errors
- [ ] No TypeScript errors
- [ ] Formatted with Prettier
- [ ] Tested locally
```

**Review process**:
1. Create PR on GitHub
2. Request review from at least 1 team member
3. Post in team chat: "PR ready for review: [link]"
4. Reviewer has 4 hours to review (or notify if they need more time)
5. Address feedback, push changes
6. After approval: **Squash and merge** to `main`
7. Delete feature branch

---

## Handling Merge Conflicts

### Prevention (Best Practices)

1. **Pull from main daily** before starting work
2. **Keep PRs small** (1-2 days of work max)
3. **Merge PRs quickly** (don't let them sit for days)
4. **Communicate** when working on shared files

### Resolution (When Conflicts Happen)

**Step 1**: Update your branch
```bash
git checkout main
git pull origin main
git checkout <your-branch>
git merge main
```

**Step 2**: Resolve conflicts
```bash
# Git will mark conflicts in files like:
<<<<<<< HEAD
your changes
=======
changes from main
>>>>>>> main

# Edit files to keep correct version
# Remove conflict markers
```

**Step 3**: Test and commit
```bash
# Make sure everything still works!
npm run dev  # or npm test

git add .
git commit -m "merge: resolve conflicts with main"
git push origin <your-branch>
```

**If stuck**: Ask teammate for help immediately (screen share)

---

## Communication Protocols

### Slack/Discord Channels

**#dev-general**: General discussion, questions, help
**#dev-frontend**: Frontend-specific (Person 1)
**#dev-ai**: AI/Analysis-specific (Person 2)
**#dev-backend**: Backend-specific (Person 3)
**#dev-blockers**: Critical blockers (ping @everyone)
**#dev-prs**: PR notifications

### When to Notify Team

**Immediately notify when**:
- Changing API contracts
- Changing database schema
- Changing shared types
- You're blocked and can't proceed
- You found a critical bug
- You'll be unavailable for >2 hours

**Daily updates (end of day)**:
- What you completed today
- What you're working on tomorrow
- Any concerns/questions

### Code Review Expectations

**As author**:
- Provide context in PR description
- Link to related issues/docs
- Respond to feedback within 2 hours

**As reviewer**:
- Review within 4 hours
- Be constructive, not critical
- Approve if no major issues (minor issues can be fixed later)
- If you can't review in time, notify team

---

## Integration Points (Critical!)

### Frontend ↔ Backend

**Contract**: `/Backend/backend_api_spec.md`

**Process**:
1. Backend dev implements endpoint
2. Backend dev updates spec doc
3. Backend dev creates PR → notifies Frontend dev
4. Frontend dev reviews spec → approves PR
5. Frontend dev implements API client call

**Example flow**:
```
Backend: "I implemented GET /api/v1/recommendations, PR #12"
Frontend: "Reviewed spec, looks good. Will integrate tomorrow"
Backend: PR merged
Frontend: Integrates in frontend/recommendation-hub branch
```

### AI ↔ Backend

**Contract**: Service interfaces in `/backend/src/types/`

**Process**:
1. Backend dev defines interface (e.g., `RecommendationService`)
2. AI dev implements service
3. Backend dev calls service in API controllers

**Example**:
```typescript
// Backend dev creates interface
interface RecommendationService {
  generate(productId: string): Promise<Recommendation[]>
}

// AI dev implements
class AIRecommendationService implements RecommendationService {
  async generate(productId: string) {
    // GPT-4 magic
  }
}

// Backend dev uses in controller
const recommendations = await this.recommendationService.generate(productId)
```

### Database Changes

**Process** (Backend dev drives this):
1. Update `prisma/schema.prisma`
2. Run `npx prisma migrate dev --name <migration-name>`
3. **Notify team immediately** (they need to run migration locally)
4. Commit migration files
5. Update types if needed

**Team action**:
```bash
# When notified of DB changes
git pull origin main
cd backend
npx prisma migrate dev  # Applies migrations
npx prisma generate     # Updates Prisma client
```

---

## Local Development Setup

### Initial Setup (First Time)

**All team members**:
```bash
# 1. Clone repo
git clone <repo-url>
cd SynderHacks_wro_2025

# 2. Install global tools (if needed)
npm install -g pnpm  # Optional: faster than npm
```

**Frontend Developer**:
```bash
cd frontend
npm install
cp .env.example .env

# Edit .env
# VITE_API_URL=http://localhost:3000/api/v1

npm run dev
# Frontend runs on http://localhost:5173
```

**Backend/AI Developers**:
```bash
cd backend
npm install
cp .env.example .env

# Edit .env - add your API keys
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://localhost:6379
# OPENAI_API_KEY=sk-...

# Run database migrations
npx prisma migrate dev
npx prisma generate

npm run dev
# Backend runs on http://localhost:3000
```

### Daily Development

**Frontend Developer**:
```bash
cd frontend
npm run dev
# Work in browser at localhost:5173
# Hot reload enabled
```

**Backend Developer**:
```bash
cd backend
npm run dev
# API at localhost:3000
# Test with Thunder Client, Postman, or curl
```

**AI Developer**:
```bash
cd backend
npm run dev
# Test AI services via API endpoints
# Monitor OpenAI usage/costs
```

---

## Testing & Quality

### Before Creating PR

**Checklist**:
- [ ] Code builds without errors (`npm run build`)
- [ ] No TypeScript errors (`npm run type-check` or built into build)
- [ ] Formatted with Prettier (`npm run format` or VSCode auto-format)
- [ ] Linted (`npm run lint`)
- [ ] Tested manually (run dev server, test feature)
- [ ] No `console.log` left in code (except intentional logging)
- [ ] No commented-out code
- [ ] No secrets/API keys in code

**Frontend-specific**:
- [ ] Responsive (test mobile, tablet, desktop)
- [ ] Accessibility (keyboard navigation, screen reader friendly)
- [ ] Loading states implemented
- [ ] Error states handled

**Backend-specific**:
- [ ] Error handling with proper status codes
- [ ] Input validation (Zod schemas)
- [ ] Updated API spec doc if endpoints changed

**AI-specific**:
- [ ] Prompts stored in `/backend/src/ai/prompts/`
- [ ] Error handling for API failures
- [ ] Cost tracking/logging
- [ ] Results cached if appropriate

---

## Troubleshooting Common Issues

### "My code works but CI fails"

**Likely causes**:
- TypeScript errors (fix with `npm run type-check`)
- Linting errors (fix with `npm run lint`)
- Environment variables missing in CI (add to GitHub Secrets)

### "I can't pull from main - conflicts"

```bash
# Save your work first
git stash

# Pull main
git checkout main
git pull origin main

# Go back to your branch
git checkout <your-branch>

# Reapply your work
git stash pop

# Resolve conflicts if any
```

### "Frontend can't connect to backend"

**Checklist**:
- Is backend running? (`cd backend && npm run dev`)
- Check `VITE_API_URL` in frontend `.env`
- Check CORS settings in backend
- Check Network tab in browser DevTools

### "Database migration failed"

```bash
# Reset database (⚠️ loses data)
npx prisma migrate reset

# Or fix manually
npx prisma studio  # Opens DB GUI
```

### "OpenAI API errors"

**Common issues**:
- Invalid API key (check `.env`)
- Rate limit exceeded (slow down requests)
- Quota exceeded (check billing)
- Network timeout (increase timeout, add retry logic)

---

## Emergency Protocols

### Critical Bug in Main

1. **Notify team immediately** in #dev-blockers
2. Create `hotfix/<description>` branch from main
3. Fix bug
4. Create PR with `[HOTFIX]` prefix
5. Get immediate review (drop everything)
6. Merge ASAP
7. All team members pull main

### Blocked and Can't Proceed

1. **Post in #dev-blockers**: "Blocked on X, need help from Y"
2. Tag relevant teammate
3. Schedule quick sync call if needed (10-15 min)
4. Document resolution

### Accidentally Pushed to Main

**If caught immediately** (within minutes):
```bash
git revert <commit-hash>
git push origin main
```

**If not caught**: Create revert PR, notify team

---

## Weekly Sync (Recommended)

**Friday afternoon** (30 min):
- Review what was accomplished
- Identify blockers for next week
- Align on priorities
- Celebrate wins

**Agenda**:
1. Quick demo of features completed
2. Review open PRs
3. Discuss architecture decisions if needed
4. Plan next week's work

---

## Quick Reference

### Git Commands Cheat Sheet

```bash
# Start new feature
git checkout main && git pull && git checkout -b <role>/<feature>

# Commit work
git add . && git commit -m "<type>(<scope>): <description>"

# Push to remote
git push origin <branch-name>

# Update branch with latest main
git checkout main && git pull && git checkout <branch> && git merge main

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes (⚠️ careful!)
git reset --hard origin/<branch>

# See what changed
git status
git diff
git log --oneline -10
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build tasks, dependencies

### Useful VSCode Extensions

- **ESLint**: Linting
- **Prettier**: Formatting
- **GitLens**: Git superpowers
- **Thunder Client**: API testing
- **Prisma**: Prisma schema support

---

## Success Metrics

**Good collaboration looks like**:
- ✅ PRs merged within 24 hours of creation
- ✅ Zero merge conflicts (or resolved in <15 min)
- ✅ Main branch always builds and runs
- ✅ All team members unblocked
- ✅ Daily communication in team chat

**Red flags**:
- ❌ PRs sitting for >48 hours
- ❌ Frequent merge conflicts
- ❌ Main branch broken
- ❌ Team members blocked for >4 hours
- ❌ Silent periods (no communication for >8 hours during work day)

---

## Remember

1. **Communicate early and often**
2. **Small PRs > Large PRs**
3. **Test before pushing**
4. **Review code promptly**
5. **Ask for help when stuck**
6. **Be kind in code reviews**
7. **Celebrate small wins**

---

**Happy coding!** 🚀

**Questions?** Ask in #dev-general or create an issue in this repo with label `question`.
