# Key Learnings

## Learning in Public

We encourage everyone to share what they learned throughout this project. This is called "learning in public".

### Why learn in public?

- Accountability: Sharing progress helps keep momentum and commitment high.
- Feedback: The community can point out mistakes, better approaches, and new ideas.
- Networking: Public posts help connect with others working on similar problems.
- Documentation: Your notes and updates become a useful record of your learning journey.
- Opportunities: Employers and collaborators often notice people who document their work clearly.

### Key lessons from this project

- Building a working RAG pipeline starts with understanding the data source and its structure.
- Search quality matters as much as model quality; retrieval improves answer usefulness.
- Good prompts and clear instructions help the model stay grounded in the retrieved context.
- Cleaning and organizing code early reduces confusion and makes the project easier to reuse.
- Notebooks are useful for experiments, but reusable logic should live in well-structured Python modules.
- Environment variables and secrets should never be hardcoded into code or notebooks.
- Documentation is part of the project: clear README instructions help others run and understand the work.

### Common pitfalls

- Hardcoding API keys or other credentials inside notebooks or scripts.
- Forgetting to validate the data schema before building the index.
- Relying only on the LLM without checking retrieval results.
- Mixing exploration code with production-ready logic.
- Not adding enough context to prompts, which can lead to weak or generic answers.
- Leaving generated artifacts, caches, or local databases untracked in the repo.

### Example post for LinkedIn

```
🚀 Finished building a small RAG project for the LLM Zoomcamp FAQ!

What I learned:
✅ How to fetch and structure FAQ data
✅ How to build a search index for relevant retrieval
✅ How to use prompt templates to ground answers
✅ How to keep code cleaner and easier to reuse

One important takeaway: retrieval quality strongly affects the final answer quality.

I’m also learning the value of documenting the process and sharing progress publicly.

Following the amazing work by @Alexey Grigorev and the @DataTalksClub community.
```
