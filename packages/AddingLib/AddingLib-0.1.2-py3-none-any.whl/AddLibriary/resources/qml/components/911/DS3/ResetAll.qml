import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  Component size
    enum ComponentSize {
        S,    // 16x16
        M,    // 24x24
        L     // 32x32
    }
//  Property need for pixel size
    readonly property int sizeInPixels: {
        switch (size) {
            case DS3.ResetAll.ComponentSize.S: 16;
            break;
            case DS3.ResetAll.ComponentSize.M: 24;
            break;
            case DS3.ResetAll.ComponentSize.L: 32;
            break;
        }
    }
//  Whether checked or not
    property bool checked: false
//  If you need to add action on item
    property alias clickedArea: clickedArea
//  Default size of component
    property var size: DS3.ResetAll.ComponentSize.M

    width: sizeInPixels
    height: sizeInPixels

    border {
        width: 2

        color: ui.ds3.figure.secondary
    }
    color: ui.ds3.figure.transparent
    radius: 2
    opacity: enabled ? 1 : 0.3

    Rectangle {
        width: Math.round(sizeInPixels / 3)
        height: 2

        anchors.centerIn: parent

        visible: checked
        color: ui.ds3.figure.secondary
    }

    DS3.MouseArea {
        id: clickedArea
    }
}