# 囧 JiongTu
Takes a list of images formated as lists of pixels `(x_offset, y_offset, R, G, B)`
and render them in an HTML canvas on a local server.

`(0, 0, 255, 0, 0)` A red point on the top left.
## Setup
`pip install jiongtu`

Depends on `Flask`
## Example
    import jiongtu.jiongtu as j
    images = [[(i, i, 0, 0, 255)] for i in range(100)]
    j.start(images)

go to [http://localhost:5000/](http://localhost:5000/) enjoy
