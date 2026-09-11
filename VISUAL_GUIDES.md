# Checklist image guides

Every check has an image button beside its bullet toggle. The viewer keeps the original inspection script separate from the visual aid. Pictures load on demand and can be enlarged; numbered overlays can be hidden.

The catalog covers 139 stable check IDs. It reuses 30 photographs and 15 original SVG component diagrams instead of baking a separate bitmap for every check. 82 checks include a photo view. The other 57 use diagrams or procedural illustrations because the relevant parts were not clearly photographed. Some checks offer both a photo and a diagram. Diagram views are explicitly identified as illustrative, not the actual vehicle layout; obscured or uncertain photo areas are described in the viewer caption.

## Files

- `assets/photos/`: optimized, auto-oriented WebP copies of all 30 supplied project photos. Original files in the user's local `Photos/` folder are untouched. EXIF metadata is stripped from the published copies.
- `assets/diagrams/`: reusable component illustrations, authored as SVG.
- `scripts/build-visual-guides.py`: reviewed photo coordinates, diagram artwork, and explicit check-to-view mappings. Coordinates are percentages of the normalized image. `tx`/`ty` optionally place the arrow tip on a specific surface instead of the bounding-box center.
- `assets/visual-guides.js`: generated catalog used by the page.
- `assets/visual-viewer.js`: shared, accessible image dialog and overlay renderer.

Regenerate the catalog and diagrams with `python scripts/build-visual-guides.py` (requires Pillow). Committed WebP images are sufficient; originals are not required. Run `npm ci` followed by `npm test` for the interaction and asset-coverage checks.

## Review and references

All 30 source photographs were reviewed individually. Rendered overlay previews were reviewed across the check mappings. Photo pointers identify visible components or explicitly described location references. The photographed trailer shows leaf springs; checks for air bags/control arms use separate illustrative diagrams.

The brake actuator/drum schematic represents the chamber–pushrod–slack-adjuster–cam relationship described in [Bendix SD-05-1200](https://www.bendixvrc.com/itemDisplay.asp?documentID=7563). It is a simplified original illustration, not a reproduction of a manufacturer drawing. [Freightliner driver manuals](https://www.freightliner.com/parts/driver-maintenance-manuals/) provide vehicle-specific reference material. The diagrams add no test limits or replacement inspection instructions.

Automated verification exercises all 139 image buttons, checks asset and marker coverage, and covers alternate views, pointer visibility, zoom, keyboard navigation, focus return, load errors, bullet icons, notes/export, search, progress, and the section accordion. The connected browser was unavailable for live layout testing during this change; rendered SVG previews and DOM interaction checks were used.
