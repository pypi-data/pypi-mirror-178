import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T


Item {
    id: comboSearch
    width: 256
    height: 32

    property var model: null
    property var currentText: ""
    property var defaultText: ""

    property alias field: topLevel
    property alias popup: comboPopup

    TextField {
        id: topLevel
        text: comboSearch.currentText
        selectByMouse: true
        color: ui.colors.light1
        font.pixelSize: 13
        font.family: roboto.name
        font.weight: Font.Medium
        font.letterSpacing: 1
        leftPadding: 10
        bottomPadding: 5
        rightPadding: 32
        width: parent.width - 64
        height: parent.height
        anchors.centerIn: parent

        PlaceholderText {
            id: placeholder
            x: topLevel.leftPadding
            y: topLevel.topPadding
            width: topLevel.width - (topLevel.leftPadding + topLevel.rightPadding)
            height: topLevel.height - (topLevel.topPadding + topLevel.bottomPadding)
            visible: !topLevel.length && !topLevel.preeditText && (!topLevel.activeFocus || topLevel.horizontalAlignment !== Qt.AlignHCenter)

            text: comboSearch.defaultText
            font: topLevel.font
            opacity: 0.5
            color: ui.colors.light1
            verticalAlignment: topLevel.verticalAlignment
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: topLevel.width
            implicitHeight: topLevel.height
            color: topLevel.enabled ? "#616161" : "gray"
            radius: 3

            Image {
                width: 22
                height: 22
                visible: topLevel.text != ""
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    rightMargin: 7
                }

                source: "qrc:/resources/images/icons/ic-clear.png"

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        topLevel.text = ""
                    }
                }
            }
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.IBeamCursor
            propagateComposedEvents: true
            onClicked: {
                comboPopup.open()
                mouse.accepted = false
                topLevel.forceActiveFocus()
            }
        }
    }

    Popup {
        id: comboPopup
        width: topLevel.width + 4
        height: 200
        modal: false
        focus: false
        parent: topLevel

        x: -2
        y: topLevel.y + topLevel.height + 4
        z: topLevel.z

        padding: 0

        closePolicy: Popup.CloseOnEscape

        background: Item {}

        enter: Transition {
            NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 100 }
        }

        exit: Transition {
            NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 100 }
        }

        Rectangle {
            anchors.fill: parent
            color: "#212121"
            radius: 4
            border.width: 0.1
            border.color: "#1a1a1a"
            opacity: 0.999
        }
    }
}
