import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

AjaxPopup {
    id: topLevel
    width: 400
    height: 120

    Rectangle {
        color: "#1f1f1f"
        width: 400
        height: 100
        focus: true

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        Keys.onPressed: {
            if (event.key == Qt.Key_Left || event.key == Qt.Key_Right) {
                yesButton.buttonActive = !yesButton.buttonActive
            }

            if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
                if (yesButton.buttonActive) {
                    yesArea.clicked(true)
                } else {
                    noArea.clicked(true)
                }
            }
        }

        Image {
            id: closeIco
            source: "qrc:/resources/images/logo/logo@2x.png"
            width: 56
            height: 42
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 25
            }
        }

        Text {
            text: tr.Are_you_sure_you_want_to_exit_desktop
            font.pixelSize: 14
            font.family: roboto.name
            font.letterSpacing: 1
            color: ui.colors.light1
            width: 300
            wrapMode: Text.WordWrap

            anchors {
                top: closeIco.top
                topMargin: -5
                left: closeIco.right
                leftMargin: 35
            }
        }

        Rectangle {
            property var buttonActive: true
            property var selectedColor: {
                return buttonActive ? "#60e3ab" : "#7f7f7f"
            }

            id: yesButton
            width: 80
            height: 30
            radius: 5
            color: "#2a2a2a"
            border.color: selectedColor

            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                right: noButton.left
                rightMargin: 20
            }

            Text {
                text: tr.yes
                font.pixelSize: 14
                font.family: roboto.name
                font.letterSpacing: 1
                color: parent.selectedColor
                anchors.centerIn: parent
            }

            MouseArea {
                id: yesArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    topLevel.close()
                    application.close.accepted = true
                    application.visible = false
                    Qt.quit()
                }

                onPositionChanged: {
                    if (yesArea.containsMouse) yesButton.buttonActive = true
                }
            }
        }

        Rectangle {
            property var buttonActive: !yesButton.buttonActive
            property var selectedColor: {
                return buttonActive ? "#60e3ab" : "#7f7f7f"
            }

            id: noButton
            width: 80
            height: 30
            radius: 5
            color: "#2a2a2a"
            border.color: selectedColor

            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                right: parent.right
                rightMargin: 20
            }

            Text {
                text: tr.no
                font.pixelSize: 14
                font.family: roboto.name
                font.letterSpacing: 1
                color: parent.selectedColor
                anchors.centerIn: parent
            }

            MouseArea {
                id: noArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    topLevel.close()
                }

                onPositionChanged: {
                    if (noArea.containsMouse) yesButton.buttonActive = false
                }
            }
        }
    }
}