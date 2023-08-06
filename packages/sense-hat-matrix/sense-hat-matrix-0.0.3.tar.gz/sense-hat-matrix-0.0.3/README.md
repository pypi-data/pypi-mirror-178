# sense-hat-matrix
## Usage
```python
from sense_hat import SenseHat
from Graph import Graph

min_temp = 20
max_temp = 24
sense    = SenseHat()
temp     = sense.get_temperature()
g        = Graph(min_temp, max_temp)
pixels   = g.render(temp)
sense.set_pixels(pixels)
```

## Dev
### Install project
   * `pip3 install -e . `

### Release new version
[Create new release with new `tag` on `github`](https://github.com/szigyi/sense-hat-matrix/releases/new)

