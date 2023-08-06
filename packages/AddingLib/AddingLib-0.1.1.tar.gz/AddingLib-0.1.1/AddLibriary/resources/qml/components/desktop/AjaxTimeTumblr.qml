import QtQuick 2.12
import QtQuick.Window 2.2
import QtQuick.Controls 2.12

Item {
    property alias minutesTumbler: minutesTumbler
    property alias secondsTumbler: secondsTumbler

    function formatText(count, modelData) {
        var data = count === 12 ? modelData + 1 : modelData;
        return data.toString().length < 2 ? "0" + data : data;
    }

    Component {
        id: delegateComponent

        Label {
            text: formatText(Tumbler.tumbler.count, modelData)
            opacity: 1.0 - Math.abs(Tumbler.displacement) / (Tumbler.tumbler.visibleItemCount / 3)
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 18
            color: ui.colors.green1
        }
    }

    Item {
        id: frame
        width: parent.width
        height: parent.height

        Row {
            id: row
            anchors.centerIn: parent

            Tumbler {
                id: minutesTumbler
                height: 128
                width: 24
                model: 60
                currentIndex: 3
                delegate: delegateComponent
                MouseArea {
                    anchors.fill: parent
                    onWheel: {
                        if (wheel.angleDelta.y > 0) {
                            minutesTumbler.currentIndex -= 1
                        } else {
                            minutesTumbler.currentIndex += 1
                        }
                    }
                }
            }

            Item {
                width: 6
                height: parent.height
                Text {
                    text: ":"
                    color: ui.colors.green1
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            Tumbler {
                id: secondsTumbler
                height: 128
                width: 24
                model: 60
                currentIndex: 0
                delegate: delegateComponent

                MouseArea {
                    anchors.fill: parent
                    onWheel: {
                        if (wheel.angleDelta.y > 0) {
                            secondsTumbler.currentIndex -= 1
                        } else {
                            secondsTumbler.currentIndex += 1
                        }
                    }
                }
            }
        }
    }
}