import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS" as DS


// Text that can be copied with appropriate text
DS.Text {
    id: copyText

    enum Position {
        Bottom,
        Right
    }

//  Position of the tooltip
    property var position: CopyText.Position.Bottom

    height: contentHeight

    Binding on color {
        when: copyArea.containsMouse
        value: ui.colors.interactive
    }

    DS.MouseArea {
        id: copyArea

        hoverEnabled: true

        onClicked: {
            util.set_clipboard_text(parent.text)
            tooltip.show(700)
        }
    }

    Item {
        id: tooltip

        property int tooltipPadding: 4

        width: checkMark.width + 4 + copiedText.width + 2 * tooltipPadding
        height: copiedText.height + 2 * tooltipPadding

        anchors {
            verticalCenter: position == CopyText.Position.Bottom ? undefined : parent.verticalCenter
            left: parent.left
            leftMargin: (
                position == CopyText.Position.Bottom ?
                    (copyText.contentWidth - tooltip.width) / 2 :
                    copyText.contentWidth + checkMark.anchors.leftMargin
            )
            top: position == CopyText.Position.Bottom ? parent.bottom : undefined
            topMargin: 4
        }

        opacity: 0

        DropShadow {
            anchors.fill: background
            verticalOffset: 1
            radius: 5
            samples: 17
            color: ui.backgrounds.overlay
            source: background
        }

        Rectangle {
            id: background

            anchors.fill: parent

            color: ui.backgrounds.highest
            radius: tooltip.tooltipPadding
        }

        DS.Text {
            id: copiedText

            width: contentWidth

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: tooltip.tooltipPadding
            }

            text: tr.copied
            color: ui.colors.interactive
        }

        DS.Image {
            id: checkMark

            anchors {
                left: copiedText.right
                leftMargin: 4
                verticalCenter: parent.verticalCenter
            }

            width: 12
            height: 12

            source: "qrc:/resources/images/Athena/common_icons/check.svg"
        }

        Timer {
            id: tooltipTimer
            triggeredOnStart: true
            onTriggered: {
                if (tooltip.opacity == 0) {
                    tooltip.opacity = 1
                } else {
                    tooltip.opacity = 0
                }
            }
        }

        function show(delay) {
            if (opacity == 0) {
                tooltipTimer.interval = delay
                tooltipTimer.start()
            }
        }

        Behavior on opacity {
            NumberAnimation { duration: 150 }
        }
    }
}
