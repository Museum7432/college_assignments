import daa from "./drawLine/daa.js"

class Painter {

    bgRgba = [240, 240, 200, 255]
    pointRgba = [0, 0, 255, 255]
    lineRgba = [0, 0, 0, 255]
    vlineRgba = [255, 0, 0, 255]

    constructor(canvas_id, width, height) {
        this.canvas_id = canvas_id
        this.width = width
        this.height = height


        let canvas = document.getElementById(canvas_id)
        canvas.setAttribute("width", width)
        canvas.setAttribute("height", height)

        this.context = canvas.getContext("2d")
        this.canvas = canvas

        // (y, x, 4)
        this.imageData = this.context.getImageData(0, 0, width, height);

        this.points = []
        this.now = [-1, -1]


    }

    getPixelIndex(x, y) {
        if (x < 0 || y < 0 || x >= this.width || y >= this.height) {
            return -1
        }
        return (y * this.width + x) << 2
    }

    setPixel(x, y, rgba) {
        let PixelIndex = this.getPixelIndex(x, y)
        if (PixelIndex == -1) return

        for (let i = 0; i < 4; i++) {
            this.imageData.data[PixelIndex + i] = rgba[i]
        }
    }

    drawPoint(x, y, rgba) {

        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                this.setPixel(x + i, y + j, rgba)
            }
        }
        this.context.putImageData(this.imageData, 0, 0);
    }

    drawLine(x0, y0, x1, y1, rgba) {
        daa(this, x0, y0, x1, y1, rgba)
    }

    getPosOnCanvas(x, y) {
        let bbox = this.canvas.getBoundingClientRect();
        return [
            Math.floor(x - bbox.left * (this.canvas.width / bbox.width) + 0.5),
            Math.floor(y - bbox.top * (this.canvas.height / bbox.height) + 0.5)
        ]
    }


}

export default Painter


