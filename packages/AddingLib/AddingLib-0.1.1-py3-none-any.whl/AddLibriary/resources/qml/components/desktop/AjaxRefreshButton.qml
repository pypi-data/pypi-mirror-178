import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

Item {
    id: topLevel
    width: 128
    height: 64

    Image {
        id: iconRefresh
        anchors {
            verticalCenter: parent.verticalCenter
        }
        source: "qrc:/app/qml/images/ic-hub-refresh@2x.png"

        RotationAnimation on rotation {
            id: refreshAnim
            loops: 1
            from: 0
            to: 360
            running: false
            duration: 500
        }
    }

    Text {
        anchors {
            verticalCenter: parent.verticalCenter
            left: iconRefresh.right
            leftMargin: 7
        }
        text: "Refresh"
        color: ui.colors.green1
        font.pixelSize: 14
        font.family: roboto.name
        font.weight: Font.Light
    }

    MouseArea {
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        anchors.fill: parent
        onClicked: {
            refreshAnim.running = true
            app.refresh()
        }
    }
}