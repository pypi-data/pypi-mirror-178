import QtQuick 2.0


Item {
    id: progressForward

//  How much steps need to completed progress
    property int stepsAmount: 5
//  Value that we increase
    property double value: 100 / stepsAmount

//  Value parameters
    readonly property double from: 0
    readonly property double to: 100

//  Progress circle angle
    readonly property double fromAngle: 0 - Math.PI / 2
    readonly property double toAngle: Math.PI * 2 - Math.PI / 2

    function update() {
        progressForward.value += 100 / stepsAmount
        canvas.requestPaint()
        background.requestPaint()
    }

    width: 32
    height: 32

    transformOrigin: Item.Center

    Canvas {
        id: background

        width: parent.width
        height: parent.height

        antialiasing: true

        onPaint: {
            var radius = background.width / 2
            var centreX = background.width / 2.0
            var centreY = background.height / 2.0
            var ctx = background.getContext('2d')

            ctx.strokeStyle = ui.ds3.special.hole
            ctx.lineWidth = 2
            ctx.lineCap = "round"
            ctx.beginPath()
            ctx.clearRect(0, 0, background.width, background.height)
            ctx.arc(centreX, centreY, radius - 2, progressForward.fromAngle, progressForward.toAngle, false)
            ctx.stroke()
        }
    }

    Canvas {
        id: canvas

        width: parent.width
        height: parent.height

        antialiasing: true

        onPaint: {
            var step = progressForward.value / (progressForward.to - progressForward.from) * (progressForward.toAngle - progressForward.fromAngle)
            var radius = height / 2
            var centreX = canvas.width / 2.0
            var centreY = canvas.height / 2.0
            var ctx = canvas.getContext('2d')

            ctx.strokeStyle = ui.ds3.figure.interactive
            ctx.lineWidth = 2
            ctx.lineCap = "round"
            ctx.beginPath()
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            ctx.arc(centreX, centreY, radius - 2, progressForward.fromAngle, progressForward.fromAngle + step, false)
            ctx.stroke()
        }
    }
}