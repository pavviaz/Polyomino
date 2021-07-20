# Polyomino
Polyomino solver using SAT

## Launching

### Preprocess
For launching you need:
- numpy
- matplotlib
- more-itertools
- ortools (https://developers.google.com/optimization)

Use 
```bash
pip install <moduleName>
```
for installing all necessary stuff.

Then use 
```bash
python main.py
```
for launch prog

### Configure problem

There are two ways how to define problem (field size, count and shapes of polyominos):
- console input (branch: with_console_input)
- JSON configuration file (branch: with_json_parser - default)
    - field
    - rectPolyomino for rectangle polyominos
    - lPolyomino for L-polyominos
    - width, height for sizes
    - capacity for capacity of the polyomino (how many times it should be used in a solution)

Example of JSON-configuration file:
```ruby
{
  "field": {
    "width": 5,
    "height": 5
  },
  "rectPolyomino": [
    {
      "width": 2,
      "height": 3,
      "capacity": 1
    },
    {
      "width": 1,
      "height": 3,
      "capacity": 1
    }
  ],
  "lPolyomino": [
    {
      "width": 3,
      "height": 5,
      "capacity": 1
    },
    {
      "width": 2,
      "height": 4,
      "capacity": 1
    },
    {
      "width": 2,
      "height": 3,
      "capacity": 1
    }
  ]
}
```
It shows possible decision if it exists and nothing if it's not.

![image](https://user-images.githubusercontent.com/57394771/126393713-9b749ccf-907a-4eb0-8fb1-f0e5708a92a0.png)

## Algorythm

I use SAT solver by Google OR-tools tool.

I designed polyomino problem solver with rectangle and L-polyominos of different sizes (with rotations).

I use int variables to encode (x, y) coordinates of each cell for every polyomino. Also I use boolean variables to encode which shape (rotation) of polyomino is used.

So I have:

W - field width

H - field height


pCount - polyominos count

p_i_shapes_count - count of possible shapes of the p_i

p_i_cells_count - count of cells which polyomino should fill

So for each p_i (where i in range(0, pCount)) I have:
- p_i_shapes_count of Boolean Variables to encode which one is used
- 2 * p_i_cells_count of Int Variables to encode (x, y) coordinates of every polyomino cell

Also there are some contraints:
1. Rules for relative location for every cell of every polyomino shape
2. Rules for shape uniqueness for each polyomino
3. Rules for ensure that all polyominos are used

Then we have a SAT problem determining if there exists an interpretation that satisfies a given Boolean formula. It's a NP-Complete problem.
