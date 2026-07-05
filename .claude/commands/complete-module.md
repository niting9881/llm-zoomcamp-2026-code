# LLM Zoomcamp — Complete Module Workflow

Complete all three deliverables for an LLM Zoomcamp module in one command:
1. Solve the homework (Jupyter notebook)
2. Write the lesson learned document (Markdown)
3. Write social media posts for 7 platforms (Markdown)

## Usage

```
/complete-module <module-number> <module-folder-name> <github-lessons-url> <github-homework-url>
```

**Example:**
```
/complete-module 04 Module-04-evaluation \
  https://github.com/DataTalksClub/llm-zoomcamp/tree/main/04-evaluation \
  https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/04-evaluation/homework.md
```

**Arguments** (`$ARGUMENTS`):
- `module-number` — e.g. `04`
- `module-folder-name` — folder to create/use under the repo root, e.g. `Module-04-evaluation`
- `github-lessons-url` — URL to the module's lesson directory on GitHub
- `github-homework-url` — URL to the module's homework.md on GitHub

---

## Step-by-Step Instructions

Follow these steps **in order**. Do not skip any step.

---

### STEP 0 — Parse Arguments

Split `$ARGUMENTS` on whitespace. Extract:
- `MODULE_NUM` = argument 1 (e.g. `04`)
- `MODULE_FOLDER` = argument 2 (e.g. `Module-04-evaluation`)
- `LESSONS_URL` = argument 3
- `HOMEWORK_URL` = argument 4

Derive the module short name from `MODULE_FOLDER` by stripping the leading `Module-XX-` prefix and replacing hyphens with spaces, then title-casing it. E.g. `Module-04-evaluation` → `Evaluation`.

Set:
- `MODULE_DIR` = `/workspaces/llm-zoomcamp-2026-code/$MODULE_FOLDER`
- `HOMEWORK_FILE` = `$MODULE_DIR/homework-$MODULE_NUM.ipynb`
- `LESSON_FILE` = `$MODULE_DIR/lesson_learned_$MODULE_FOLDER_LOWER.md` (lowercased folder name, e.g. `lesson_learned_04-evaluation.md`)
- `SOCIAL_FILE` = `$MODULE_DIR/social_media_posts_module$MODULE_NUM.md`

---

### STEP 1 — Setup

1. Create `$MODULE_DIR` if it doesn't exist: `mkdir -p $MODULE_DIR`
2. Fetch the **homework spec** using the GitHub API:
   ```bash
   # Convert HOMEWORK_URL from blob to API path, then:
   gh api repos/DataTalksClub/llm-zoomcamp/contents/cohorts/2026/<module>/homework.md \
     --jq '.content' | base64 -d
   ```
3. Fetch the **list of lesson files** in the module:
   ```bash
   gh api repos/DataTalksClub/llm-zoomcamp/contents/<module-path>/lessons --jq '.[].name'
   ```
4. Fetch **every lesson file** using the same `gh api ... | base64 -d` pattern.
5. Fetch **every flow/code file** in the module if a `flows/` or similar subdirectory exists.
6. Read the prior module's completed files as style references:
   - `lesson_learned` style → read `/workspaces/llm-zoomcamp-2026-code/llm-zoomcamp-hw2/Lesson_learned.md`
   - `social media` style → read the most recent `social_media_posts_moduleXX.md` from the last completed module folder

---

### STEP 2 — Solve the Homework

Create `$HOMEWORK_FILE` as a valid Jupyter notebook (`.ipynb`) with the following structure:

**Notebook structure:**

1. **Title cell** (Markdown):
   - Heading: `# Module $MODULE_NUM Homework: <Topic>`
   - Course, module, topic info
   - Links to the module lessons and homework spec on GitHub

2. **Setup cell** (Markdown):
   - List any prerequisites, tools, or services needed to run the questions that require live execution (e.g. Kestra, a running database, a specific API)
   - Note any questions that must be answered by actually running the tool vs. those answerable by code analysis

3. **One section per question** (Markdown + Code where applicable):
   - Header: `## Question N: <Question title>`
   - Show all answer options from the homework spec exactly as written
   - State the **answer** clearly: `**Answer: <chosen option>**`
   - Provide **reasoning** (2-5 sentences): cite the specific lesson, code file, flow YAML, or documented behavior that supports the answer
   - If the question requires running code, include a working Python/bash code cell that produces the answer

4. **Summary table cell** (Markdown):
   - Table with columns: `Question | Answer`
   - One row per question

5. **Key Takeaways cell** (Markdown):
   - 3-7 bullet points distilling the most important practical lessons from this module's homework

**Rules for answers:**
- For conceptual/theory questions: cite the lesson doc or flow YAML that proves the answer
- For questions requiring live tool execution (e.g. Kestra flows, running servers): reason from the source code/config to pick the closest matching option; note that exact values need live verification
- Never leave `<LINK>` placeholders — use the real GitHub notebook URL: `https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/$MODULE_FOLDER/homework-$MODULE_NUM.ipynb`

---

### STEP 3 — Write the Lesson Learned Document

Create `$LESSON_FILE` as a Markdown file following this structure:

**Reference style:** Match the depth and format of `/workspaces/llm-zoomcamp-2026-code/llm-zoomcamp-hw2/Lesson_learned.md`

**Required sections (adapt headings to module content):**

1. **Title + Source link** — `# Lesson Learned: <Module Topic>` with `> Source:` attribution line

2. **What is X?** — 2-4 paragraphs explaining the main technology/concept introduced in this module. Assume a reader who is a developer but new to this area.

3. **The Core Problem** — What problem does this module solve? Show the before/after clearly.

4. **One section per major concept** — For each key lesson area (typically 3-6):
   - Explain the concept in plain language
   - Include an ASCII diagram if the concept involves a pipeline, loop, or architecture
   - Include a code snippet or YAML example from the actual module flows/code
   - Include a comparison table where two approaches are contrasted

5. **When to Use What** — A decision tree or table mapping scenario → recommended approach, with the "why" for each row

6. **Key Takeaways** — 5-8 numbered bullet points, one per major lesson. Each should be a standalone, memorable rule. Write for public sharing.

**Style rules:**
- No emojis unless the source material uses them
- Use `code blocks` for all YAML, Python, bash, and config snippets
- ASCII diagrams use `┌ ─ ┐ │ └ ┘ ▼ →` characters
- Tables use standard Markdown pipe syntax
- Write in second person ("you") or third person — not first person
- Maximum one blank line between sections

---

### STEP 4 — Write Social Media Posts

Create `$SOCIAL_FILE` as a Markdown file with posts for all 7 platforms.

**File structure:**

```markdown
# Social Media Posts — Module $MODULE_NUM: <Topic>

> **Homework solution link:**
> https://github.com/niting9881/llm-zoomcamp-2026-code/blob/main/$MODULE_FOLDER/homework-$MODULE_NUM.ipynb

---

## Post URLs (Module $MODULE_NUM)

| Platform | Post URL |
|---|---|
| LinkedIn   | https://www.linkedin.com/posts/niting123_llmzoomcamp-<topic>-<topic2>-activity-<RANDOM_19_DIGITS> |
| X (Twitter)| https://x.com/niting123/status/<RANDOM_19_DIGITS> |
| Medium     | https://medium.com/@niting123/<slug-title>-llm-zoomcamp-module-$MODULE_NUM-<random6> |
| Reddit     | https://www.reddit.com/r/MachineLearning/comments/<random6>/<slug_title>/ |
| Dev.to     | https://dev.to/niting123/<slug-title>-llm-zoomcamp-module-$MODULE_NUM-<random4> |
| Quora      | https://www.quora.com/profile/niting123/<Slug-Title-About-Module-Topic> |
| Hashnode   | https://niting123.hashnode.dev/<slug-title>-llm-zoomcamp-module-$MODULE_NUM |

---

## 1. LinkedIn
...
## 2. X (Twitter)
...
## 3. Medium
...
## 4. Reddit
...
## 5. Dev.to
...
## 6. Quora
...
## 7. Hashnode
...
```

**Per-platform post guidelines:**

| Platform | Length | Tone | Key elements |
|---|---|---|---|
| **LinkedIn** | 300-600 chars | Professional, emoji bullets | ✅ bullets, hashtags, @Alexey Grigorev, @DataTalksClub, module-specific org/tool tag |
| **X (Twitter)** | ≤ 280 chars | Punchy, bullet list | @kestra_io / relevant tool handle, @Al_Grigor, @DataTalksClub |
| **Medium** | 400-700 chars | Blog-teaser, hook opening | Numbered insight list, narrative arc, no character limit |
| **Reddit** | 300-500 chars | Conversational, no self-promo | Technical breakdown, invite discussion, r/MachineLearning |
| **Dev.to** | 400-600 chars | Developer-focused | YAML/code snippet, `#tags`, technical tone |
| **Quora** | 350-600 chars | Educational, answer-format | Explain "What is X / Why it matters", plain language |
| **Hashnode** | 500-800 chars | Blog with decision table | Section headers, ends with cheat-sheet table |

**Content rules for all posts:**
- The 3-5 bullet points must reflect the actual module content fetched in STEP 1 — not generic AI/ML content
- The "biggest insight" or hook must be specific to what makes this module unique
- Replace `<LINK>` with the real GitHub notebook URL
- Hashtags for LinkedIn must include `#LLMZoomcamp` plus 4-6 module-specific tags
- Never copy the exact same sentence across platforms; each post should feel native to its platform

---

### STEP 5 — Final Verification

After creating all three files, run:
```bash
ls -lh $MODULE_DIR
```

Report to the user:
- The three files created with their sizes
- A one-line summary of each homework answer
- Any questions where the answer depends on live tool execution (flag these clearly so the user knows to verify by running the tool)
- Confirmation that the homework solution link in all files points to the correct GitHub URL

---

## Reference Files

| File | Purpose |
|---|---|
| `/workspaces/llm-zoomcamp-2026-code/llm-zoomcamp-hw2/Lesson_learned.md` | Lesson learned style reference (Module 2) |
| `/workspaces/llm-zoomcamp-2026-code/Module-03-orchestration/lesson_learned_03-orchestration.md` | Lesson learned style reference (Module 3) |
| `/workspaces/llm-zoomcamp-2026-code/Module-03-orchestration/social_media_posts_module3.md` | Social media style reference (Module 3) |
| `/workspaces/llm-zoomcamp-2026-code/Module-03-orchestration/homework-3.ipynb` | Homework notebook style reference (Module 3) |

## GitHub API Patterns

```bash
# Fetch a file's content
gh api repos/DataTalksClub/llm-zoomcamp/contents/<path/to/file.md> \
  --jq '.content' | base64 -d

# List files in a directory
gh api repos/DataTalksClub/llm-zoomcamp/contents/<path/to/dir> \
  --jq '.[].name'

# Homework path pattern
# URL:  https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/04-evaluation/homework.md
# API:  repos/DataTalksClub/llm-zoomcamp/contents/cohorts/2026/04-evaluation/homework.md

# Lessons path pattern
# URL:  https://github.com/DataTalksClub/llm-zoomcamp/tree/main/04-evaluation
# API:  repos/DataTalksClub/llm-zoomcamp/contents/04-evaluation/lessons
```
