import QtQuick 2.12
import QtQuick.Controls 2.13


Rectangle {
//  Amount of dots
    property int amount: 2
//  Index of current dot. Starts at 0
    property int current: 0
//  If first circle is triangle
    property bool firstTriangle: false
//  If with background
    property bool withBackground: false

    width: repeaterRow.width + 32
    height: withBackground ? 24 : 8

    color: withBackground ? ui.ds3.bg.high : ui.ds3.figure.transparent
    radius: 12

    Row {
        id: repeaterRow

        height: 8

        anchors.centerIn: parent

        spacing: 8

        Repeater {
            model: amount

            Rectangle {
                width: 8
                height: 8

                color: {
                    if (index == 0 && firstTriangle) {
                        return ui.ds3.figure.transparent
                    }
                    return current == index ? ui.ds3.figure.interactive : ui.ds3.special.hole
                }
                radius: index == 0 && firstTriangle ? 0 : 4

                Canvas{
                    anchors.fill: parent

                    visible: index == 0 && firstTriangle

                    onPaint:{
                        var context = getContext("2d");

                        // the triangle
                        context.beginPath();
                        context.moveTo(0, 0);
                        context.lineTo(0, 8);
                        context.lineTo(7, 4);
                        context.closePath();

                        // the fill color
                        context.fillStyle = current == index ? ui.ds3.figure.interactive : ui.ds3.special.hole;
                        context.fill();
                    }
                }

                Behavior on color {
                    ColorAnimation {
                        duration: 200
                    }
                }
            }
        }
    }
}
