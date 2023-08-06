import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups

Popup {
    id: topLevel
    width: 177
    height: 101

    x: application.width - width - 16
    y: 62
    modal: false
    focus: true

    padding: 0

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Item {}

    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
    }

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999

        /*
        Item {
            height: parent.height / 2
            width: parent.width

            anchors {
                top: parent.top
                topMargin: 3
            }

            Image {
                id: settingsIcon
                source: "qrc:/resources/images/icons/ic-tooltip-settings@2x.png"

                height: 20
                width: 20

                anchors {
                    left: parent.left
                    leftMargin: 14
                    verticalCenter: parent.verticalCenter
                }
            }

            Text {
                id: settingsLabel
                text: tr.action_settings
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 12
                opacity: 0.8

                anchors {
                    left: settingsIcon.right
                    leftMargin: 6
                    verticalCenter: parent.verticalCenter
                }
            }

            MouseArea {
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                height: settingsIcon.height
                width: settingsIcon.width + 6 + settingsLabel.width

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: settingsIcon.left
                }

                onClicked: {
                }
            }
        }
        */

        Item {
            height: parent.height / 2
            width: parent.width

            anchors {
                top: parent.top
                topMargin: 3
            }

            AjaxSettingsCombobox {
                anchors.centerIn: parent
                id: languageCombobox
                width: 180
                highlightSelected: true
                model: tr.get_available_tr().languages
                currentIndex: model.indexOf(tr.get_selected())
                anchors {
                    top: parent.top
                    topMargin: 40
                    left: parent.left
                    leftMargin: 30
                }

                onValueActivated: {
                    tr.select_lang(currentIndex)
                }
            }
        }

        Item {
            height: parent.height / 2
            width: parent.width

            anchors {
                bottom: parent.bottom
                bottomMargin: 3
            }

            Image {
                id: problemsIcon
                source: "qrc:/resources/images/icons/ic-tooltip-report@2x.png"

                height: 20
                width: 20

                anchors {
                    left: parent.left
                    leftMargin: 24
                    verticalCenter: parent.verticalCenter
                }
            }

            Text {
                id: problemsLabel
                text: tr.report_problem
                width: parent.width - 64
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 12
                opacity: 0.8
                wrapMode: Text.WordWrap

                anchors {
                    left: problemsIcon.right
                    leftMargin: 6
                    verticalCenter: parent.verticalCenter
                }
            }

            MouseArea {
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                height: problemsIcon.height
                width: problemsIcon.width + 6 + problemsLabel.width

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: problemsIcon.left
                }

                onClicked: {
                    topLevel.close()
                    Popups.report_problem()
                }
            }
        }
    }
}
