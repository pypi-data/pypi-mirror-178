import QtQuick 2.14
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


ScrollView {
    id: view

//  Custom scrollBar
    readonly property var scrollBar: DS3.ScrollBar {}
//  Flag of scrollBar visibility
    property bool scrollBarVisibility: true
//  Spacing between items
    property alias contentSpacing: content.spacing
//  Padding existance for scrollBar
    property bool scrollBarHasPadding: true
//  Content of scrollview is enabled
    property alias contentEnabled: content.enabled

    default property alias data: content.data

    anchors.fill: parent

    padding: 32
    contentHeight: content.height
    objectName: "scrollView"
    clip: true

    Component.onCompleted: {
        scrollBar.visible = Qt.binding(() => content.height + 2 * view.padding > view.height && enabled && scrollBarVisibility)
        scrollBar.hasPadding = view.scrollBarHasPadding
        ScrollBar.vertical = scrollBar
    }

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AlwaysOff

    Flickable {
        id: flickable

        anchors {
            fill: parent
            margins: parent.padding
            leftMargin: parent.leftPadding
            rightMargin: parent.rightPadding
            topMargin: parent.topPadding
            bottomMargin: parent.bottomMargin
        }

        boundsBehavior: Flickable.StopAtBounds

        MouseArea {
            readonly property real velocity: 1

            anchors.fill: parent

            acceptedButtons: Qt.NoButton
            enabled: view.ScrollBar.vertical.visible

            onWheel: (e) => {
                const movementY = -(e.angleDelta.y / velocity)

                view.ScrollBar.vertical.active = true;
                if (flickable.contentY + movementY + flickable.height > flickable.contentHeight) {
                    flickable.contentY = flickable.contentHeight - flickable.height
                } else if (flickable.contentY + movementY < 0) {
                    flickable.contentY = 0
                } else {
                    flickable.contentY += movementY
                }
                view.ScrollBar.vertical.active = false;
            }
        }

        Column {
            id: content

            width: view.width - view.leftPadding - view.rightPadding
        }
    }
}