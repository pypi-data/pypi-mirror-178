import QtQuick 2.7
import QtQuick.Controls 2.2

Item {
    width: 16
    height: 16

    Canvas {
        id: canvas
        width: 12
        height: 6
        contextType: "2d"
        property var colorTriangle: "#60e3ab"
        onPaint: {
            context.reset();
            context.moveTo(0, 0);
            context.lineTo(width, 0);
            context.lineTo(width / 2, height);
            context.closePath();
            context.fillStyle = colorTriangle;
            context.fill();
        }
        anchors.centerIn: parent
    }
}