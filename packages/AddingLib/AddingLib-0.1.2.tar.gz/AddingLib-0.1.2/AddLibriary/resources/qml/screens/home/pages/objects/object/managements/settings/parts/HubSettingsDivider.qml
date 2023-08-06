import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

Item {
    width: parent.width
    height: 1

    Rectangle {
        width: parent.width - 2
        height: 1
        color: ui.colors.light1
        opacity: 0.2
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
