function draw_mirrored_points(self, x, y, xC, yC, rgba) {
    self.setPixel(xC + x, yC + y, rgba)
    self.setPixel(xC + x, yC - y, rgba)
    self.setPixel(xC - x, yC + y, rgba)
    self.setPixel(xC - x, yC - y, rgba)

    self.setPixel(xC + y, yC + x, rgba)
    self.setPixel(xC + y, yC - x, rgba)
    self.setPixel(xC - y, yC + x, rgba)
    self.setPixel(xC - y, yC - x, rgba)

}

function midpoint(xC, yC, R, rgba) {
    let x = 0, y = R, f = 1 - R
    draw_mirrored_points(this, x, y, xC, yC, rgba)

    while (x < y) {
        if (f < 0) {
            f += 2 * x + 3
        } else {
            f += 2 * x - 2 * y + 5
            y--
        }
        x++
        draw_mirrored_points(this, x, y, xC, yC, rgba)
    }
}

export default midpoint;