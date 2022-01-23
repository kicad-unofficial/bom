# Octopart BOM Generator

This plugin generates an Octopart compatible BOM file.

## Octopart Queries

Octopart's CSV format uses a "query" column to find components. This column is
generated from the (non-standard) `Octopart Query` field on each component.

Our [symbols library](https://github.com/kicad-unofficial/symbols) includes the
`Octopart Query` field wherever possible. However, be aware that components with
packing alternatives (reel vs tray, for example) are often listed separately on
Octopart, which is not accounted for.

If the component does not have an `Octopart Query` field, the built-in `Value`
field is used. A custom `Octopart Query` field can be added on a per-component
basis in the schematic editor.
