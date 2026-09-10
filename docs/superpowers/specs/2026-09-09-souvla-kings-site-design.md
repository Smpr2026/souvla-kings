# Souvla Kings site: design spec (2026-09-09)

## Brief
George asked for a "full animated, crazy website" for Souvla Kings with smoke flowing through the page or something rotating, using their Instagram and Facebook for direction. Built autonomously; all product facts below come from their public posts.

## Facts gathered (public posts)
- Business: Souvla Kings, Sydney. Facebook category "Outdoor and sporting goods company". Phone 0429 543 435 (Facebook intro, 2026). An older 2020 Instagram post lists 0429 543 434.
- Product: 100% stainless steel hooded souvla, 30 kg motor with speed controller, 3 long skewers, 11 shorter skewers, grilling plates. "FREE Australia wide shipping ONLY $749 DELIVERED".
- Instagram highlights: "Triple Mega", "$1099 Delivered", "$849 Delivered". No kit lists found for the $849 and $1099 tiers.
- Dec 2020 commercial unit: $1,599, 1,500 mm wide, 100 kg motor, 1.5 mm stainless, three 6.5 mm stainless grills, built-in thermometer, large lockable wheels, fully adjustable.
- Recent posts: Father's Day sale with free delivery and assembly; collaboration with Dulwich Hill Gourmet Meats; "Testing our new Mega Souvla" video.
- TikTok @souvla_king line: "Nothing will ever compare to an original Cypriot Souvla."

## Design plan
- Scene: Saturday dusk in a Sydney backyard, coals gone to orange glow, motor humming, three spits turning, smoke over the fence. Dark ground with ember light, single-theme.
- Colour (OKLCH): ground olive-charcoal 0.15/0.016/110; surface 0.19; ink steel-white 0.96; olive 0.70/0.11/112 for labels and links; ember 0.74/0.19/52 for CTAs and glow; stainless greys for the machine.
- Type: Alfa Slab One (display, prices), Barlow (body), Barlow Condensed (labels, marquee, specs).
- Layout: poster hero (headline + lede above a full-width canvas scene), marquee ribbon, lineup as a workshop order sheet (rows, not cards), anatomy diagram with numbered parts key, three-step Cypriot method, delivery stamp, socials, phone footer.

## Motion
- Fixed full-page smoke canvas above the content: sprite particles rising from the bottom of the viewport and from the hero coal bed, pushed by the cursor, dragged by scroll so smoke flows through every section.
- Hero canvas: three skewers of lamb rotating (facet shading rolls around each chunk), flickering coals, ambient ember glow, sparks, fat drips that flare and puff smoke, chain-and-sprocket drive, hood reflection. Speed controller slider sets rpm live; "Throw on coals" boosts glow, sparks and smoke.
- Lineup rows each carry a small spinning spit canvas; hover speeds it up.
- Rotating text stamp in the hero, CSS marquee ribbon, headline word rise on load, parts pins pop in on scroll.
- prefers-reduced-motion: single still frame of scene and smoke, no marquee or stamp rotation.

## Open items for George
- Kit lists and names for the $849 and $1099 tiers, and the Triple Mega price.
- Whether the $1,599 commercial spec and price are still current.
- Confirm the phone number (0429 543 435 vs 0429 543 434).
- Real photos or video from Instagram to replace or sit beside the drawn scene once assets are supplied.
