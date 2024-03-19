import daa from "./algorithms/daa.js"
import midpoint from "./algorithms/midpoint.js"
import bresenham from "./algorithms/bresenham.js"

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

        this.context = canvas.getContext("2d", { willReadFrequently: true })
        this.canvas = canvas

        // (y, x, 4)
        this.ImageData = this.context.getImageData(0, 0, this.width, this.height)

        this.points = []
        this.now = [-1, -1]

        this.daa = daa.bind(this)
        this.midpoint = midpoint.bind(this)
        this.bresenham = bresenham.bind(this)

        this.mode = "daa"
    }

    getImageData(DeepCopy = false) {
        if (DeepCopy) {
            return new ImageData(
                new Uint8ClampedArray(this.ImageData.data),
                this.ImageData.width,
                this.ImageData.height
            )
        }
        return this.context.getImageData(0, 0, this.width, this.height)
    }

    updateCanvas(imgD = this.ImageData, DeepCopy = false) {
        if (DeepCopy) {
            imgD = new ImageData(
                new Uint8ClampedArray(imgD.data),
                imgD.width,
                imgD.height
            )
        }

        this.ImageData = imgD
        this.context.putImageData(imgD, 0, 0)
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
            this.ImageData.data[PixelIndex + i] = rgba[i]
        }
    }

    drawPoint(x, y, rgba) {

        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                this.setPixel(x + i, y + j, rgba)
            }
        }
        this.updateCanvas()
    }

    drawLine(x0, y0, x1, y1, rgba) {
        this.daa(x0, y0, x1, y1, rgba)
    }

    draw(x0, y0, x1, y1, rgba, mode = this.mode) {
        if (mode == "daa") {
            this.daa(x0, y0, x1, y1, rgba)
        } else if (mode == "midpoint") {
            let R = Math.round( Math.sqrt((x0 - x1)*(x0 - x1) + (y0 - y1)*(y0 - y1)))
            this.midpoint(x0, y0, R, rgba)
        } else if (mode == "bresenham"){
            this.bresenham(x0, y0, x1, y1, rgba)
        }
    }

    getPosOnCanvas(x, y) {
        let bbox = this.canvas.getBoundingClientRect();
        return [
            Math.floor(x - bbox.left * (this.width / bbox.width) + 0.5),
            Math.floor(y - bbox.top * (this.height / bbox.height) + 0.5)
        ]
    }

    clear() {
        this.context.clearRect(0, 0, this.width, this.height);
        this.ImageData = this.context.getImageData(0, 0, this.width, this.height)
    }

    changeMode(mode){
        this.mode = mode
    }
}

class EventListenerPainter {
    tempRgba = [255, 0, 0, 255]

    constructor(painter) {
        this.painter = painter
        this.MousePressed = false

        this.pressedPoint = [0,0]


        this.painter.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.painter.canvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.painter.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.painter.canvas.addEventListener('mouseout', this.onMouseout.bind(this));
        document.addEventListener('keydown', this.onESC.bind(this));


    }
    onMouseDown(e) {
        // when the cursor is pressed on the canvas
        if (this.MousePressed) {
            return
        }
        this.MousePressed = true
        this.pressedPoint = this.painter.getPosOnCanvas(e.clientX, e.clientY)

        // preserve the current canvas
        this.tempImageData = this.painter.getImageData()
    }
    onMouseUp(e) {
        // when the cursor is lifted on the canvas
        if (!this.MousePressed) {
            return
        }
        this.MousePressed = false

        this.painter.updateCanvas(this.tempImageData)

        let liftedPoint = this.painter.getPosOnCanvas(e.clientX, e.clientY)

        // this.painter_callback(this.pressedPoint, liftedPoint)
        this.painter.draw(this.pressedPoint[0], this.pressedPoint[1], liftedPoint[0], liftedPoint[1], this.painter.lineRgba)
        this.painter.updateCanvas()
    }
    onMouseMove(e) {
        // when the cursor is moved on the canvas
        if (!this.MousePressed) {
            return
        }

        let [x, y] = this.painter.getPosOnCanvas(e.clientX, e.clientY)

        // removed the last guide line
        this.painter.updateCanvas(this.tempImageData, true)

        // TODO: context is updated twice here
        this.painter.draw(this.pressedPoint[0], this.pressedPoint[1], x, y, this.tempRgba)

        this.painter.updateCanvas()
    }
    onMouseout(e) {
        if (this.MousePressed) {
            this.MousePressed = false
            this.painter.updateCanvas(this.tempImageData)
        }
    }

    onESC(e) {
        if (!this.MousePressed) {
            return
        }

        let keyID = e.keyCode ? e.keyCode : e.which
        if (keyID == 27) {
            this.MousePressed = false
            this.painter.updateCanvas(this.tempImageData)
        }
    }
}





export {
    Painter,
    EventListenerPainter
}


