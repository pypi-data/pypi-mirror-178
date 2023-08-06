import QtQuick 2.12
import QtQuick.Controls 2.13

Canvas {
    id: canvas
    width: 12
    height: 6
    contextType: "2d"
    property var colorTriangle: ui.colors.middle1
    onPaint: {
        context.reset();
        context.moveTo(0, 0);
        context.lineTo(width, 0);
        context.lineTo(width / 2, height);
        context.closePath();
        context.fillStyle = colorTriangle;
        context.fill();
    }
}