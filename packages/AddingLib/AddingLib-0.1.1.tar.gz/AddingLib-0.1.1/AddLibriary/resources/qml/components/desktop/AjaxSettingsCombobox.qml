import QtQuick 2.7
import QtQuick.Controls 2.2


import "qrc:/resources/qml/components/desktop/"


Item {
    id: topLevel
    width: parent.width
    height: control.contentItem.contentHeight + 24
    opacity: enabled ? 1.0 : 0.5

    signal valueActivated()

    property var model: []
    property string miniText: ""
    property alias currentIndex: control.currentIndex
    property alias currentText: control.currentText
    property alias combobox: control
    property bool highlightSelected: false
    property bool smallAndBright: false
    property alias popup: popup
    property alias listView: listView

    property var func: null

    property var filter: ""

    ComboBox {
        id: control
        model: parent.model
        currentIndex: parent.currentIndex
        focusPolicy: Qt.NoFocus

        width: parent.width - 64
        height: textF.contentHeight
        anchors.centerIn: parent

        Keys.onEnterPressed: {
            if (func) func()
        }

        Keys.onReturnPressed: {
            if (func) func()
        }

        onActivated: valueActivated()

        onCurrentIndexChanged: {
            currentIndex = currentIndex
        }

        delegate: ItemDelegate {
            id: delegate
            focusPolicy: Qt.NoFocus
            width: control.width
            height: {
                if (!topLevel.filter.length) return textI.contentHeight + 12
                return modelData.toLowerCase().includes(topLevel.filter.toLowerCase()) ? textI.contentHeight + 12 : 0
            }
            visible: height != 0

            contentItem: Text {
                id: textI
                text: {
                    if (index == control.currentIndex) return "✔ " + modelData
                    return modelData
                }
                color: ui.colors.green1
                opacity: (index == control.currentIndex) ? 1.0 : 0.6
                font.family: roboto.name
                font.pixelSize: 12
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft
                wrapMode: Text.WordWrap
            }

            background: Rectangle {
                id: rect
                color: delegate.hovered ? "#262626" : "transparent"
                width: parent.width
                height: delegate.height
            }
        }

        indicator: Canvas {
            id: canvas
            x: control.width - width - control.rightPadding
            y: control.topPadding + (control.availableHeight - height) / 2
            width: 12
            height: 8
            contextType: "2d"

            Connections {
                target: control
                onPressedChanged: canvas.requestPaint()
            }

            onPaint: {
                var context = getContext("2d");
                context.reset();
                context.moveTo(0, 0);
                context.lineTo(width, 0);
                context.lineTo(width / 2, height);
                context.closePath();
                context.fillStyle = control.pressed ? "#60e3ab" : "#60e3ab"
                context.fill();
            }
        }

        contentItem: Text {
            id: textF
            rightPadding: 16
            leftPadding: 5
            bottomPadding: 5
            focus: false
            text: control.displayText
            font.family: roboto.name
            font.pixelSize: smallAndBright ? 12 : 14
            color: highlightSelected ? "#60e3ab" : "#fdfdfd"
            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WordWrap
            elide: Text.ElideRight
            opacity: smallAndBright || control.delegate.hovered ? 1.0 : 0.8
        }

        background: Rectangle {
            color: "transparent"
            radius: 2
            Rectangle {
                id: bottomBorder
                width: parent.width
                height: 1
                color: {
                    return control.popup.visible ? "#60e3ab" : "#4e4e4e"
                }
                opacity: 0.8
                anchors.top: parent.bottom
                anchors.topMargin: 3
            }

            Text {
                text: miniText
                color: ui.colors.light1
                opacity: 0.5
                font.family: roboto.name
                font.pixelSize: 10
                anchors {
                    bottom: parent.top
                    bottomMargin: 2
                    left: parent.left
                    leftMargin: 2
                }
            }
        }

        popup: Popup {
            id: popup
            y: control.height + 8
            width: control.width
            height: {
                return listView.contentHeight < 219 ? listView.contentHeight + search.height : 218 + search.height
            }
            padding: 1

            contentItem: Item {
                id: item
                width: control.width
                height: listView.height + search.height
                AjaxSearchField {
                    id: search
                    width: control.width
//                    height: 32
                    placeHolderText: "..."
                    focus: true
                    anchors.top: parent.top
                    visible: false
                    height: 0

                    onTextChanged: {
                        topLevel.filter = text
                    }
                }
                ListView {
                    id: listView
                    clip: true
                    focus: false
//                    height: contentHeight < 219 ? contentHeight : 218
                    width: control.width
                    model: control.popup.visible ? control.delegateModel : null
                    currentIndex: control.highlightedIndex
                    anchors.top: search.bottom
                    anchors.bottom: parent.bottom
                    ScrollBar.vertical: ScrollBar {
                        id: scrollBar

                        active: true
                    }
                }
            }

            background: Rectangle {
                anchors.fill: item
                border.color: "#3f3f3f"
                radius: 2
                color: "#3c3c3c"
            }
        }
    }
}
