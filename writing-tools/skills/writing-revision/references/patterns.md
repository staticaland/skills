# Extended Patterns and Examples

## Email Revisions

### Status Update Email

**Before:**

```
Hi team,

I just wanted to give everyone a quick update on where we are with the project. So basically, we've been working really hard on the backend integration and I think we're making good progress. There were some issues with the API but we managed to work through most of them. We're hoping to have everything wrapped up by next week but there might be some delays depending on how testing goes.

Let me know if you have any questions!
```

**After:**

```
**Project status:** Backend integration is 80% complete. On track for next Friday.

**Completed:**
- API integration (resolved authentication issues)
- Database schema migration

**Remaining:**
- Load testing (starts Monday)
- Security review (pending Jim's availability)

**Risk:** Testing may push delivery to the following Monday if we find performance issues.
```

### Request Email

**Before:**

```
Hey Sarah,

I hope you're doing well! I was wondering if you might have some time to help me out with something. I've been working on the quarterly report and I'm having some trouble with the data visualization section. I know you're really good at this kind of thing and I thought maybe you could take a look when you get a chance? No rush or anything, just whenever works for you.

Thanks so much!
```

**After:**

```
Sarah, I need help with data visualizations for the quarterly report.

**Ask:** Review my draft charts and suggest improvements. ~30 minutes of your time.

**Deadline:** Thursday EOD (report due Friday)

**Context:** Draft is in `shared/q3-report-draft.pdf`, pages 4-7.

Can you do Thursday morning?
```

## Slack Message Revisions

### Announcement

**Before:**

```
Hey everyone! So I wanted to let you all know that we're going to be doing some maintenance on the staging environment this weekend. It shouldn't take too long but there might be some downtime. Just wanted to give everyone a heads up in case anyone was planning to do any testing or anything like that. Feel free to reach out if you have any questions or concerns!
```

**After:**

```
**Staging maintenance:** Saturday 2am-6am UTC

Impact: Staging environment unavailable. Production unaffected.

Plan testing accordingly. Questions → #infra-support
```

### Asking for Help

**Before:**

```
Has anyone ever run into an issue where the build fails on CI but works locally? I've been trying to figure this out for a while and I'm not really sure what's going on. I think it might be something with the environment variables but I'm not 100% sure. Any ideas would be really appreciated!
```

**After:**

```
Build fails on CI, passes locally. Suspect env vars.

**Error:** `REDIS_URL undefined` at `src/cache.ts:12`
**Tried:** Verified secrets in GitHub settings, cleared CI cache
**Repo:** `app-service`, branch `feature/caching`

Anyone seen this before?
```

## Documentation Revisions

### Process Documentation

**Before:**

```
This document describes the process for deploying new versions of the application to production. It's important to follow these steps carefully to ensure that everything goes smoothly. Before you begin, you'll want to make sure that you have all the necessary permissions and that you've reviewed the changes that are going to be deployed. The deployment process involves several steps that need to be completed in order.
```

**After:**

```
# Production Deployment

**Prerequisites:**
- `deploy` role in AWS
- PR approved and merged to `main`
- All CI checks passing

**Steps:**
1. Run `./scripts/deploy.sh production`
2. Monitor Datadog dashboard for 10 minutes
3. If errors spike, run `./scripts/rollback.sh`

**Rollback:** Automatic if health check fails. Manual via `rollback.sh` otherwise.
```

## Common Filler Phrases to Cut

| Filler                       | Replacement                     |
| ---------------------------- | ------------------------------- |
| "I just wanted to..."        | [Delete, start with the point]  |
| "I think maybe we should..." | "We should..." or "Consider..." |
| "It would be great if..."    | [State the ask directly]        |
| "I was wondering if..."      | [Ask the question directly]     |
| "Just a quick..."            | [Delete]                        |
| "Basically..."               | [Delete]                        |
| "Actually..."                | [Delete unless contrasting]     |
| "In order to..."             | "To..."                         |
| "At this point in time"      | "Now"                           |
| "Due to the fact that"       | "Because"                       |
| "In the event that"          | "If"                            |
| "Prior to"                   | "Before"                        |
| "Subsequent to"              | "After"                         |
| "With regard to"             | "About" or "On"                 |

## Restructuring Long Messages

For messages over 3 paragraphs:

1. **Extract the core ask/point** → Make it the first line
2. **Group related details** → Use headers or bold labels
3. **Convert lists in prose** → Use actual bullet points
4. **Move context to the end** → Or link to a doc
5. **Add explicit next steps** → Who, what, when

## When NOT to Revise

Preserve original voice and length when:

- Personal/emotional messages where warmth matters
- Creative writing where style is intentional
- Formal documents with required language (legal, compliance)
- The author explicitly wants verbose/formal tone
