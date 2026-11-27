# Set ADT Simulator

A Python GUI application that simulates the **Set ADT** using a **hash table with linear probing** (table size 10). Built with `tkinter`; no Python built-in set operations are used.

## Features

- Two sets (**A** and **B**) that can be modified, plus a result set (**C**) for set operations
- Basic operations: **Add**, **Delete**, **Search**, **Display**
- Set operations: **Union**, **Intersection**, **Difference** (A ∪ B, A ∩ B, A − B)
- Live hash table visualization showing the index and contents of A, B and C
- Output log with colour-coded messages (green = success, red = error)
- Status bar showing the current set and the element count of A, B and C

## How to Use

1. Choose **Set A** or **Set B** under *Select Set to Modify*.
2. Type an integer in the **Element** box.
3. Click **Add**, **Delete** or **Search** (pressing `Enter` also adds).
4. Click **Union**, **Intersection** or **Difference** to compute the result into Set C.
5. Click **Display** to print the contents of A, B and C in the output area.
6. Use **Clear Output** to empty the log and **Exit** to close the app.

## How It Works

| Part | Description |
|------|-------------|
| `HashTable` | Fixed-size table (10 slots). Hash function is `value % 10`; collisions are resolved with **linear probing**. |
| `MySet` | Set wrapper around `HashTable` with `add`, `delete`, `contains`, `members`, `size`, `union`, `intersection`, `difference`. |
| `SetApp` | The tkinter GUI: layout, theme, event handling and table drawing. |

Notes on behaviour:

- **Duplicates** are rejected with a message.
- **Full table**: adding to a set with 10 elements is rejected. If a set operation result needs more than 10 slots (e.g. a large union), it fails with an error message.
- **Deletion** removes the element and re-inserts the following cluster of items so that later searches still work correctly.
- Only whole numbers are accepted; anything else highlights the input box in red.

## Example

| Index | A  | B     | C  |
|-------|----|-------|----|
| 0     | 10 | 50    | 10 |
| 1     | 20 | 60    | 20 |
| 2     | 30 | 30    | 30 |
| 3     | 40 | 40    | 40 |
| 4     | EMPTY | EMPTY | 50 |

```
SET A: {10, 20, 30, 40}
SET B: {30, 40, 50, 60}
SET C: {10, 20, 30, 40, 50, 60}   (Union)
```
