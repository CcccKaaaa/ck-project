
## Two Lists

Here are two lists. The reason this is interpreted as such is that the first 
one has two items. The empty line that follows item B terminates the list and
indicates that the next one is actually a second one.

- Item A
  - Subitem AA
  - Subitem AB
- Item B

- Item A
  - Subitem AA
  - Subitem AB


## Two Lists?

On the surface, this looks like two lists. However, the empty line after 
subitem AB indicates that subitems AA and AB make up a broken off paragraph 
within the a single list, made up of items A and B and their subitems.

Surrounding empty lines is the syntax of these sorts of paragraphs within lists.
This is why prettier inserts the empty line after item A.
The reason item B doesn't receive that treatment is because it's the last item
in the list, meaning that the empty line after it doesn't indicate a broken
off paragraph.


- Item A
  - Subitem AA
  - Subitem AB

- Item B
  - Subitem BA
  - Subitem BB
  
This becomes more obvious when adding another List item. Below, new lines
appear for both items A and B.

- Item A
  - Subitem AA
  - Subitem AB

- Item B
  - Subitem BA
  - Subitem BB

- Item C
  - Subitem CA
  - Subitem CB
  
## Why?

The reason this happens likely is that lists conceptually contain multiple
items, making the this a reasonable and consisten interpretation by Prettier.
Rather than writing multiple single-item lists, it would technically be more
consistent to use headings rather than top-level list items, e.g.:

### List A

- Item A
- Item B

### List B

- Item A
- Item B

### List C

- Item A
- Item B




```

**Output:**
```markdown
## Two Lists

Here are two lists. The reason this is interpreted as such is that the first
one has two items. The empty line that follows item B terminates the list and
indicates that the next one is actually a second one.

- Item A
  - Subitem AA
  - Subitem AB
- Item B

- Item A
  - Subitem AA
  - Subitem AB

## Two Lists?

On the surface, this looks like two lists. However, the empty line after
subitem AB indicates that subitems AA and AB make up a broken off paragraph
within the a single list, made up of items A and B and their subitems.

Surrounding empty lines is the syntax of these sorts of paragraphs within lists.
This is why prettier inserts the empty line after item A.
The reason item B doesn't receive that treatment is because it's the last item
in the list, meaning that the empty line after it doesn't indicate a broken
off paragraph.

- Item A

  - Subitem AA
  - Subitem AB

- Item B
  - Subitem BA
  - Subitem BB

This becomes more obvious when adding another List item. Below, new lines
appear for both items A and B.

- Item A

  - Subitem AA
  - Subitem AB

- Item B

  - Subitem BA
  - Subitem BB

- Item C
  - Subitem CA
  - Subitem CB

## Why?

The reason this happens likely is that lists conceptually contain multiple
items, making the this a reasonable and consisten interpretation by Prettier.
Rather than writing multiple single-item lists, it would technically be more
consistent to use headings rather than top-level list items, e.g.:

### List A

- Item A
- Item B

### List B

- Item A
- Item B

### List C

- Item A
- Item B

```