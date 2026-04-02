# Contributing to Discord Archiver

Thanks for wanting to contribute! Here is everything you need to know.

---

## Ways to Contribute

You don't have to write code to contribute:

- ⭐ **Star the repo** — helps others find the project
- 🐛 **Report bugs** — [open a bug report](https://github.com/TanaTTV/Discord-Archiver/issues/new/choose)
- 💡 **Suggest features** — [open a feature request](https://github.com/TanaTTV/Discord-Archiver/issues/new/choose)
- 💬 **Help others** — answer questions in [Discussions](https://github.com/TanaTTV/Discord-Archiver/discussions)
- 📖 **Improve docs** — fix typos, clarify instructions, add examples
- 🧑‍💻 **Submit code** — pick an open issue and build it

---

## Before You Start Coding

1. Check the [open issues](https://github.com/TanaTTV/Discord-Archiver/issues) to see if someone is already working on it
2. For large changes, open an issue or discussion first so we can align before you invest time
3. Check the [milestones](https://github.com/TanaTTV/Discord-Archiver/milestones) to understand what is planned for each version

---

## Setting Up Locally

```bash
git clone https://github.com/TanaTTV/Discord-Archiver.git
cd Discord-Archiver
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open `http://localhost:5000` to verify it works.

---

## Making Changes

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test locally — run the app and verify your change works end to end
5. Commit: `git commit -m "Add: short description of what you did"`
6. Push: `git push origin feature/your-feature-name`
7. Open a Pull Request against `main`

---

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Fill out the PR template fully
- Make sure the app still runs without errors after your change
- Update the README if you are adding or changing a feature users interact with
- Do not commit `.env` files, bot tokens, or any credentials

---

## Important Rules

- **Discord ToS compliance** — all contributions must stay within Discord's Terms of Service. Do not add features designed to evade rate limits, bypass permissions, or mass-scrape servers
- **Privacy first** — do not add anything that sends user data, bot tokens, or messages to external servers
- **Localhost only** — the app is designed to run locally. Do not add cloud integrations that could expose user data

---

## Code Style

- Python: follow PEP 8, use descriptive variable names, avoid bare `except:` clauses
- Log errors with `log.warning()` or `log.error()` rather than silently passing
- Keep new dependencies minimal — if it can be done with the standard library, do that

---

## Questions?

Head to [Discussions](https://github.com/TanaTTV/Discord-Archiver/discussions) — happy to help.
