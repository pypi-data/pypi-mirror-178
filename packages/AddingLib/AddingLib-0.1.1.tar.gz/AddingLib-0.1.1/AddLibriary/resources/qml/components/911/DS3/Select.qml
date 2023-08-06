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
            case DS3.Select.ComponentSize.S: 16;
            break;
            case DS3.Select.ComponentSize.M: 24;
            break;
            case DS3.Select.ComponentSize.L: 32;
            break;
        }
    }
//  Default size of component
    property var size: DS3.Select.ComponentSize.M
//  Whether checked or not
    property bool checked: false
//  If you need to add action on item
    property alias clickedArea: clickedArea
//  Shape of checkbox
    property bool isRound: false
// Whether checkbox is outlined
    property bool hasBackground: false
//  Whether to cancel property binding
    property bool cancelBinding: true

    Component.onCompleted: if (cancelBinding) checked = checked

    width: sizeInPixels
    height: sizeInPixels

    border {
        width: {
            if (hasBackground) return 0
            return checked ? 0 : 2
        }
        color: ui.ds3.figure.secondary
    }
    color: {
        if (checked && !hasBackground) return ui.ds3.figure.interactive
        return ui.ds3.figure.transparent
    }
    radius: isRound ? 12 : 2
    opacity: enabled ? 1 : 0.3


    DS3.Icon {
        anchors.centerIn: parent

        visible: checked
        source: hasBackground
                ? "qrc:/resources/images/Athena/common_icons/Check-M.svg"
                : "qrc:/resources/images/Athena/common_icons/checkMark.svg"
        color: hasBackground ? ui.ds3.figure.interactive : ui.ds3.figure.inverted
    }

    DS3.MouseArea {
        id: clickedArea
    }
}