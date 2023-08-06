import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: columnItem

    width: parent.width
    height: columnItem.margin + columnItemBody.height

    property var margin: 0
    property var contentItem: null
    property var trueWidth: parent.width * 0.5

    property alias itemLoader: itemLoader
    property alias columnItemBody: columnItemBody

    Item {
        id: columnItemBody

        width: columnItem.trueWidth
        height: itemLoader.item.height

        anchors {
            top: parent.top
            topMargin: columnItem.margin
            horizontalCenter: parent.horizontalCenter
        }

        Loader {
            id: itemLoader

            clip: true
            anchors.fill: parent
            sourceComponent: columnItem.contentItem
        }
    }
}
