import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtQuick.Dialogs 1.3

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom

AjaxPopup {
    id: popup
    objectName: "reportPopup"
    width: 440
    height: 520
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true

    anchors.centerIn: parent

    property var userName: ""
    property var userEmail: ""

    property var attachedImage: null

    Component.onCompleted: {
        nameField.control.text = popup.userName
        emailField.control.text = popup.userEmail
    }

    FileDialog {
        id: fileDialog
        title: tr.select_image
        folder: shortcuts.home
        nameFilters: ["Images (*.jpg *.jpeg *.png)"]

        onAccepted: {
            util.prepare_report_image(fileDialog.fileUrl)
            fileDialog.close()
        }

        onRejected: {
            fileDialog.close()
        }
    }

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 10

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.report_problem
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        ScrollView {
            id: scrollView
            clip: true
            width: parent.width
            anchors {
                top: header.bottom
                right: parent.right
                bottom: buttonItem.top
                bottomMargin: 24
            }

            ScrollBar.vertical: Custom.ScrollBar {
                id: scrollBar
                parent: scrollView
                anchors {
                    top: parent.top
                    right: parent.right
                    bottom: parent.bottom
                }
            }

            ColumnLayout {
                width: popup.width - 64
                spacing: 16
                anchors {
                    top: parent.top
                    topMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 24
                    horizontalCenter: parent.horizontalCenter
                }

                Item {
                    Layout.fillWidth: true
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40

                    Custom.TextField {
                        id: emailField
                        width: parent.width
                        placeHolderText: tr.email
                        anchors.centerIn: parent
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40

                    Custom.TextField {
                        id: nameField
                        width: parent.width
                        placeHolderText: tr.name
                        anchors.centerIn: parent
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.minimumHeight: problemField.height
                    Layout.maximumHeight: problemField.height

                    Custom.TextArea {
                        id: problemField
                        width: parent.width
                        placeHolderText: tr.please_describe_what_you_think_is_wrong
                        preferredHeight: 120
                        height: control.contentHeight + 24 < preferredHeight ? preferredHeight : control.contentHeight + 24
                        control.wrapMode: Text.WordWrap
                        control.verticalAlignment: TextInput.AlignTop
                        control.height: control.contentHeight + 24 < preferredHeight - 8 ? preferredHeight - 8 : control.contentHeight + 24

                        onHeightChanged: {
                            scrollBar.position = 1
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40
                    Layout.topMargin: 8
                    Layout.bottomMargin: 8

                    Custom.Button {
                        width: parent.width
                        text: tr.assign_photo
                        transparent: true
                        color: ui.colors.light3
                        anchors.centerIn: parent
                        visible: !popup.attachedImage

                        Image {
                            sourceSize.width: parent.down ? 32 : 36
                            sourceSize.height: parent.down ? 32 : 36
                            source: "qrc:/resources/images/icons/photo-plus-button.svg"
                            anchors {
                                left: parent.left
                                leftMargin: parent.down ? 6 : 4
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        onClicked: {
                            fileDialog.open()
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: parent.height
                        radius: height / 2
                        color: ui.colors.dark4
                        visible: popup.attachedImage

                        Image {
                            sourceSize.width: 40
                            sourceSize.height: 40
                            source: "qrc:/resources/images/icons/a-delete-button.svg"
                            anchors {
                                left: parent.left
                                verticalCenter: parent.verticalCenter
                            }

                            Custom.HandMouseArea {
                                onClicked: {
                                    popup.attachedImage = null
                                }
                            }
                        }

                        Custom.FontText {
                            text: popup.attachedImage ? popup.attachedImage.name : ""
                            width: parent.width - 112
                            height: parent.height
                            color: ui.colors.white
                            font.bold: true
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            anchors.centerIn: parent
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }
            }
        }

        Item {
            id: buttonItem
            width: parent.width
            height: 88
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors.right: parent.right
            }

            Item {
                width: parent.width - 64
                height: 48
                anchors.centerIn: parent

                Custom.Button {
                    width: parent.width
                    text: tr.send
                    transparent: false
                    enabledCustom: emailField.control.text && nameField.control.text && problemField.control.text
                    anchors.centerIn: parent
                    onClicked: {
                        var data = {}
                        data["email"] = emailField.control.text.trim()
                        data["name"] = nameField.control.text
                        data["problem"] = problemField.control.text
                        if (popup.attachedImage) {
                            data["image"] = popup.attachedImage
                        }

                        app.report_problem(data)
                        popup.close()
                    }
                }
            }
        }
    }

    Connections {
        target: util

        onReportImageLink: {
            popup.attachedImage = data
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
            popup.close()
        }
    }
}
