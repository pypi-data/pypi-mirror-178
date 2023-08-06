import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


ComboBox {
    id: control
    height: 40

    property var days: 0
    property var defaultText: "..."
//    property var copyVisible: true

    property alias backgroundRectangle: backgroundRectangle

    font.family: roboto.name
    font.pixelSize: 16

    displayText: {
        if (control.days == 0) return defaultText

        if (control.days == 7) return tr.seven_days
        if (control.days == 30) return tr.thirty_days
        if (control.days == 90) return tr.ninety_days
        if (control.days == 180) return tr.one_hundred_eighty_days
        if (control.days == 365) return tr.one_year
        if (control.days == 730) return tr.two_years

        return defaultText
    }

    model: [
        {"days": 7, "repr": tr.seven_days},
        {"days": 30, "repr": tr.thirty_days},
        {"days": 90, "repr": tr.ninety_days},
        {"days": 180, "repr": tr.one_hundred_eighty_days},
        {"days": 365, "repr": tr.one_year},
        {"days": 730, "repr": tr.two_years},
    ]

    delegate: ItemDelegate {
        id: delegate
        width: control.width
        height: 48
        contentItem: Text {
            text: modelData.repr
            color: ui.colors.white
            font: control.font
            elide: Text.ElideRight
            leftPadding: 4
            verticalAlignment: Text.AlignVCenter
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark4
            anchors.bottom: parent.bottom
        }

        background: Rectangle {
            id: rect
            color: hovered ? ui.colors.dark3 : ui.colors.dark1
            width: parent.width
            height: delegate.height
        }

        Image {
            id: selectedImage

            visible: control.days == modelData.days
            sourceSize.width: 40
            sourceSize.height: 40
            source: "qrc:/resources/images/incidents/cards/a-green-badge.svg"

            anchors.right: parent.right
            anchors.rightMargin: 6
        }
    }

    indicator: Canvas {
        id: canvas
        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        width: 12
        height: 6
        contextType: "2d"

        Connections {
            target: control
            onPressedChanged: {
                canvas.requestPaint()
            }
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

    contentItem: Text {
        id: textLabel
        leftPadding: 16
        rightPadding: control.indicator.width + control.spacing

        text: control.displayText
        font: control.font
        color: control.pressed ? ui.colors.white : ui.colors.white
        opacity: control.days == 0 ? 0.5 : 1
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        id: backgroundRectangle
        implicitWidth: 120
        implicitHeight: 36
        radius: 8
        color: ui.colors.dark1
    }

    popup: Popup {
        y: control.height + 1
        width: control.width
        height: listView.contentHeight > 360 ? 360 : listView.contentHeight + 21
        padding: 0

        contentItem: ListView {
            id: listView
            height: parent.height - 21
            clip: true
            spacing: 0
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            boundsBehavior: Flickable.StopAtBounds
            anchors {
                top: parent.top
                topMargin: 8
                bottom: parent.bottom
                bottomMargin: 13
            }

            ScrollBar.vertical: Custom.ScrollBar {
                id: scrollBar
                parent: listView
                anchors {
                    top: parent.top
                    right: parent.right
                    bottom: parent.bottom
                }

                policy: ScrollBar.AlwaysOff
            }
        }

        background: Rectangle {
            anchors.fill: parent
            color: ui.colors.dark2
            border.color: "transparent"
            radius: 8
        }
    }
}
