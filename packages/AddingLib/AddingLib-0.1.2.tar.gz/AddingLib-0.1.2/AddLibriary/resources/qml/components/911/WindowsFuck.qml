import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/"


Item {
    width: 4
    height: 4

    // according to A911-427 (OS Windows) ui freezes during the resizing
    // infinite animation should fix the problem (login screen, home/header, pro/header)

    property var color: ui.colors.black

    Rectangle {
        id: loopRect
        width: 4
        height: 4
        radius: height / 2
        color: parent.color
    }

    RotationAnimator {
        target: loopRect
        loops: Animation.Infinite
        from: 0
        to: 360
        duration: 300
        running: false
    }
}
