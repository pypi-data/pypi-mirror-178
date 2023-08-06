import QtQuick 2.13
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/" as Custom


ComboBox {
    id: control
    height: 40

    model: []

    property var defaultText: ""
    property var countryCodes: []
    property var defaultWidth: 100

    property alias backgroundRectangle: backgroundRectangle

    font.family: roboto.name
    font.pixelSize: 14

    delegate: ItemDelegate {
        id: delegate
        width: control.width
        height: 48

        contentItem: Item {
            id: delegateItem
            width: parent.width - 12

            Image {
                id: delegateImage
                width: 24
                height: 24
                source: {
                    if (index == 0) return "qrc:/resources/images/desktop/countries/earth.png"
                    return "qrc:/resources/images/desktop/countries/" + countryCodes[index] + ".png"
                }

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }
            }

            Custom.FontText {
                id: delegateText

                text: modelData
                width: parent.width - 40
                color: ui.colors.light1

                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: delegateImage.right
                    leftMargin: 8
                }
            }
        }

        background: Rectangle {
            id: rect
            color: hovered ? ui.colors.dark3 : ui.colors.dark1
            width: parent.width
            height: delegate.height
        }

        Image {
            id: selectedImage

            visible: index == control.currentIndex
            sourceSize.width: 40
            sourceSize.height: 40
            source: "qrc:/resources/images/incidents/cards/a-green-badge.svg"

            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }
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

    contentItem: Item {
        Image {
            id: contentImage
            width: 24
            height: 24
            source: {
                if (currentIndex == 0) return "qrc:/resources/images/desktop/countries/earth.png"
                return "qrc:/resources/images/desktop/countries/" + countryCodes[currentIndex] + ".png"
            }

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 8
            }
        }

        Custom.FontText {
            id: contentText

            width: parent.width - 48
            text: control.displayText
            color: ui.colors.light1

            wrapMode: Text.Wrap
            elide: Text.ElideRight
            font.letterSpacing: 0.5
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft

            anchors {
                left: contentImage.right
                leftMargin: 8
                verticalCenter: parent.verticalCenter
            }
        }
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
        height: 200
        padding: 0

        contentItem: ScrollView {
            topPadding: 6
            bottomPadding: 6

            ListView {
                id: listView
                clip: true
                implicitHeight: contentHeight
                model: control.popup.visible ? control.delegateModel : null
                currentIndex: control.highlightedIndex
                spacing: 1

                anchors {
                    top: parent.top
                    topMargin: 8
                    bottom: parent.bottom
                    bottomMargin: 8
                }
            }
        }

        background: Rectangle {
            anchors.fill: parent
            color: ui.colors.dark2
            border.color: "transparent"
            radius: 8

            Rectangle {
                color: ui.colors.dark4

                anchors {
                    fill: parent
                    topMargin: 8
                    bottomMargin: 8
                }
            }
        }
    }

    Connections {
        target: management.companies

        onCompaniesReceived: {
            var data = management.companies.get_countries(tr.get_selected())

            control.model = data.countries
            control.countryCodes = data.codes
        }
    }
}
