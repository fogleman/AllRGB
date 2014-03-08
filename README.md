## AllRGB

Efficiently create AllRGB images that target an input image. The input must be 4096x4096px. The output will also be 4096x4096px and will contain all 16,777,216 distinct RGB values once and only once.

An octree is used to spatially represent the RGB colors. The octree is only 9 levels deep from root to leaves. Each node in the octree stores a count for how many colors in its subtree are still available to be used. To find a color in the octree, use a single bit from each of R, G and B to form a 3-bit number representing the next child node to visit. Repeat this process from the most significant to the least significant bits.

For example, if RGB = (27, 89, 233)...

       12345678
    R: 00011011
    G: 01011001
    B: 11101001
    
    001, 011, 001, 110, 111, 000, 100, 111 => 1, 3, 1, 6, 7, 0, 4, 7

When encountering a node with a value of zero (meaning no colors are available in that space), visit a different child instead to find as similar of a color as possible.

If some areas of the image are more important than others, such as a face, let those pixels pick their colors first - give them priority. The pixels in the sample shown below were simply ordered randomly.

See http://allrgb.com/ for details on the concept.

![Screenshot](http://i.imgur.com/gQuJo83.jpg)
