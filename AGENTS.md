---
type: Note
_organized: true
---

# AGENTS.md — Tolaria Vault

This is a [Tolaria](https://github.com/refactoringhq/tolaria) vault.

Keep this file focused on vault-specific conventions. For general Tolaria behavior, use the bundled Tolaria agent docs path provided by the app session context.

## Core conventions

- Notes are Markdown files.
- Use the first H1 as the note title. Tolaria uses this title in the note list, wikilinks, search, and other display surfaces.
- Store note type in the `type:` frontmatter field.
- Use wikilinks in body text and frontmatter fields to connect notes.
- Prefer types and relationships for organization. Folder structure is optional and should not be treated as the primary source of meaning.
- Tolaria reads notes recursively from all folders and stores new notes in the vault root by default.
- Saved views live in `views/*.yml`.
- Files in `attachments/` are assets, not notes. Reference them from notes, but do not treat them as notes or types.
- Frontmatter properties that start with `_` are usually Tolaria-managed state. Leave them alone unless the user explicitly asks for them to change.

## Notes

```yaml
---
type: Note
related_to: "[[tolaria]]"
status: Active
url: https://example.com
---

# Example note

Body content in Markdown.
```

## Types

Types are regular notes with `type: Type`. They define how notes of that type appear and which properties or relationships should be suggested for new notes.

```yaml
---
type: Type
_icon: rocket
_color: "#3b82f6"
_order: 0
_list_properties_display:
  - related_to
_sort: "property:onboarding:asc"
---

# Project
```

Empty properties and relationships in a type document become placeholders on new notes of that type. Values attached to properties in the type document become defaults for type instances.

Useful type metadata includes `icon`/`_icon`, `color`/`_color`, `order`/`_order`, `sidebar label`, `_list_properties_display`, `_sort`, `template`, `view`, and `visible`. When editing an existing file, preserve the key style already used there instead of mass-normalizing underscored keys.

## Relationships

Any frontmatter property whose value contains `[[wikilinks]]` is treated as a relationship. Common relationship keys include `related_to`, `belongs_to`, and `has`, but custom relationship names are valid too.

Preserve older relationship labels such as `Belongs to:` when editing existing notes that already use them.

Use quoted wikilinks for scalar frontmatter values and YAML lists for multi-value relationships.

## Wikilinks

- `[[filename]]` or `[[Note Title]]` for normal links
- `[[filename|display text]]` for custom display text
- Works in frontmatter values and Markdown body

## Views

Saved views live in `views/*.yml` and are written as YAML. Tolaria scans every `.yml` file in `views/`, and the filename is the stable view id, so use kebab-case filenames such as `active-projects.yml`.

A view definition looks like this:

```yaml
name: Active Projects
icon: null
color: null
sort: "property:onboarding:asc"
filters:
  any:
    - field: type
      op: equals
      value: Project
    - field: related_to
      op: contains
      value: "[[tolaria]]"
```

View rules that matter when creating or editing files:
- `name` is required. `icon`, `color`, and `sort` are optional.
- `sort` uses `option:direction`. Built-in options are `modified`, `created`, `title`, and `status`. Custom-property sorts use `property:<Property Name>`, for example `property:onboarding:asc`.
- `filters` must be a tree whose root is exactly one `all:` group or one `any:` group.
- Each filter condition uses `field`, `op`, and usually `value`.
- `field` can target built-ins like `type`, `status`, `title`, `favorite`, and `body`, plus actual frontmatter keys used in this vault such as `related_to`, `belongs_to`, or `url`.
- Supported operators are `equals`, `not_equals`, `contains`, `not_contains`, `any_of`, `none_of`, `is_empty`, `is_not_empty`, `before`, and `after`.
- `any_of` and `none_of` expect `value` to be a YAML list.
- `regex: true` is supported with `equals`, `not_equals`, `contains`, and `not_contains` when pattern matching is needed.
- Relationship filters can use wikilinks in `value`, for example `"[[tolaria]]"`.
- Do not create JSON view files or `.view.json` filenames.

## Filenames

Use kebab-case: `my-note-title.md`. One note per file.

## What agents should do

- Create and edit notes using the frontmatter and H1 conventions above.
- Create and edit type documents when the user asks for note categories or defaults.
- Add or modify relationships without breaking existing wikilinks.
- Create and edit saved views in `views/`.
- Update `AGENTS.md` only when the user asks for vault-level guidance changes.
- Search the bundled Tolaria docs when the user asks how Tolaria works or when you need product behavior beyond these base conventions.
- Use Portent as the default best-practice model when the user asks how to improve, organize, or restructure the knowledge base. Combine Portent's types, relationships, and capture -> organize -> archive lifecycle with Tolaria's type documents, properties, Inbox, archive, and saved views.

## What agents should avoid

- Do not infer note type or meaning from folders.
- Do not treat files in `attachments/` as notes, types, or view definitions.
- Do not silently overwrite an existing custom `AGENTS.md`.
- Do not rewrite installation-specific app configuration unless the user explicitly asks.
