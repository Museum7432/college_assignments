function bresenham_quater(self, x0, y0, x1, y1, rgba, swap_axis = false) {
    let dx = x1 - x0
    let dy = y1 - y0

    let y_step = 1
    if (dy < 0){
        y_step = -1
    }

    dx = Math.abs(dx)
    dy = Math.abs(dy)

    // (Math.abs(dy) <= Math.abs(dx) && x0 < x)

    let p = 2 * dy - dx
    let y = y0

    for (let x = x0; x <= x1 + 1; x++) {
        if (swap_axis) {
            self.setPixel(y, x, rgba)

        } else {
            self.setPixel(x, y, rgba)
        }

        if (x == x1 + 1) return

        if (p < 0) {
            p += 2 * dy
        } else {
            p += 2 * dy - 2 * dx
            y += y_step
        }
    }
}

function bresenham(x0, y0, x1, y1, rgba) {
    let dx = x1 - x0
    let dy = y1 - y0

    if (dx == 0 || dy == 0) {
        return
    }

    if (Math.abs(dy) <= Math.abs(dx)) {
        if (x0 < x1) bresenham_quater(this, x0, y0, x1, y1, rgba)
        else bresenham_quater(this, x1, y1, x0, y0, rgba)

    } else {
        if (y0 < y1) bresenham_quater(this, y0, x0, y1, x1, rgba, true)
        else bresenham_quater(this, y1, x1, y0, x0, rgba, true)
    }

}

export default bresenham = bresenham