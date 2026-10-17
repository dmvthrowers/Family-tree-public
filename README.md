# Lowe & Rogers Family Tree: public splash page

The public face of the family tree. The tree itself is private and will be shared with family behind a sign-in (coming soon).

This repo publishes one page (`site/`) with:

- **The tree in numbers:** counts of people, families, generations and surnames, plus births by country and century. No person's name, dates, places or story.
- **Already on the public record:** a few relatives whose stories others have already published (a military citation, a line-of-duty memorial, an encyclopedia article). The page shows only a name, one line and links to those outside sources. They're listed in `highlights.json`, each with the date it was checked.
- **For family:** how to ask for access.

## Rules

- **Nothing from the private tree is copied here.** The counts are built from the private repo and arrive as finished HTML.
- **A highlight needs a public source that someone else published,** and that source has to be checked by hand: a page that opens publicly and is about this person. Sources that can't be checked, such as sites that block automated access, are left out.
- **No living person** is ever listed.
- **No scripts, no trackers, nothing loaded from other servers.** `check_site.py` enforces this, and the publish workflow runs it before every deploy.

## Updating

The page is built by `site/build.py --splash` in the family-tree code, from counts the private repo produces:

```bash
FAMILY_TREE_URL=https://dmvthrowers.club/Family-tree-public/ \
FAMILY_TREE_HIGHLIGHTS=../family-tree-public/highlights.json \
FAMILY_TREE_CONTACT=Brandon.james.rogers@outlook.com \
python site/build.py --splash site/splash-stats.json ../family-tree-public/site
python3 ../family-tree-public/check_site.py
```

When the family sign-in is live, add `FAMILY_TREE_LOGIN_URL=https://...` to show a sign-in button in place of "coming soon".
