## AllRGB

Efficiently create AllRGB images that target an input image. The input must be 4096x4096px. The output will also be 4096x4096px and will contain all 16,777,216 distinct RGB values once and only once.

### Usage

    python main.py input.png

The output will be stored in output.png. The program takes 2 - 3 minutes to run (longer if the C module is not compiled and the pure Python module is used instead).

### Sample

![Screenshot](http://i.imgur.com/gQuJo83.jpg)

### Algorithm

An octree is used to spatially represent the RGB colors. The octree is only 9 levels deep from root to leaf (inclusive). Each node in the octree stores a count for how many colors in its subtree are still available to be used. The octree is stored in a flat array, as it is a complete octree. Children indexes are computed as:

    8 * i + 1 + x

...where `i` is the current index and `x` specifies the xth (0 - 7) child. To find a color in the octree, use a single bit from each of R, G and B to form a 3-bit number representing the next child node to visit. Repeat this process from the most significant to the least significant bits.

For example, if RGB = (27, 89, 233)...

       12345678
    R: 00011011
    G: 01011001
    B: 11101001
    
    001, 011, 001, 110, 111, 000, 100, 111 => 1, 3, 1, 6, 7, 0, 4, 7

When encountering a node with a value of zero (meaning no colors are available in that space), visit a different child instead to find as similar of a color as possible. But don't just pick a random other child, pick one that will minimize error, especially in the green channel. A lookup table is used for this purpose.

    LOOKUP = [
        [0, 1, 4, 5, 2, 3, 6, 7],
        [1, 0, 5, 4, 3, 2, 7, 6],
        [2, 3, 6, 7, 0, 1, 4, 5],
        [3, 2, 7, 6, 1, 0, 5, 4],
        [4, 5, 0, 1, 6, 7, 2, 3],
        [5, 4, 1, 0, 7, 6, 3, 2],
        [6, 7, 2, 3, 4, 5, 0, 1],
        [7, 6, 3, 2, 5, 4, 1, 0],
    ]

Optionally, if some areas of the image are more important than others, such as a face, let those pixels pick their colors first - give them priority. This was not done in the sample image. The pixels in the sample were simply ordered randomly.

See http://allrgb.com/ for details on the concept.
