import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


ComboBox {
    id: control

    height: 42
    model: ["Some text 1", "Some text 2", "Some text 3"]

    property var defaultText: tr.a911_not_chosen + "..."
    property var copyVisible: true

    property alias backgroundRectangle: backgroundRectangle
    property alias textLabel: textLabel

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleItemNamePrefix: ""
    /* ---------------------------------------------------- */

    font.family: roboto.name
    font.pixelSize: 14

    delegate: ItemDelegate {
        id: delegate

        width: control.width
        height: 40
        contentItem: Custom.FontText {
            text: modelData
            textFormat: textLabel.textFormat
            color: ui.colors.white
            font: control.font
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            id: rect
            color: hovered ? ui.colors.dark3 : ui.colors.dark1
            width: parent.width
            height: delegate.height
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: control.accessibleItemNamePrefix ? control.accessibleItemNamePrefix + "_" + modelData : ""
        Accessible.description: control.accessibleItemNamePrefix ? "<button enabled=" + Accessible.checkable + ">" + modelData + "</button>" : ""
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            control.currentIndex = index
            control.activated(index)
        }
        /* ---------------------------------------------------- */
    }

    indicator: Canvas {
        id: canvas

        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        width: 12
        height: 6
        contextType: "2d"
        visible: control.enabled

        Connections {
            target: control
            onPressedChanged: canvas.requestPaint()
        }

        onPaint: {
            context.reset();
            context.moveTo(0, 0);
            context.lineTo(width, 0);
            context.lineTo(width / 2, height);
            context.closePath();
            context.fillStyle = control.pressed ? ui.colors.middle1 : ui.colors.middle1;
            context.fill();
        }
    }

    contentItem: Custom.FontText {
        id: textLabel

        leftPadding: 12
        rightPadding: {
            if (copyItem.visible) {
                return control.indicator.width + control.spacing + 12 + 18
            }
            return control.indicator.width + control.spacing
        }

        text: control.currentIndex == -1 ? defaultText : control.displayText
        font: control.font
        color: ui.colors.white
        opacity: control.currentIndex == -1 ? 0.5 : 1
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight

        Rectangle {
            id: copyItem

            visible: control.hovered && copyVisible && currentIndex != -1
            color: "transparent"
            width: 18
            height: 18
            anchors.right: parent.right
            anchors.rightMargin: control.indicator.width + control.spacing + 12
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -1

            Rectangle {
                id: greenRect

                width: 10
                height: 10
                color: "transparent"
                anchors.centerIn: parent
                radius: 3
                border {
                    color: ui.colors.green1
                    width: 1
                }

                Rectangle {
                    width: 10
                    height: 10
                    border {
                        color: parent.border.color
                        width: 1
                    }
                    radius: parent.radius
                    color: backgroundRectangle.color
                    anchors.centerIn: parent
                    anchors.verticalCenterOffset: 3
                    anchors.horizontalCenterOffset: -3
                }
            }

            Custom.HandMouseArea {
                id: copyArea

                anchors.fill: parent

                onEntered: greenRect.border.color = ui.colors.green2
                onExited: greenRect.border.color = ui.colors.green1

                ToolTip {
                    id: tooltip
                    parent: parent

                    contentItem: Text {
                        text: tr.copied
                        font.family: roboto.name
                        font.pixelSize: 12
                        color: ui.colors.light1
                    }

                    background: Rectangle {
                        color: ui.colors.dark4
                        radius: 4
                        border {
                            width: 1
                            color: ui.colors.green1
                        }
                    }
                }

                onClicked: {
                    util.set_clipboard_text(textLabel.text)
                    tooltip.show("", 500)
                }
            }
        }
    }

    background: Rectangle {
        id: backgroundRectangle
        implicitWidth: 120
        implicitHeight: 36
        border.color: (control.popup.opened || control.activeFocus) ? ui.colors.green1 : "transparent"
        border.width: (control.popup.opened || control.activeFocus) ? 1 : 0
        radius: (control.popup.opened || control.activeFocus) ? 0 : 8
        color: ui.colors.dark2
    }

    popup: Popup {
        y: control.height + 1
        width: control.width
        height: Math.min(listView.contentHeight, 252)
        padding: 0

        contentItem: ScrollView {
            ListView {
                id: listView
                clip: true
                implicitHeight: contentHeight
                model: control.popup.visible ? control.delegateModel : null
                currentIndex: control.highlightedIndex
                spacing: 1

                footer: Custom.RoundedRect {
                    width: listView.width
                    height: 8
                    bottomRightCorner: true
                    bottomLeftCorner: true
                    color: ui.colors.dark1
                    radius: 8
                }
            }
        }

        background: Rectangle {
            color: ui.colors.dark4
            border.color: "transparent"
            radius: 2
        }
    }
}