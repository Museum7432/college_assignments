function daa(self, x0, y0, x1, y1, rgba) {
    let dx = x1 - x0
    let dy = y1 - y0
    if (dx == 0 || dy == 0) {
        return
    }

    if (Math.abs(dy) <= Math.abs(dx)) {
        if (x1 < x0) {
            // swap two points
            let t = x0; x0 = x1; x1 = t
            t = y0; y0 = y1; y1 = t
        }

        let k = dy / dx
        let y = y0

        for (let x = x0; x <= x1; x++) {
            self.setPixel(x, Math.floor(y + 0.5), rgba)
            y = y + k
        }
    }
    else {
        if (y1 < y0) {
            // swap two points
            let t = x0; x0 = x1; x1 = t
            t = y0; y0 = y1; y1 = t
        }

        let k = dx / dy
        let x = x0

        for (let y = y0; y <= y1; y++) {
            self.setPixel(Math.floor(x + 0.5), y, rgba)
            x = x + k
        }
    }
}
export default daa