import QtQuick 2.14
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.ScrollView {
    id: scrollView

//  Padding of the list's content
    property var contentPadding: 24
//  Original list component
    property alias list: list

    property bool scrollBarVisible: true

//  When list scrolled to bottom
    signal bottomReached()

    anchors.fill: undefined

    padding: 0

    ListView {
        id: list

        width: parent.width - contentPadding * 2
        height: scrollView.height

        anchors.horizontalCenter: parent.horizontalCenter

        clip: true
        spacing: 4
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: DS3.ScrollBar {
            parent: scrollView

            visible: scrollView.height < list.contentHeight && scrollBarVisible
        }

        header: Item {
            height: contentPadding
        }
        footer: Item {
            height: contentPadding
        }

        MouseArea {
            readonly property real velocity: 1

            anchors.fill: parent

            acceptedButtons: Qt.NoButton
            z: -1

            onWheel: (e) => {
                if (!list.ScrollBar.vertical.visible) return

                const movementY = -(e.angleDelta.y / velocity)

                if (movementY < 0 || !list.atYEnd) {
                    list.ScrollBar.vertical.active = true;
                    list.contentY = Math.max(list.contentY + movementY, 0)
                    list.returnToBounds()
                    list.ScrollBar.vertical.active = false;
                    if (list.atYEnd) bottomReached()
                }
            }
        }
    }
}
