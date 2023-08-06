import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

AjaxPopup {
    id: popup
    width: 320
    height: 180 + problem.height + 50 - 33

    property string imageName: ""
    property string imageLink: ""

    signal reReportImageLink(variant data)

    onReReportImageLink: {
        imageName = data.name
        imageLink = data.link
    }

    Rectangle {
        width: 320
        height: 144
        anchors.fill: parent
        color: "#2c2c2c"

        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999

        Column {
            anchors.fill: parent
            spacing: 14

            Item {
                width: parent.width
                height: 1
            }

            AjaxTextField {
                id: email
                width: parent.width - 20
                anchors.horizontalCenter: parent.horizontalCenter
                placeholderText: tr.email
                text: {
                    if (typeof appUser == "undefined") return ""
                    return appUser.email
                }
                onTextChanged: {
                    if (!valid) valid = true
                }
            }

            AjaxTextField {
                id: name
                width: parent.width - 20
                anchors.horizontalCenter: parent.horizontalCenter
                placeholderText: tr.name
                onTextChanged: {
                    if (!valid) valid = true
                }
            }

            AjaxTextField {
                width: parent.width - 20
                id: problem
                anchors.horizontalCenter: parent.horizontalCenter
                maximumLength: 299
                placeholderText: tr.please_describe_what_you_think_is_wrong
                wrapMode: Text.WordWrap
                onTextChanged: {
                    if (!valid) valid = true
                }
            }

            AjaxAddItemDelegate {
                width: 248
                height: 34
                label: tr.assign_photo
                visible: imageLink == ""

                mouseArea.onClicked: {
                    imageFileDialog.reportAttach = true
                    imageFileDialog.open()
                }

                anchors {
                    left: parent.left
                    leftMargin: 5
                }
            }

            Item {
                visible: imageLink != ""
                width: 300
                height: 34

                Rectangle {
                    height: 26
                    width: Math.min(imageText.paintedWidth + 44, 274)
                    radius: height/2
                    color: ui.colors.light1
                    opacity: 0.4

                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: parent.left
                        leftMargin: 15
                    }

                    Image {
                        id: closeIco
                        visible: false
                        width: 28
                        height: 28
                        source: "qrc:/resources/images/icons/ic-tooltip-report@2x.png"
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                        }
                    }

                    ColorOverlay {
                        source: closeIco
                        anchors.fill: closeIco
                        color: "#1a1a1a"

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                imageName = ""
                                imageLink = ""
                            }
                        }
                    }

                    Text {
                        id: imageText
                        text: imageName
                        font.family: roboto.name
                        font.pixelSize: 14
                        width: 230
                        elide: Text.ElideRight
                        color: "black"
                        anchors {
                            left: closeIco.right
                            leftMargin: 4
                            verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }

            Item {
                width: parent.width
                height: -20
            }

            MouseArea {
                width: parent.width
                height: 48

                Rectangle {
                    height: 1
                    width: parent.width
                    opacity: 0.1
                    color: ui.colors.light1
                    anchors.top: parent.top
                }

                Text {
                    anchors.centerIn: parent
                    font.family: roboto.name
                    font.pixelSize: 14
                    color: ui.colors.green1
                    text: tr.report_problem
                }

                onClicked: {
                    var notFilled = false
                    if (!email.text.trim()) {
                        email.valid = false
                        notFilled = true
                    }
                    if (!name.text.trim()) {
                        name.valid = false
                        notFilled = true
                    }
                    if (!problem.text.trim()){
                        problem.valid = false
                        notFilled = true
                    }

                    if (notFilled) return
                    client.report_problem(email.text.trim(), name.text.trim(), problem.text.trim(), imageLink)
                }
            }
        }
    }

    Connections {
        target: client

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
            popup.close()
        }
    }

    Component.onCompleted: {
        client.reportImageLink.connect(reReportImageLink)
    }
}
