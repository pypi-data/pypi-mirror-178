import QtQuick 2.12

import "qrc:/resources/qml/components/911/" as Custom

Rectangle {
    id: footer

    property alias btn: btn
    property alias roundRect: roundRect
    property alias topRightCorner: roundRect.topRightCorner
    property alias bottomRightCorner: roundRect.bottomRightCorner

    /* ------------------------------------------------ */
    /* desktop tests */
    property var accessibleButtonName: ""
    /* ------------------------------------------------ */

    width: parent.width
    height: visible ? 72 : 0

    clip: true
    color: ui.colors.black

    Custom.RoundedRect {
        id: roundRect

        width: parent.width
        height: parent.height

        radius: 10
        color: ui.colors.dark3
        topRightCorner: false

        Custom.Button {
            id: btn

            width: footer.width - 64
            height: 40

            anchors {
                top: parent.top
                topMargin: 24
                verticalCenter: parent.verticalCenter
                centerIn: parent
            }

            transparent: true
            text: tr.add_room

            /* -------------------------------------------- */
            /* desktop tests */
            Accessible.name: footer.accessibleButtonName
            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
            Accessible.role: Accessible.Button
            Accessible.checkable: visible && enabled
            Accessible.onPressAction: {
                if (!Accessible.checkable) return
                btn.clicked(true)
            }
            /* -------------------------------------------- */
        }
    }
}
